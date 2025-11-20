# Bedrock AI Demo

Demo code I had hoped to show you in class...

The night before this class I used AWS to deploy a Bedrock Knowledge Base which integrates with a Large Language Model (LLM) to break down a file in an S3 bucket (S3 is the Amazon "Simple Storage Service" and is similar to something like OneDrive). The file I used was "csc_340_final_project.pdf", it was not hard to deploy this knowledge base and I added the terraform that shows what the infrastructure-as-code equivalent is. This is not a complete example but shows the basic resources needed - this file is [bedrock-kb.tf](bedrock-kb.tf). 

From there I created a Lambda function. A lambda is a function-as-a-service offering from AWS that lets you run code without having to have a CPU to run it on, you don't run it on your laptop, rather you run it in your cloud environment. Lambda was one of the premier AWS services and is a staple in the "serverless" cloud native architecture. Using a simple python script (source code in [bedrock-lambda.py](bedrock-lambda.py)) as a lambda I was able to sent a prompt to the bedrock knowledge base and ask a question about the PDF file above.  The terrform for this is in the file is [bedrock-lambda.tf](bedrock-lambda.tf). 

Much of this will be confusing but it's to demonstrate that to create a large AI application in AWS you don't need more than a few hundred lines of code.

You can expose a lambda function via an invocation URL so you can use a command like `curl` to invoke the lambda with a prompt - for example:

```
curl -X POST "https://6kbn6uckov2ib7eo2bwblxtjum0lelra.lambda-url.us-east-1.on.aws/" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What do you think is the hardest part of this project?"}' \
  --ssl-no-revoke
```

Feel free to run this! (you will need to install `curl` if you do not have it, should be included on MacOS and GitBash on Windows)

Here is an example of what that looks like - the output is not very readable but :

<img width="781" height="272" alt="image" src="https://github.com/user-attachments/assets/2e5bae5f-4f2f-44ec-93fa-0153a8341e53" />

Here is an altnative command that strips out the response from the output for readability (note requires both `curl` and `jq` commands):

```
curl -s -X POST "https://6kbn6uckov2ib7eo2bwblxtjum0lelra.lambda-url.us-east-1.on.aws/" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What do you think is the hardest part of this project?"}' \
  --ssl-no-revoke | jq -r '.response'

Based on the provided search results, it seems that the hardest part of the project can be attributed to several factors:

1. **Lack of communication within the group**: Effective communication is crucial for the success of any group project.
If team members are not communicating well, it can lead to misunderstandings, missed deadlines, and a lack of cohesion
in the project.

2. **Procrastination**: Delaying tasks until the last minute can lead to rushed work, mistakes, and increased stress.
It's important to manage time effectively and avoid procrastination to ensure the quality of the project.

3. **Poor time management**: Allocating sufficient time for each task and adhering to the project timeline is essential.
Poor time management can result in incomplete tasks, missed deadlines, and a lack of progress.

4. **Underestimating the time/work involved**: It's easy to underestimate the amount of work required for each task,
which can lead to unrealistic expectations and a lack of preparedness. It's important to accurately estimate the time
and effort needed for each task.

5. **Collaboration and shared responsibilities**: Working effectively with a team and understanding each member's
role and responsibilities can be challenging. It's important to establish clear roles and responsibilities,
communicate effectively, and ensure that everyone is contributing to the project.

To overcome these challenges, it's essential to communicate regularly with team members, manage time effectively,
accurately estimate the work required, and establish clear roles and responsibilities. Additionally, seeking help
when needed and choosing a project that everyone in the group enjoys working on can contribute to a more successful
and enjoyable group project experience.
````
