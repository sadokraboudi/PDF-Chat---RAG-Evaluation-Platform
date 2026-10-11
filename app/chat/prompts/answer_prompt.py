from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder

answer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a helpful assistant answering questions about a PDF.

Use the retrieved document context to answer the user's question.

Use the conversation history to understand references
and maintain continuity.

If the answer cannot be found in the provided context,
say that you don't have enough information.

Do not invent information.
And answer directly without based on the provided document or something like that 

Retrieved context:

{context}
"""
    ),

    MessagesPlaceholder("history"),

    (
        "human",
        "{question}"
    ),
])