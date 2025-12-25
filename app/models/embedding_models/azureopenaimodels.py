from azure.identity import DefaultAzureCredential,get_bearer_token_provider
from langchain_openai import AzureOpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
azureopenai_embedding_model= AzureOpenAIEmbeddings(
    api_version="2024-12-01-preview",
    azure_endpoint="https://az-genai-3016-resource.openai.azure.com/",
    azure_ad_token_provider= token_provider,
    model= "text-embedding-ada-002"
    )

response = azureopenai_embedding_model.embed_query("what is langchain?")
print(response)
 