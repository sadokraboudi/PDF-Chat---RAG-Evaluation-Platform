from langchain_core.prompts import (ChatPromptTemplate , MessagesPlaceholder)

rewrite_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a query rewriting assistant for a document retrieval system.

Your job is to rewrite the user's latest question into a
standalone search query that can be used to search a vector database.

Use the conversation history to resolve references such as:
- "it"
- "this"
- "that"
- "the first one"
- "the previous concept"

Do NOT answer the question.

Return ONLY the search query.
"""
    ),

    MessagesPlaceholder("history"),

    (
        "human",
        "{question}"
    ),
])