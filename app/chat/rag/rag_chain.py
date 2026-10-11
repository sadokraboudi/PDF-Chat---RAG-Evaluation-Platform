from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory
from app.chat.memories.sql_memory import get_session_history
from app.chat.rag.run_rag import run_rag

# # BEFORE
# rag_chain = RunnableLambda(
#     lambda inputs: run_rag(inputs["question"], inputs["history"], chat_args)
# )

# # AFTER
def rag_step(inputs):
    yield from run_rag(inputs["question"], inputs["history"], chat_args = inputs["chat_args"])

rag_chain = RunnableLambda(rag_step)


# rag_chain = RunnableLambda(
#     lambda inputs: run_rag(
#         inputs["question"],
#         inputs["history"],
#         chat_args = inputs["chat_args"]

#     )
# )
