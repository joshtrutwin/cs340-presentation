# Bedrock Lambda Function Resources
# Note: These resources are deployed in us-east-1

# Lambda function
resource "aws_lambda_function" "concordia_cs340_bedrock_test" {
  provider = aws.us_east_1

  function_name = "concordia-cs340-bedrock-test"  
  runtime       = "python3.13"
  handler       = "lambda_function.lambda_handler"
  memory_size   = 128
  timeout       = 3
  publish       = false
  architectures = ["x86_64"]
  
  # permissions - see bedrock-lambda-iam.tf
  role = aws_iam_role.concordia_cs340_bedrock_lambda_role.arn
 
  # Placeholder filename - will be populated on import, then ignored
  filename         = "lambda_placeholder.zip"
  source_code_hash = "placeholder"

  # Ignore changes to the code - managed outside of Terraform
  lifecycle {
    ignore_changes = [
      filename,
      source_code_hash
      # Note: The lifecycle block ignores changes to the code/deployment package
      # This allows Terraform to manage the Lambda configuration (runtime, memory, etc.)
      # while the code is managed outside of Terraform (CI/CD, manual uploads, etc.)
    ]
  }

  # Environment variables to pass to the function
  environment {
    variables = {
      KNOWLEDGE_BASE_ID = aws_bedrockagent_knowledge_base.concordia_cs340_bedrock_kb.id
      LLM_MODEL_ARN     = "arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-micro-v1:0"
    }
  }

  tags = merge(local.common_tags, {
    Name = "concordia-cs340-bedrock-test"
    Role = "Bedrock Test Lambda Function"
  })
}

# Lambda Function URL for public HTTPS access
resource "aws_lambda_function_url" "concordia_cs340_bedrock_test_url" {
  provider = aws.us_east_1

  function_name      = aws_lambda_function.concordia_cs340_bedrock_test.function_name
  authorization_type = "NONE"  # Public access - anyone with the URL can invoke

  cors {
    allow_origins     = ["*"]
    allow_methods     = ["POST"]
    allow_headers     = ["content-type"]
    max_age           = 86400
  }
}

# Output the function URL so students can use it
output "bedrock_lambda_url" {
  value       = aws_lambda_function_url.concordia_cs340_bedrock_test_url.function_url
  description = "Public HTTPS URL for the Bedrock test Lambda function"
}
