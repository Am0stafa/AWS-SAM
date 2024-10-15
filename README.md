# AWS Serverless Application Model (SAM) Guide

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
10. [Building a RESTful API with Lambda and API Gateway using SAM](#building-a-restful-api-with-lambda-and-api-gateway-using-sam)
11. [Building a RESTful API with JavaScript, Prisma, and AWS SAM](#building-a-restful-api-with-javascript-prisma-and-aws-sam)
12. [Cleaning Up](#cleaning-up)
13. [Advanced Topics](#advanced-topics)
14. [Troubleshooting](#troubleshooting)
15. [Additional Resources](#additional-resources)

## Introduction to AWS SAM

AWS Serverless Application Model (SAM) is an open-source framework for building serverless applications on AWS. It simplifies the process of defining Amazon API Gateway APIs, AWS Lambda functions, and Amazon DynamoDB tables for your serverless applications.

SAM consists of two main components:
1. **AWS SAM template specification**: An extension of AWS CloudFormation templates with a simpler syntax for serverless resources.
2. **AWS SAM CLI**: A command-line tool for developing, testing, and deploying serverless applications.

## How AWS SAM Works

1. Define your serverless application using AWS SAM syntax in a YAML file (`template.yaml`).
2. Use the SAM CLI to package your application:
   - Uploads your code to an S3 bucket.
   - Generates a CloudFormation template from your SAM template.
3. Deploy your application using the SAM CLI:
   - Deploys the CloudFormation template to AWS.
   - Creates and manages all specified AWS resources.

## Project Structure

A typical SAM project structure:

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

## Prerequisites

Ensure you have the following installed and configured:

1. [AWS CLI](https://aws.amazon.com/cli/)
2. [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
3. [Python 3.9](https://www.python.org/downloads/) or later
4. [Docker](https://docs.docker.com/get-docker/) (for local testing)
5. AWS credentials configured (`aws configure`)

## Getting Started

Create a new SAM application:

```bash
sam init
```

Follow the prompts to select your options (e.g., AWS Quick Start Templates, Hello World Example, Python runtime).

## Developing with AWS SAM

The main file is `template.yaml`. Here's a basic example:

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

## Building a RESTful API with JavaScript, Prisma, and AWS SAM

AWS Serverless Application Model (SAM) provides an excellent framework for building and deploying serverless applications, including RESTful APIs. Let's walk through the process of creating a RESTful API using JavaScript, Prisma as the ORM, and AWS SAM for deployment.

### 1. Set Up the Project

First, create a new directory for your project and initialize it:

```bash
mkdir sam-prisma-api
cd sam-prisma-api
npm init -y
```

Install the necessary dependencies:

```bash
npm install @prisma/client express
npm install --save-dev prisma @types/express aws-sdk
```

### 2. Initialize Prisma

Initialize Prisma in your project:

```bash
npx prisma init
```

This will create a `prisma` directory with a `schema.prisma` file. Update the `schema.prisma` file with your data model. For example:

```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
  binaryTargets = ["native", "rhel-openssl-1.0.x"]
}

model User {
  id    Int     @id @default(autoincrement())
  email String  @unique
  name  String?
  posts Post[]
}

model Post {
  id        Int     @id @default(autoincrement())
  title     String
  content   String?
  published Boolean @default(false)
  author    User    @relation(fields: [authorId], references: [id])
  authorId  Int
}
```

Note the `binaryTargets` in the `generator` block. This is crucial for AWS Lambda deployment, as mentioned in the Prisma documentation[^1].

### 3. Create the Express App

Create a file named `app.js` in your project root:

```javascript
const express = require('express');
const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();
const app = express();

app.use(express.json());

// GET all users
app.get('/users', async (req, res) => {
  const users = await prisma.user.findMany();
  res.json(users);
});

// POST new user
app.post('/users', async (req, res) => {
  const { name, email } = req.body;
  const user = await prisma.user.create({
    data: { name, email },
  });
  res.json(user);
});

// GET user by id
app.get('/users/:id', async (req, res) => {
  const { id } = req.params;
  const user = await prisma.user.findUnique({
    where: { id: parseInt(id) },
  });
  res.json(user);
});

module.exports = app;
```

### 4. Create the Lambda Handler

Create a file named `lambda.js`:

```javascript
const serverless = require('serverless-http');
const app = require('./app');

module.exports.handler = serverless(app);
```

### 5. Set Up AWS SAM Template

Create a `template.yaml` file in your project root:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: SAM Prisma API

Globals:
  Function:
    Timeout: 3

Resources:
  ApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: ./
      Handler: lambda.handler
      Runtime: nodejs14.x
      Events:
        Api:
          Type: Api
          Properties:
            Path: /{proxy+}
            Method: ANY
      Environment:
        Variables:
          DATABASE_URL: !Ref DatabaseUrl

  ApiGatewayApi:
    Type: AWS::Serverless::Api
    Properties:
      StageName: Prod

Parameters:
  DatabaseUrl:
    Type: String
    Description: The URL for the database

Outputs:
  ApiEndpoint:
    Description: "API Gateway endpoint URL"
    Value: !Sub "https://${ApiGatewayApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/"
```

### 6. Configure SAM for Local Testing

Create a `env.json` file for local testing:

```json
{
  "ApiFunction": {
    "DATABASE_URL": "your-database-url-here"
  }
}
```

### 7. Build and Deploy

Build your SAM application:

```bash
sam build
```

Deploy your application:

```bash
sam deploy --guided
```

Follow the prompts to configure your deployment settings.

### 8. Testing Your API

After deployment, SAM will output the API Gateway endpoint URL. You can use tools like curl or Postman to test your API endpoints.

For local testing, you can use:

```bash
sam local start-api --env-vars env.json
```

This setup creates a serverless RESTful API using JavaScript, Prisma as the ORM, and AWS SAM for deployment. It incorporates the best practices for deploying Prisma to AWS Lambda, such as specifying the correct `binaryTargets` in the Prisma schema[^1].

Remember to handle environment variables securely, especially the `DATABASE_URL`, as suggested in the SST deployment guide[^2]. You might want to use AWS Systems Manager Parameter Store or AWS Secrets Manager for managing sensitive configuration in production.

By following this approach, you can create a scalable, serverless API that leverages the power of Prisma for database operations and AWS Lambda for compute. This setup allows for easy development, testing, and deployment of your API, while maintaining the benefits of a serverless architecture.

[^1]: https://www.prisma.io/docs/orm/prisma-client/deployment/serverless/deploy-to-aws-lambda
[^2]: https://www.prisma.io/docs/guides/deployment/deployment-guides/deploying-to-aws-lambda

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