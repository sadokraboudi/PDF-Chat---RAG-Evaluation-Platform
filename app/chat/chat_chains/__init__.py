from app.chat.prompts import answer_prompt , rewrite_prompt
# from app.chat.llms.chatgemini import build_llm_from_gemini
from langchain_core.output_parsers import StrOutputParser
# from app.chat.logs.timing import timed
from app.chat.llms import llm_map

# llm = build_llm_from_gemini()
builder = llm_map["gemini-3.1-flash-lite"]
llm = builder()
def build_answer_chain( answer_prompt = answer_prompt):
    return answer_prompt | llm | StrOutputParser()

def build_rewrite_chain (rewrite_prompt = rewrite_prompt):
    return rewrite_prompt | llm | StrOutputParser()

