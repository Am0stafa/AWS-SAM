# AWS Serverless Application Model (SAM) Hello World Application

## Table of Contents
1. [Introduction to AWS SAM](#introduction-to-aws-sam)
2. [How AWS SAM Works](#how-aws-sam-works)
3. [Project Structure](#project-structure)
4. [Prerequisites](#prerequisites)
5. [Getting Started](#getting-started)
6. [Developing with AWS SAM](#developing-with-aws-sam)
7. [Deploying Your Application](#deploying-your-application)
8. [Testing Your Application](#testing-your-application)
9. [Modifying and Updating Your Application](#modifying-and-updating-your-application)
10. [Cleaning Up](#cleaning-up)
11. [Building a RESTful API with Lambda and API Gateway using SAM](#Building a RESTful API with Lambda and API Gateway using SAM)
12. [Advanced Topics](#advanced-topics)
13. [Troubleshooting](#troubleshooting)
14. [Additional Resources](#additional-resources)

## Introduction to AWS SAM

AWS Serverless Application Model (SAM) is an open-source framework for building serverless applications on AWS. It provides a simplified way to define the Amazon API Gateway APIs, AWS Lambda functions, and Amazon DynamoDB tables needed by your serverless application[^1].

SAM consists of two main components:
1. **AWS SAM template specification**: An extension of AWS CloudFormation templates with a simpler syntax for configuring common serverless application resources.
2. **AWS SAM CLI**: A command-line tool that helps you develop, test, and deploy your serverless applications defined by SAM templates.

## How AWS SAM Works

AWS SAM works by extending CloudFormation templates with simplified syntax for defining serverless resources. Here's a high-level overview of how SAM works[^1]:

1. You define your serverless application using AWS SAM syntax in a YAML file (typically named `template.yaml`).
2. You use the SAM CLI to package your application, which:
   - Uploads your application code to an S3 bucket.
   - Generates a CloudFormation template that represents your SAM template.
3. You then use the SAM CLI to deploy your application, which:
   - Deploys the generated CloudFormation template to AWS.
   - Creates and manages all the specified AWS resources.

## Project Structure

A typical SAM project structure looks like this:

```
sam-app/
├── .aws-sam/
├── events/
│   └── event.json
├── hello_world/
│   ├── __init__.py
│   ├── app.py
│   └── requirements.txt
├── tests/
│   ├── unit/
│   └── integration/
├── .gitignore
├── README.md
├── samconfig.toml
└── template.yaml
```

Key files and directories:
- `template.yaml`: The SAM template file that defines your application's AWS resources.
- `hello_world/app.py`: The Lambda function code.
- `hello_world/requirements.txt`: Python dependencies for the Lambda function.
- `events/`: Contains sample event data for testing.
- `tests/`: Contains unit and integration tests.
- `samconfig.toml`: Configuration file for your SAM CLI commands.

## Prerequisites

Before you begin, ensure you have the following installed and configured:

1. [AWS CLI](https://aws.amazon.com/cli/)
2. [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
3. [Python 3.9](https://www.python.org/downloads/) or later
4. [Docker](https://docs.docker.com/get-docker/) (for local testing)

Also, make sure you have configured your AWS credentials using `aws configure`.

## Getting Started

To create a new SAM application:

1. Open your terminal and run:
   ```
   sam init
   ```
2. Follow the prompts to select your desired options. For this example, choose:
   - AWS Quick Start Templates
   - Hello World Example
   - Python for the runtime

This will create a new directory with your project files.

## Developing with AWS SAM

The main file you'll work with is `template.yaml`. This file defines your serverless application's resources. Here's a breakdown of its key sections:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Sample SAM Template

Globals:
  Function:
    Timeout: 3

Resources:
  HelloWorldFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: hello_world/
      Handler: app.lambda_handler
      Runtime: python3.9
      Events:
        HelloWorld:
          Type: Api
          Properties:
            Path: /hello
            Method: get

Outputs:
  HelloWorldApi:
    Description: API Gateway endpoint URL for Prod stage for Hello World function
    Value: !Sub "https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/hello/"
```

This template defines:
- A Lambda function (`HelloWorldFunction`)
- An API Gateway endpoint that triggers the function
- An output that provides the API endpoint URL

## Deploying Your Application

To deploy your application:

1. Build your application:
   ```
   sam build --use-container
   ```

2. Deploy your application:
   ```
   sam deploy --guided
   ```

   Follow the prompts to configure your deployment settings. This will create a `samconfig.toml` file with your preferences.

3. For subsequent deployments, you can simply run:
   ```
   sam deploy
   ```

## Testing Your Application

You can test your application locally or in the cloud:

### Local Testing

1. Invoke the function locally:
   ```
   sam local invoke HelloWorldFunction
   ```

2. Start a local API:
   ```
   sam local start-api
   ```
   Then, you can access your API at `http://localhost:3000/hello`

### Cloud Testing

After deployment, you can test your live API using the URL provided in the Outputs section of the deployment process.

## Modifying and Updating Your Application

1. Make changes to your application code in `hello_world/app.py`.
2. Update your SAM template (`template.yaml`) if you're adding new resources or changing configurations.
3. Rebuild and redeploy your application:
   ```
   sam build --use-container
   sam deploy
   ```

For faster development iterations, you can use the `sam sync` command:

```
sam sync --watch
```

This command will automatically detect changes and update your application in the cloud.

## Building a RESTful API with Lambda and API Gateway using SAM

AWS SAM makes it straightforward to build RESTful APIs using Lambda functions and Amazon API Gateway. Let's walk through the process of creating a simple CRUD (Create, Read, Update, Delete) API for a "Todo" application.

### 1. Define the API in the SAM Template

First, we'll update our `template.yaml` to define our API and Lambda functions:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Todo API

Globals:
  Function:
    Timeout: 3
    Runtime: python3.9

Resources:
  TodoApi:
    Type: AWS::Serverless::Api
    Properties:
      StageName: Prod
      Cors:
        AllowMethods: "'GET,POST,PUT,DELETE'"
        AllowHeaders: "'Content-Type'"
        AllowOrigin: "'*'"

  GetTodosFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: todo_api/
      Handler: app.get_todos
      Events:
        GetTodos:
          Type: Api
          Properties:
            RestApiId: !Ref TodoApi
            Path: /todos
            Method: GET

  CreateTodoFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: todo_api/
      Handler: app.create_todo
      Events:
        CreateTodo:
          Type: Api
          Properties:
            RestApiId: !Ref TodoApi
            Path: /todos
            Method: POST

  UpdateTodoFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: todo_api/
      Handler: app.update_todo
      Events:
        UpdateTodo:
          Type: Api
          Properties:
            RestApiId: !Ref TodoApi
            Path: /todos/{todoId}
            Method: PUT

  DeleteTodoFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: todo_api/
      Handler: app.delete_todo
      Events:
        DeleteTodo:
          Type: Api
          Properties:
            RestApiId: !Ref TodoApi
            Path: /todos/{todoId}
            Method: DELETE

Outputs:
  ApiUrl:
    Description: "API Gateway endpoint URL for Prod stage"
    Value: !Sub "https://${TodoApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/"
```

This template defines:
- An API Gateway (`TodoApi`) with CORS configuration
- Four Lambda functions for GET, POST, PUT, and DELETE operations
- API events that connect each function to a specific HTTP method and path
- An output that provides the API endpoint URL

### 2. Implement the Lambda Functions

Next, create a file `todo_api/app.py` with the following content:

```python
import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Todos')

def get_todos(event, context):
    response = table.scan()
    return {
        "statusCode": 200,
        "body": json.dumps(response['Items'])
    }

def create_todo(event, context):
    todo = json.loads(event['body'])
    response = table.put_item(Item=todo)
    return {
        "statusCode": 201,
        "body": json.dumps({"message": "Todo created successfully"})
    }

def update_todo(event, context):
    todoId = event['pathParameters']['todoId']
    todo = json.loads(event['body'])
    response = table.update_item(
        Key={'id': todoId},
        UpdateExpression="set title=:t, completed=:c",
        ExpressionAttributeValues={
            ':t': todo['title'],
            ':c': todo['completed']
        },
        ReturnValues="UPDATED_NEW"
    )
    return {
        "statusCode": 200,
        "body": json.dumps(response['Attributes'])
    }

def delete_todo(event, context):
    todoId = event['pathParameters']['todoId']
    response = table.delete_item(Key={'id': todoId})
    return {
        "statusCode": 204,
        "body": ""
    }
```

This implements the four CRUD operations using DynamoDB as the backend database.

### 3. Add DynamoDB Table to the SAM Template

Add the following resource to your `template.yaml`:

```yaml
  TodoTable:
    Type: AWS::Serverless::SimpleTable
    Properties:
      PrimaryKey:
        Name: id
        Type: String
```

### 4. Update IAM Permissions

Add IAM permissions for your Lambda functions to access DynamoDB. Update each function in the `template.yaml`:

```yaml
  GetTodosFunction:
    Type: AWS::Serverless::Function
    Properties:
      # ... other properties ...
      Policies:
        - DynamoDBReadPolicy:
            TableName: !Ref TodoTable

  CreateTodoFunction:
    Type: AWS::Serverless::Function
    Properties:
      # ... other properties ...
      Policies:
        - DynamoDBWritePolicy:
            TableName: !Ref TodoTable

  UpdateTodoFunction:
    Type: AWS::Serverless::Function
    Properties:
      # ... other properties ...
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref TodoTable

  DeleteTodoFunction:
    Type: AWS::Serverless::Function
    Properties:
      # ... other properties ...
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref TodoTable
```

### 5. Build and Deploy

Build and deploy your application:

```bash
sam build
sam deploy --guided
```

### 6. Testing Your API

After deployment, SAM will output the API Gateway endpoint URL. You can use tools like curl or Postman to test your API:

```bash
# Get all todos
curl https://your-api-id.execute-api.your-region.amazonaws.com/Prod/todos

# Create a new todo
curl -X POST https://your-api-id.execute-api.your-region.amazonaws.com/Prod/todos \
     -H "Content-Type: application/json" \
     -d '{"id": "1", "title": "Learn SAM", "completed": false}'

# Update a todo
curl -X PUT https://your-api-id.execute-api.your-region.amazonaws.com/Prod/todos/1 \
     -H "Content-Type: application/json" \
     -d '{"title": "Learn SAM", "completed": true}'

# Delete a todo
curl -X DELETE https://your-api-id.execute-api.your-region.amazonaws.com/Prod/todos/1
```

### 7. Local Testing

SAM allows you to test your API locally before deploying:

```bash
sam local start-api
```

This will start a local API Gateway that you can use for testing.

### 8. Adding API Documentation

You can add API documentation using Swagger/OpenAPI. Create a file named `swagger.yaml` and reference it in your `template.yaml`:

```yaml
  TodoApi:
    Type: AWS::Serverless::Api
    Properties:
      StageName: Prod
      DefinitionBody:
        Fn::Transform:
          Name: AWS::Include
          Parameters:
            Location: swagger.yaml
```

### 9. Monitoring and Logging

SAM automatically sets up CloudWatch Logs for your Lambda functions. You can view these logs in the AWS Console or using the AWS CLI:

```bash
sam logs -n GetTodosFunction --stack-name your-stack-name
```

### 10. Continuous Deployment

For continuous deployment, you can use AWS CodePipeline with SAM. Create a `buildspec.yml` file in your project root:

```yaml
version: 0.2
phases:
  install:
    runtime-versions:
      python: 3.9
  build:
    commands:
      - sam build
      - sam deploy --no-confirm-changeset --no-fail-on-empty-changeset
```

Then set up a CodePipeline that uses this buildspec file.

By following these steps, you've created a fully functional RESTful API using AWS SAM, Lambda, and API Gateway. This approach allows for easy development, testing, and deployment of serverless APIs.

Remember always to consider security best practices, such as implementing proper authentication and authorization for your API endpoints.


## Cleaning Up

To delete your application and all associated resources:

```
sam delete
```

## Advanced Topics

- **Layers**: Use Lambda Layers to manage dependencies and shared code.
- **Step Functions**: Integrate with AWS Step Functions for complex workflows.
- **SAM Policy Templates**: Use predefined IAM policies for common use cases.
- **Custom Resources**: Extend SAM with custom CloudFormation resources.

## Troubleshooting

For common issues and solutions, refer to the [AWS SAM CLI Troubleshooting Guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-troubleshooting.html).

## Additional Resources

- [AWS SAM Developer Guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)
- [AWS SAM CLI Command Reference](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-command-reference.html)
- [AWS SAM Template Specification](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-specification.html)
- [Serverless Land](https://serverlessland.com/) - A collection of serverless resources and examples

By following this guide, you should now have a solid understanding of AWS SAM and be able to build, deploy, and manage serverless applications on AWS. Remember to always refer to the official AWS documentation for the most up-to-date information and best practices.

[^1]: https://aws.amazon.com/serverless/sam/
