## Overview

Automated test generation that converts OpenAPI/Swagger specifications into Gherkin feature files 
and Java test step definitions.
This project provides notebook and prompts that helps generates consistent BDD test scenarios from 
API specifications, reducing manual test creation effort and ensuring comprehensive API coverage.

## Components
### Jupyter Notebook (gherkin_java_generator.ipynb)

Interactive notebook for generating Gherkin scenarios and Java test stubs from OpenAPI specifications. <br/>
Features:<br/>

Parse Swagger/OpenAPI JSON files.<br/>
Uses Amazon Bedrock foundation models for test scenario creation.<br/>
Generate Gherkin feature files with contextual placeholders.<br/>
Create corresponding Java step definition classes with RestAssured integration.<br/>
Support for multiple HTTP methods and response codes.


## Terraform Infrastructure (terraform)
AWS infrastructure setup for running the automation framework.<br/>
Components:<br/>
* Main Infrastructure (main.tf, provider.tf, variables.tf)
  * VPC and networking setup
  * KMS encryption configuration
  * Security groups and IAM roles
* SageMaker Notebook (notebook/)
  * Jupyter notebook instance for development
  * Pre-configured with required dependencies
  * Lifecycle scripts for environment setup

## Getting Started

### Requirements

* Python 3.8+
* Jupyter Notebook
* Terraform 1.0+
* AWS CLI (for deployment)

### Usage

#### Deploy Infrastructure:

```
git clone https://github.com/aws-samples/sample-genai-gherkin-testcase.git
cd terraform
terraform init
terraform apply
```

#### Access SageMaker:

* Open AWS Console → SageMaker → Notebook Instances
* Click "Open Jupyter" on your instance
* Navigate to gherkin_java_generator.ipynb


#### Generate Tests

* Add API Specification:
* Upload your OpenAPI/Swagger JSON file in **input** folder

#### Run Generation:

* Execute notebook cells sequentially
* Customize prompts in **prompts** if needed
* Modify templates in prompts to:
  * Change output format
  * Add custom validation logic
  * Support additional API patterns

* Collect Output:
  * Gherkin features: **output/features/**
  * Java step definitions: **output/stubs/**

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

