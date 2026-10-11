# import os 
# from langfuse.client import Langfuse

# langfuse = Langfuse(
#     os.environ["LANGFUSE_PUBLIC_KEY"],
#     os.environ["LANGFUSE_SECRET_KEY"],
#     host=os.environ["LANGFUSE_BASE_URL"]
# )
from langfuse.langchain import CallbackHandler
from langfuse import get_client, Langfuse
# from dotenv import load_dotenv
# load_dotenv()

# Langfuse(
#     public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
#     secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
#     host=os.getenv("LANGFUSE_HOST") or os.getenv("LANGFUSE_BASE_URL"),
# )
langfuse = get_client()
langfuse_handler = CallbackHandler()

