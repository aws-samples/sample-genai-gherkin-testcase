variable "name" {
  type        = string
  default     = "genai-gherkin-testcase-samples"
  description = "Name of the project"
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Key value pairs of tags to apply to resources"
}

variable "vpc_id" {
  type        = string
  description = "VPC id of the vpc"
}

variable "subnet_id" {
  type        = string
  description = "Subnet id of the subnet to use for notebook"
}

variable "instance_type" {
  type        = string
  default     = "ml.t2.medium"
  description = "Instance type for the notebook"
}

variable "volume_size" {
  type        = number
  default     = 30
  description = "Volume size in GB"
}


variable "kms_key_id" {
  type        = string
  description = "KMS key id for encryption"
}

variable "model_id" {
  type        = string
  description = "Model id for the notebook"
}

variable "model_inference_id" {
  type        = string
  description = "Model inference id for the notebook"
}


variable "default_code_repository_url" {
  type        = string
  description = "Default code repository url for the notebook"
  default     = null
}

variable "secrets_manager_arn" {
  type        = string
  description = "AWS Secrets Manager secret that contains the credentials used to access the git repository"
  default     = null
}

