import streamlit as st
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate,load_prompt

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

# ------------------- Page Config -------------------
st.set_page_config(
    page_title="Travel Planner",
    page_icon="🌍",
    layout="centered"
)

# ------------------- Custom CSS -------------------
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #667eea, #764ba2);
}
.main {
    background-color: #ffffffcc;
    padding: 25px;
    border-radius: 15px;
}
h1 {
    color: #4B0082;
    text-align: center;
}
h3 {
    color: #2F4F4F;
}
.stButton > button {
    background-color: #ff7f50;
    color: white;
    border-radius: 10px;
    height: 3em;
    font-size: 18px;
}
.stButton > button:hover {
    background-color: #ff6347;
}
</style>
""", unsafe_allow_html=True)

# ------------------- UI -------------------
st.markdown("<h1>🌍 Travel Plan Generator</h1>", unsafe_allow_html=True)

st.write("Choose your preferences to generate a personalized travel plan ✨")

# City Selection
city_name = st.selectbox(
    "🏙️ Select City",
    ["Paris", "New York", "Tokyo", "Rome", "Dubai", "Bangkok", "Sydney","India"]
)

# Interests
interest = st.multiselect(
    "🎯 Select Your Interests",
    ["Adventure", "Culture", "Food", "Nature", "Shopping", "History", "Relaxation"]
)

# Stay Duration
stay_duration = st.slider(
    "📅 Length of Stay (Days)",
    min_value=1,
    max_value=30,
    value=5
)

# Budget
budget = st.selectbox(
    "💰 Budget Type",
    ["Low", "Medium", "Luxury"]
)

'''
if st.button("✈️ Generate Travel Prompt"):
    if not interest:
        st.warning("Please select at least one interest.")
    else:
        interest_text = ", ".join(interest)
        # This is with f-string, which is not recommended for production use.
        travel_prompt = f"""
            Create a travel plan for someone visiting {city_name}, 
            interested in {interest_text}, 
            staying for {stay_duration} days, 
            and having a {budget} budget.
            Don't ask for more information. Just provide the travel plan and Avoid asking for printing or format change or any other things.
            """
        
        # using Prompt Template (recommended for production use)
        travel_prompt_template = load_prompt("./prompt_generator.json")
        prompt = travel_prompt_template.invoke(input={"city_name": city_name, "interest": interest_text, "stay_duration": stay_duration, "budget": budget})

        #travel_prompt_template = PromptTemplate.from_file(template_file=  "./prompt_generator.json",encoding="utf-8")
        #print(travel_prompt_template.invoke(input={"name": city_name, "interest": interest_text, "stay_duration": stay_duration, "budget": budget}))


    with st.spinner("Generating Plan..."):       
       # response = llm.invoke(travel_prompt.format(city_name=city_name, interest=interest_text, stay_duration=stay_duration, budget=budget))
        response = llm.invoke(prompt)
        st.subheader("Travel Plan")
        st.write(response.content)
  '''     

if st.button("✈️ Generate Travel Prompt"):
    if not interest:
        st.warning("Please select at least one interest.")
    else:
        interest_text = ", ".join(interest)
        # using Prompt Template (recommended for production use)
        travel_prompt_template = load_prompt("./prompt_generator.json")
        
    with st.spinner("Generating Plan..."):       
        chain = travel_prompt_template |llm
        response = chain.invoke({ "city_name": city_name, "interest": interest_text, "stay_duration": stay_duration, "budget": budget})
        st.subheader("Travel Plan")
        st.write(response.content)