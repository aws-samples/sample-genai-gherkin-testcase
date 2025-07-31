locals {

  name    = var.name
  account = data.aws_caller_identity.current.account_id
  region  = data.aws_region.current.name
  tags    = var.tags

  vpc_id                      = var.vpc_id
  subnet_id                   = var.subnet_id
  kms_key_id                  = var.kms_key_id
  instance_type               = var.instance_type
  volume_size                 = var.volume_size
  model_id                    = var.model_id
  model_inference_id          = var.model_inference_id
  default_code_repository_url = var.default_code_repository_url
  secrets_manager_arn         = var.secrets_manager_arn
}