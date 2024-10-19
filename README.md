# AWS Serverless Application Model (SAM) Guide

## Introduction to AWS SAM

AWS Serverless Application Model (SAM) is an open-source framework for building serverless applications on AWS. It simplifies the process of defining Amazon API Gateway APIs, AWS Lambda functions, and Amazon DynamoDB tables for your serverless applications. It provides developers with a powerful set of tools and abstractions to streamline the development, testing, and deployment of serverless solutions. Basically, it is another layer of abstraction on top of CloudFormation.

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

## AWS SAM Quick Start Templates

When initializing a new SAM project using `sam init`, you're presented with several Quick Start template options. Each template is designed for specific use cases and provides a starting point for different types of serverless applications. Here's a breakdown of each option:

![AWS SAM Quick Start Templates](./Screenshot%202024-10-19%20at%201.20.35%20AM.png)

1. **Hello World Example**
   - A basic Lambda function that returns a "Hello World" message.
   - **When to use**: Ideal for beginners or when you want to quickly test SAM setup and deployment process.

2. **Data processing**
   - Sets up a Lambda function triggered by S3 events to process data.
   - **When to use**: When you need to perform operations on files as soon as they're uploaded to S3, like image resizing or log analysis.

3. **Hello World Example with Powertools for AWS Lambda**
   - Similar to the basic Hello World example, but includes AWS Lambda Powertools for enhanced observability and best practices.
   - **What are AWS Lambda Powertools?**
     - Powertools is a suite of utilities for AWS Lambda functions that simplifies the adoption of best practices such as tracing, structured logging, custom metrics, and more.
     - It includes libraries for multiple languages (Python, Java, TypeScript) and integrates seamlessly with AWS services like CloudWatch, X-Ray, and CloudFormation.
   - **Key features of Powertools:**
     - Structured logging: Standardizes log formats for better searchability and analysis.
     - Tracing: Enhances distributed tracing with AWS X-Ray.
     - Metrics: Allows creation of custom metrics easily.
     - Parameter retrieval: Simplifies fetching configuration from AWS Systems Manager Parameter Store or Secrets Manager.
     - Idempotency: Helps in implementing idempotent Lambda functions.
   - **When to use**: When you want to implement best practices for observability and operations in your Lambda functions from the start.

4. **Multi-step workflow**
   - Creates a Step Functions state machine with multiple Lambda functions.
   - **When to use**: For complex, multi-step processes that require coordination between different services or tasks.

5. **Scheduled task**
   - Sets up a Lambda function that runs on a schedule using EventBridge rules. Basically, it is a cron job!
   - **When to use**: For periodic tasks like daily reports, backups, or maintenance jobs.

6. **Standalone function**
   - Provides a basic Lambda function without any triggers or additional resources.
   - **When to use**: When you need a simple function that will be triggered manually or integrated into other services later.

7. **Serverless API**
   - Creates an API Gateway with Lambda backend.
   - **When to use**: When building RESTful APIs or web services that need to scale automatically.

8. **Infrastructure event management**
   - Sets up a system to respond to AWS infrastructure events.
   - **When to use**: For monitoring and reacting to changes in your AWS environment, like EC2 instance state changes.

9. **Lambda Response Streaming**
   - Implements a Lambda function that uses response streaming.
   - **When to use**: When you need to return large responses or stream data back to the client in real-time.

10. **Serverless Connector Hello World Example**
    - Demonstrates the use of SAM Connectors for simplified resource permissions.
    - **When to use**: When you want to explore easier ways to manage permissions between AWS resources.

11. **Multi-step workflow with Connectors**
    - Combines Step Functions with SAM Connectors.
    - **When to use**: For complex workflows that require simplified permission management between different AWS services.

12. **GraphQLApi Hello World Example**
    - Sets up a GraphQL API using AppSync and Lambda.
    - **When to use**: When building applications that require flexible, efficient data querying capabilities.

13. **Full Stack**
    - Provides a complete stack including backend API and frontend web application.
    - **When to use**: When you need to quickly bootstrap a full-stack serverless application.

14. **Lambda EFS example**
    - Demonstrates how to use Amazon EFS with Lambda.
    - **When to use**: When your Lambda functions need access to a shared file system or require more storage than Lambda's default limits.

15. **DynamoDB Example**
    - Sets up a Lambda function with DynamoDB integration.
    - **When to use**: For building applications that need serverless, scalable database operations.

16. **Machine Learning**
    - Provides a template for deploying machine learning models on Lambda.
    - **When to use**: When you want to serve ML model predictions via a serverless API.

Choose the template that best fits your project requirements. You can always customize and expand upon these templates as your application grows.

## Building and Testing locally
Use SAM CLI commands to build and test your application locally:

1. **Build**:
   - `sam build`
   - This command compiles your application code and prepares it for deployment.

2. **Invoke**:
   - `sam invoke local`
   - This command invokes your Lambda function locally with the specified event payload.

3. **Start API**:
   - `sam local start-api`
   - This command starts an Amazon API Gateway locally and simulates API events for testing.

4. **Deploy**:
   - `sam deploy`
   - This command will package your application, upload it to S3, and deploy it to AWS using CloudFormation.

5. **Delete**:
   - `sam delete`
   - This command deletes your application from AWS.
