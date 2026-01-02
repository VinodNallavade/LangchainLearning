
"""
Azure OpenAI Chatbot Module
This module implements an interactive chatbot using LangChain and Azure OpenAI.
It establishes a connection to Azure OpenAI using Azure AD authentication and 
maintains a conversation history throughout the chat session.
The chatbot:
- Authenticates using Azure DefaultAzureCredential and bearer token provider
- Loads configuration from environment variables (.env file)
- Initiates a multi-turn conversation loop with the user
- Maintains message history in the format required by the LLM
- Accepts user input until 'exit' or 'quit' is entered
- Displays AI responses in real-time
- Prints the complete conversation history at the end of the session
Environment Variables Required:
    AZURE_OPENAI_MODEL_NAME: The model identifier (e.g., 'gpt-4')
    AZURE_OPENAI_DEPLOYMENT_NAME: Azure deployment name
    AZURE_OPENAI_ENDPOINT: Azure OpenAI endpoint URL
Author: vnallava
"""
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from langchain_openai import AzureChatOpenAI

load_dotenv()
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
model_name = os.getenv("AZURE_OPENAI_MODEL_NAME")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME") 
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

llm = AzureChatOpenAI(
    deployment_name=deployment_name,    
    model_name=model_name,
    azure_endpoint=azure_endpoint,
    api_version="2024-12-01-preview",
    azure_ad_token_provider=token_provider
)
message = []
while True:
    user_input = input("User: ")
    message.append({"role": "user", "content": user_input})
    if user_input.lower() in ["exit", "quit"]:
        break
    response = llm.invoke(message)
    message.append({"role": "assistant", "content": response.content})
    print("AI: ", response.content)


print("Chat ended.")
print("Conversation History:")
for msg in message:
    role = msg["role"]
    content = msg["content"]
    print(f"{role.capitalize()}: {content}")
