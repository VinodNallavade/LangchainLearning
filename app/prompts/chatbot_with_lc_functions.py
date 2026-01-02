from langchain_openai import AzureChatOpenAI
from azure.identity import DefaultAzureCredential,get_bearer_token_provider
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
import os

load_dotenv()
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
model_name = os.getenv("AZURE_OPENAI_MODEL_NAME")   
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

llm= AzureChatOpenAI(
    deployment_name=deployment_name,
    model_name=model_name,
    azure_endpoint=azure_endpoint,
    api_version="2024-12-01-preview",
    azure_ad_token_provider= token_provider
    )

sys_message = SystemMessage(content="You are a helpful assistant that provides concise and accurate information.")
#human_message = HumanMessage(content="Explain the concept of reinforcement learning.")
#response = llm.invoke([sys_message, human_message])
#print(response.content)

print("---------- Generated response ----------")
while True:
    input_text = input("User: ")
    if input_text.lower() in ["exit", "quit"]:
        break       
    human_msg = HumanMessage(content=input_text)
    response = llm.invoke([sys_message, human_msg]) 
    print("AI: ", response.content)

print("Chat ended.")
print("Conversation History:")
print("System: ", sys_message.content)
print("User: ", human_msg.content)      