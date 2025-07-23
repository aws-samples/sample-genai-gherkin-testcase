
data "aws_availability_zones" "available" {}
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}


locals {
  region   = data.aws_region.current.name
  account  = data.aws_caller_identity.current.account_id
  azs      = slice(data.aws_availability_zones.available.names, 0, 2)
  vpc_cidr = var.vpc_cidr
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.21.0"

  name = "${var.name}-vpc"
  cidr = local.vpc_cidr
  azs  = local.azs

  private_subnets = [for k, v in local.azs : cidrsubnet(local.vpc_cidr, 8, k)]
  public_subnets  = [for k, v in local.azs : cidrsubnet(local.vpc_cidr, 8, k + 4)]

  enable_nat_gateway = true
  single_nat_gateway = true

  tags = var.tags
}

module "vpc_endpoints" {
  source  = "terraform-aws-modules/vpc/aws//modules/vpc-endpoints"
  vpc_id = module.vpc.vpc_id
  create_security_group = true
  security_group_name_prefix = "${var.name}-vpc-endpoint-"
  security_group_rules = {
    ingress_https = {
      description = "ingress_https"
      protocol    = "tcp"
      from_port   = 443
      to_port     = 443
      cidr_blocks = [module.vpc.vpc_cidr_block]
    }
  }
  endpoints = {
    bedrock-runtime = {
      service = "bedrock-runtime"
      subnet_ids = module.vpc.private_subnets
      service_type = "Interface"
    }
  }
}


module "kms" {
  source  = "terraform-aws-modules/kms/aws"
  version = "3.1.1"
  key_usage   = "ENCRYPT_DECRYPT"
  # Aliases
  aliases = [var.name]
  key_statements = [
    {
      sid = "CloudWatchLogs"
      actions = [
        "kms:Encrypt*",
        "kms:Decrypt*",
        "kms:ReEncrypt*",
        "kms:GenerateDataKey*",
        "kms:Describe*"
      ]
      resources = ["*"]
      principals = [
        {
          type        = "Service"
          identifiers = ["logs.${local.region}.amazonaws.com"]
        }
      ]

      conditions = [
        {
          test     = "ArnLike"
          variable = "kms:EncryptionContext:aws:logs:arn"
          values = [
            "arn:aws:logs:${local.region}:${local.account}:log-group:*",
          ]
        }
      ]
    },
    {
      sid = "BedrockModelLogsInvocation"
      actions = [
        "kms:GenerateDataKey*"
      ]
      resources = ["*"]

      principals = [
        {
          type        = "Service"
          identifiers = ["bedrock.amazonaws.com"]
        }
      ]

      conditions = [
        {
          test     = "StringEquals"
          variable = "aws:SourceAccount"
          values = [
            data.aws_caller_identity.current.account_id
          ]
        }
      ]
    }
  ]
  tags = var.tags
}

# Bedrock Invocation logging Role
resource "aws_iam_role" "bedrock_model_logging" {
  name = "${var.name}-bedrock_model_logging-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = "AmazonBedrockLoggingAssumeRole"
        Principal = {
          Service = "bedrock.amazonaws.com"
        },
        Condition = {
          StringEquals = {
            "aws:SourceAccount" = data.aws_caller_identity.current.account_id
          }
          ArnLike = {
            "aws:SourceArn" = "arn:aws:bedrock:${local.region}:${local.account}:*"
          }
        }
      },
    ]
  })
  inline_policy {
    name = "AmazonBedrockLogsWrite"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action   = [
            "logs:CreateLogStream",
            "logs:PutLogEvents"
          ]
          Effect   = "Allow"
          Resource = "arn:aws:logs:${local.region}:${local.account}:log-group:${aws_cloudwatch_log_group.bedrock_model_log_group.name}:log-stream:aws/bedrock/modelinvocations"
        }
      ]

    })
  }
  tags = var.tags
}


# Enable bedrock model_invocation_logging
resource "aws_cloudwatch_log_group" "bedrock_model_log_group" {
  name              = "${var.name}-bedrock-logging"
  retention_in_days = 365
  kms_key_id        = module.kms.key_arn
}

# Enable bedrock model_invocation_logging
resource "aws_bedrock_model_invocation_logging_configuration" "bedrock_model_logging" {
  logging_config {
    cloudwatch_config {
      log_group_name = aws_cloudwatch_log_group.bedrock_model_log_group.name
      role_arn = aws_iam_role.bedrock_model_logging.arn
    }
    embedding_data_delivery_enabled = false
    image_data_delivery_enabled     = false
    text_data_delivery_enabled      = true
  }
}


module "notebook" {
  source                      = "./notebook"
  name                        = var.name
  subnet_id                   = module.vpc.private_subnets[0]
  vpc_id                      = module.vpc.vpc_id
  kms_key_id                  = module.kms.key_id
  model_id                    = var.model_id
  model_inference_id          = var.model_inference_id
  default_code_repository_url = "https://github.com/aws-samples/sample-genai-gherkin-testcase.git"
}

