data "aws_availability_zones" "available" {}
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

data "aws_iam_policy_document" "notebook_policy_document" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["sagemaker.amazonaws.com"]
    }
  }
}
