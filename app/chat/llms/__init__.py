from .chatgemini import build_llm_from_gemini
from functools import partial

llm_map = {
    "gemini-3.1-flash-lite": partial(build_llm_from_gemini, model_name = "gemini-3.1-flash-lite"),
    "gemini-2.5-flash":partial(build_llm_from_gemini, model_name="gemini-2.5-flash"),
    "gemini-2.5-flash-lite": partial(build_llm_from_gemini, model_name = "gemini-2.5-flash-lite")
}
# builder = llm_map["gemini-2.5-flash"]
# llm = builder()