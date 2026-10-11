from app.chat.models import ChatArgs
from app.chat.vector_stores.pinecone import build_retriever
from langchain_core.runnables.history import RunnableWithMessageHistory
from app.chat.memories.sql_memory import get_session_history
from app.chat.rag.rag_chain import rag_chain
from app.chat.chat_chains.traceable import TraceableRunnableWithHistory
from app.chat.tracing.langfuse import langfuse 

# from langfuse.model import CreateTrace :   OLD VERSION

def build_chat(chat_args: ChatArgs):
    """
    :param chat_args: ChatArgs object containing
        conversation_id, pdf_id, metadata, and streaming flag.

    :return: A chain

    Example Usage:

        chain = build_chat(chat_args)
    """
    # retriever = build_retriever(chat_args)
    # llm = build_llm(chat_args)
    # memory = build_memory(chat_args)


    # THE OLD VERSION : 
    # trace = langfuse.trace(
    #     CreateTrace(
    #         id=chat_args.conversation_id,
    #         metadata=chat_args.metadata
    #     )
    # )

    chat_chain = TraceableRunnableWithHistory(
        rag_chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="history",
       langfuse=langfuse,
    )
    


    # chat_chain = RunnableWithMessageHistory(
    #     rag_chain,
    #     get_session_history,
    #     input_messages_key="question",
    #     history_messages_key="history",
    #     # callbacks=[trace.getNewHandler()] THE OLD WAY 
    # )
    return chat_chain


    # *******THE OLD WAY **************
    # return ConversationalRetrievalChain.from_llm(
    #     llm=llm,
    #     memory=memory,
    #     retriever=retriever
    # )

    
