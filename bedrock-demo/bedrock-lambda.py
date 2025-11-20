import json
import boto3
import os

region = os.environ.get("AWS_REGION", "us-east-1")
client_bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name=region)

# --- Configuration ---
KNOWLEDGE_BASE_ID = os.environ['KNOWLEDGE_BASE_ID']
LLM_MODEL_ARN = os.environ['LLM_MODEL_ARN']

def lambda_handler(event, context):
    try:
        # Support both Lambda Function URL (event.body) and direct invoke (event.prompt)
        if 'body' in event:
            # Lambda Function URL - body is a JSON string
            body = event.get('body', '{}')
            if isinstance(body, str):
                body = json.loads(body)
            user_prompt = body.get("prompt")
        else:
            # Direct invoke from console or SDK
            user_prompt = event.get("prompt")
        
        if not user_prompt:
            return {
                'statusCode': 400,
                'body': json.dumps({"error": "Invalid input, try again..."})
            }

        response = client_bedrock_agent_runtime.retrieve_and_generate(
            input={'text': user_prompt},
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': KNOWLEDGE_BASE_ID,
                    'modelArn': LLM_MODEL_ARN
                }
            }
        )

        response_text = response['output']['text']

        return {
            'statusCode': 200,
            'body': json.dumps({"response": response_text})
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({"error": str(e)})
        }
