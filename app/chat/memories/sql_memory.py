from pydantic import BaseModel
from langchain_core.messages import BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory
# from langchain_core.runnables.history import RunnableWithMessageHistory

from app.web.api import (
    get_messages_by_conversation_id,
    add_message_to_conversation
)
# class SqlMessageHistory(BaseChatMessageHistory,BaseModel):
class SqlMessageHistory(BaseChatMessageHistory):

    def __init__(self, conversation_id: str, max_messages: int = 100):
        self.conversation_id = conversation_id
        self.max_messages = max_messages

    @property
    def messages(self) -> list[BaseMessage]:
        return get_messages_by_conversation_id(self.conversation_id)

    def add_message(self,  message : BaseMessage):
        return add_message_to_conversation(
            conversation_id=self.conversation_id,
            role= message.type,
            content= message.content
        )
    def clear(self):
        pass


def get_session_history(session_id:str) -> SqlMessageHistory:
    return SqlMessageHistory(conversation_id = session_id)


# def build_memory(chat_args):
#     return  RunnableWithMessageHistory (
#         chat_memory=SqlMessageHistory(conversation_id = chat_args.conversation_id)
#     )











# ***********NB:
# Not a "FileMemory" class. The old ConversationBufferMemory-style memory classes are deprecated. In the new version, the base class is BaseChatMessageHistory from langchain_core.chat_history. FileChatMessageHistory and SQLChatMessageHistory are just implementations of it. You only need three members:

# messages (a property) returns the stored messages as LangChain message objects.
# add_messages(messages) saves new messages. RunnableWithMessageHistory calls it after each turn with the user question and the AI answer.
# clear() deletes the session's history.















# RunnableWithMessageHistory
#   │
#   ├── get conversation history
#   │
#   ↓
# rag_chain
#   │
#   ├── retrieve documents
#   ├── construct prompt
#   └── call LLM
#   │
#   ↓
# RunnableWithMessageHistory
#   │
#   └── update history