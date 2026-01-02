import streamlit as st
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


st.set_page_config(page_title="Story Generate", layout="wide")

# Custom CSS for colors
st.markdown("""
<style>
/* Background */
.stApp {
    background: linear-gradient(to right, #fbc2eb, #a6c1ee);
}

/* Sidebar background */
section[data-testid="stSidebar"] {
    background-color: #2c3e50;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: white;
}

/* Text input styling */
input[type="text"] {
    background-color: #fff4e6 !important;
    color: #2c3e50 !important;
    border-radius: 10px !important;
    border: 2px solid #ff9f43 !important;
}

/* Dropdown styling */
div[data-baseweb="select"] > div {
    background-color: #34495e;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🎨 Sidebar Controls")

option1 = st.sidebar.selectbox("Choose Color", ["Red", "Blue", "Green"])
option2 = st.sidebar.selectbox("Choose Animal", ["Cat", "Dog", "Elephant"])
option3 = st.sidebar.selectbox("Choose City", ["New York", "London", "Tokyo"])

# Main content
st.title("🌈 Dynamic Story Generator with AI")


text = st.text_input("Type something here")

if st.button("Generate Response"):
    with st.spinner("Generating story..."):
        prompt = f"""Generate a creative story involving the color {option1}, a {option2}, and the city {option3}. Please consider the 
        following input: {text}"""
        response = llm.invoke(prompt)
       # response = llm.invoke(text)
        st.subheader("Generated Story")
        st.write(response.content)