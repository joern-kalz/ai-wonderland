FROM public.ecr.aws/lambda/python:3.12 AS builder

COPY --from=ghcr.io/astral-sh/uv:0.11.3 /uv /uvx /bin/

WORKDIR /build

COPY pyproject.toml uv.lock ./
RUN uv pip install --no-cache --system -r pyproject.toml --target /packages


FROM public.ecr.aws/lambda/python:3.12

COPY --from=builder /packages ${LAMBDA_RUNTIME_DIR}

COPY src/ ${LAMBDA_TASK_ROOT}/src/

CMD [ "src.lambda_main.handler" ]