resource "aws_iam_role" "notebook_role" {
  name_prefix        = local.name
  path               = "/"
  description        = "Role for SageMaker Notebook"
  tags               = local.tags
  assume_role_policy = data.aws_iam_policy_document.notebook_policy_document.json

  inline_policy {
    name = "sagemaker-notebook-policy"
    policy = jsonencode({
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Effect" : "Allow",
          "Action" : [
            "sagemaker:CreatePresignedDomainUrl",
            "sagemaker:DescribeNotebookInstanceLifecycleConfig",
            "sagemaker:DeleteNotebookInstance",
            "sagemaker:DescribeNotebookInstance",
            "sagemaker:StopNotebookInstance",
            "sagemaker:UpdateNotebookInstanceLifecycleConfig",
            "sagemaker:CreateNotebookInstanceLifecycleConfig",
            "sagemaker:StartNotebookInstance"
          ],
          "Resource" : [
            "arn:aws:sagemaker:${local.region}:${local.account}:notebook-instance/*",
            "arn:aws:sagemaker:${local.region}:${local.account}:notebook-instance-lifecycle-config/*"
          ]
        },
        {
          "Effect" : "Allow",
          "Action" : [
            "bedrock:InvokeModel",
            "bedrock:InvokeModelWithResponseStream"
          ],
          "Resource" : [
            "arn:aws:bedrock:*::foundation-model/${local.model_id}",
            aws_bedrock_inference_profile.bedrock_profile.arn
          ]
        },
        {
          "Effect" : "Allow",
          "Action" : [
            "kms:Encrypt",
            "kms:Decrypt",
            "kms:ReEncrypt*",
            "kms:GenerateDataKey*",
            "kms:DescribeKey"
          ],
          "Resource" : [
            "arn:aws:kms:${local.region}:${local.account}:key/${local.kms_key_id}",
          ]
        }
      ]
    })
  }
}

resource "aws_security_group" "notebook_security_group" {
  name_prefix = "${local.name}-sg"
  vpc_id      = local.vpc_id
  tags        = local.tags
  description = "Notebook security group"
  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow egress to internet"
  }
}

resource "aws_sagemaker_code_repository" "repository" {
  count                = local.default_code_repository_url == null ? 0 : 1
  code_repository_name = "${local.name}-github-repo"

  git_config {
    repository_url = local.default_code_repository_url
    secret_arn     = local.secrets_manager_arn
  }
}


resource "aws_bedrock_inference_profile" "bedrock_profile" {
  name        = local.name
  description = "Profile with tag for cost allocation tracking"

  model_source {
    # Include account ID to use inference profiles
    copy_from = "arn:aws:bedrock:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:inference-profile/${local.model_inference_id}"
  }

  tags = local.tags
}

resource "aws_sagemaker_notebook_instance" "notebook" {
  name                    = "${local.name}-notebook-instance"
  role_arn                = aws_iam_role.notebook_role.arn
  instance_type           = local.instance_type
  volume_size             = local.volume_size
  default_code_repository = local.default_code_repository_url == null ? null : aws_sagemaker_code_repository.repository[0].code_repository_name
  subnet_id               = local.subnet_id
  root_access             = "Disabled"
  direct_internet_access  = "Disabled"
  kms_key_id              = local.kms_key_id
  tags                    = local.tags
  lifecycle_config_name   = "${local.name}-lc"
  security_groups         = [aws_security_group.notebook_security_group.id]
  instance_metadata_service_configuration {
    minimum_instance_metadata_service_version = "2"
  }
}

resource "aws_sagemaker_notebook_instance_lifecycle_configuration" "notebook_lc" {
  name = "${local.name}-lc"
  on_start = base64encode(
    templatefile("${path.module}/lifecycle_scripts.tftpl", { inference_model_arn = aws_bedrock_inference_profile.bedrock_profile.arn })
  )
}

