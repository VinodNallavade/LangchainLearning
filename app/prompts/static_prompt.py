from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import os
from azure.identity import DefaultAzureCredential,get_bearer_token_provider
load_dotenv()
tokenprovider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
model = os.getenv("AZURE_OPENAI_MODEL_NAME")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

llm=  AzureChatOpenAI(
    deployment_name=deployment,
    model_name=model,
    azure_endpoint=azure_endpoint,
    api_version="2024-12-01-preview",
    azure_ad_token_provider= tokenprovider
)
response = llm.invoke("Explain the theory of relativity in simple terms.")
print(response)