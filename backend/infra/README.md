# AWS Deployment Guide

This document outlines the steps to deploy the backend to AWS.

## Prerequisites

- Install [uv](https://github.com/astral-sh/uv)
- Create an API from Groq [here](https://console.groq.com/)
- Create an API from OpenAI [here](https://platform.openai.com/login?next=%2Fsettings%2Forganization%2Fapi-keys)
- Install [Docker](https://www.docker.com/get-started/)
- Install the [AWS Cloud Development Kit (CDK)](https://docs.aws.amazon.com/cdk/v2/guide/home.html)
- Setup security credentials for CDK, e.g. by installing [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) and running `aws login`

## Install dependencies

Install dependencies with:

```bash
uv sync
```

## Deployment

Deploy to an AWS account with:

```bash
uv run cdk deploy
```

Navigate to Secret Manager in the AWS console and enter the API keys 
created earlier for GroqApiKeySecret and OpenAiApiKeySecret.