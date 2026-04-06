from aws_cdk import (
    RemovalPolicy,
    Stack,
    aws_lambda as _lambda,
    aws_secretsmanager as secretsmanager,
    aws_s3 as s3,
    Duration,
    CfnOutput,
)
from constructs import Construct


class InfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        groq_secret = secretsmanager.Secret(
            self,
            "GroqApiKeySecret",
            secret_name="GroqApiKey",
            description="API key for Groq model access",
        )

        openai_secret = secretsmanager.Secret(
            self,
            "OpenAiApiKeySecret",
            secret_name="OpenAiApiKey",
            description="API key for OpenAI model access",
        )

        storage_bucket = s3.Bucket(
            self,
            "WonderlandStorageBucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        docker_func = _lambda.DockerImageFunction(
            self,
            "WonderlandDockerFunction",
            code=_lambda.DockerImageCode.from_image_asset("../app"),
            memory_size=1024,
            timeout=Duration.seconds(120),
            environment={
                "GROQ_SECRET_NAME": groq_secret.secret_name,
                "OPENAI_SECRET_NAME": openai_secret.secret_name,
                "S3_BUCKET": storage_bucket.bucket_name,
                "env": "aws",
            },
        )

        groq_secret.grant_read(docker_func)
        openai_secret.grant_read(docker_func)
        storage_bucket.grant_read_write(docker_func)

        func_url = docker_func.add_function_url(
            auth_type=_lambda.FunctionUrlAuthType.NONE,
            cors=_lambda.FunctionUrlCorsOptions(
                allowed_origins=["*"],
                allowed_methods=[_lambda.HttpMethod.ALL],
                allowed_headers=["*"],
            ),
        )

        CfnOutput(self, "FunctionUrl", value=func_url.url)
