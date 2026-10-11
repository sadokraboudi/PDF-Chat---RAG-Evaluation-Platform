from langchain_google_genai import ChatGoogleGenerativeAI

def build_llm_from_gemini(model_name : str) : 
    return ChatGoogleGenerativeAI(
        model=model_name,  
        temperature=0
    )

