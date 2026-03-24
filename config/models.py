import os
from dotenv import load_dotenv

# Try to load .env from root first, then from venv/ as a fallback
if not load_dotenv():
    load_dotenv("venv/.env")

from langchain_aws import BedrockEmbeddings , ChatBedrockConverse

embeddings = BedrockEmbeddings(
    model_id=os.getenv("BEDROCK_EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0"),
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
)
llm = ChatBedrockConverse(
    model_id=os.getenv("BEDROCK_MODEL_ID", "global.anthropic.claude-haiku-4-5-20251001-v1:0"),
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
)

# git checkout -b feat/calender
