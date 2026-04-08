# AWS Deployment Guide

This document outlines the steps to deploy the frontend to AWS.

## Prerequisites

- Deploy the backend as described [here](../../backend/infra/README.md). You will find a Lambda Function URL in the output. You will need this when you export the frontend.
- Install [pnpm](https://pnpm.io/)
- Install the [AWS Cloud Development Kit (CDK)](https://docs.aws.amazon.com/cdk/v2/guide/home.html)
- Setup security credentials for CDK, e.g. by installing [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) and running `aws login`
- Navigate to the `frontend/app` directory and export the application to a static website with

  ```bash
  cd ../app
  pnpm install
  export NEXT_PUBLIC_API_URL=<lambda-function-url-from-backend-deployment>
  pnpm build
  ```

## Install dependencies

Install dependencies with:

```bash
pnpm install
```

## Deployment

Deploy to an AWS account with:

```bash
npm cdk deploy
```
