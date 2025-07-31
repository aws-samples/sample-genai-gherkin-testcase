variable "name" {
  type        = string
  default     = "genai-gherkin-testcase-samples"
  description = "Name of the project"
}
variable "vpc_cidr" {
  type        = string
  default     = "10.0.0.0/16"
  description = "VPC CIDR"
}

variable "region" {
  type        = string
  default     = "us-east-1"
  description = "Default region"
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Key value pairs of tags to apply to resources"
}


variable "model_id" {
  type        = string
  default     = "anthropic.claude-3-7-sonnet-20250219-v1:0"
  description = "Model id for the notebook"
}

variable "model_inference_id" {
  type        = string
  default     = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
  description = "Model inference id for the notebook"
}