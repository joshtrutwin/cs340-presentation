import json
import boto3
import os

region = os.environ.get("AWS_REGION", "us-east-1")
client_bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name=region)

# this is a bedrock Knowledge Base containing some files provided by your professor (syllabus and CS340 project)
KNOWLEDGE_BASE_ID = "UPAR77QGDP"
# this is the LLM we will ask questions to - I don't have many other models like claude configured in my AWS account
MODEL_ARN = "arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-micro-v1:0"

def lambda_handler(event, context):
    try:
        user_prompt = event.get("prompt")
        if not user_prompt:
            return {
                'statusCode': 400,
                'body': json.dumps({"error": "Missing 'prompt' in the event payload"})
            }

        # send the prompt to our LL om choice configured above and dump the response to output
        response = client_bedrock_agent_runtime.retrieve_and_generate(
            input={'text': user_prompt},
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': KNOWLEDGE_BASE_ID,
                    'modelArn': MODEL_ARN
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
