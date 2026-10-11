# PDF Chat & RAG Evaluation Platform

A Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents, ask questions about their content, and evaluate different combinations of retrievers and Large Language Models (LLMs).

The application uses Flask and LangChain for the backend and RAG pipeline, Celery for asynchronous PDF processing, Pinecone for vector storage, and Google Gemini embeddings for semantic search.

## Features

- **PDF Upload and Processing:** Extract text from PDFs and split it into smaller chunks.
- **Asynchronous Processing:** Use Celery workers to process PDFs and generate embeddings in the background.
- **Semantic Search:** Generate embeddings with Google Gemini and store document vectors in Pinecone.
- **Conversational RAG:** Use conversation history to rewrite questions into standalone queries for improved retrieval.
- **Context-Aware Answers:** Generate answers using relevant document chunks and conversation context.
- **Multiple Conversations:** Create multiple independent conversations for the same PDF, each with its own conversation ID.
- **Configurable Retrieval:** Adjust retrieval settings, including the minimum and maximum number of retrieved document chunks.
- **Multiple LLMs:** Select and compare different language models.
- **User Feedback:** Like or dislike conversations to provide evaluation scores.
- **RAG Configuration Evaluation:** Use collected feedback to compare and promote promising retriever–LLM combinations.

## Technology Stack

| Technology                   | Purpose                                                           |
| ---------------------------- | ----------------------------------------------------------------- |
| Python                       | Core application language                                         |
| Flask                        | Backend API and application server                                |
| LangChain                    | RAG pipeline and chain composition                                |
| Celery                       | Asynchronous PDF processing and embedding tasks                   |
| Redis                        | Celery message broker, if configured                              |
| SQLite                       | Relational database for conversation history and application data |
| Pinecone                     | Vector database for semantic search                               |
| Google Gemini Embeddings     | Generate embeddings for document chunks and search queries        |
| Large Language Models (LLMs) | Rewrite questions and generate context-aware answers              |
| Frontend framework           | Svelte                                                            |

### 1. PDF Processing Pipeline

When a user uploads a PDF:

1. Flask receives the upload and queues a background task.
2. Celery processes the PDF asynchronously.
3. The worker extracts the text and splits it into chunks.
4. Google Gemini generates embeddings for the chunks.
5. The embeddings and associated document information are stored in Pinecone.

### 2. Conversational RAG Pipeline

When a user submits a question, the application follows these steps:

1. **Load conversation history:** Retrieve the relevant conversation history from SQLite using the conversation ID.
2. **Rewrite the question:** Combine the user's current question with the conversation history and send it to an LLM to generate a standalone search query.
3. **Generate query embeddings:** Convert the rewritten query into an embedding using Google Gemini.
4. **Retrieve relevant documents:** Search Pinecone for document chunks relevant to the query.
5. **Prepare the context:** Combine the original question, conversation history, and retrieved document chunks using the configured prompt or chain.
6. **Generate the answer:** Send the prepared context to the selected LLM to generate a response.
7. **Update conversation history:** Save the new user question and assistant response in the conversation history.
8. **Return the response:** Send the generated answer back to the client.

This process allows the application to understand follow-up questions while retrieving information relevant to the uploaded PDF.

### Conversational RAG Flow

```text
User Question
      |
      v
Load Conversation History
      |
      v
Question + Conversation History
      |
      v
LLM Query Rewriting
      |
      v
Rewritten Search Query
      |
      v
Google Gemini Embeddings
      |
      v
Pinecone Similarity Search
      |
      v
Retrieved Document Chunks
      |
      v
Original Question + History + Retrieved Context
      |
      v
Prompt / LangChain Pipeline
      |
      v
Selected LLM
      |
      v
Generated Answer
      |
      v
Update Conversation History in SQLite
      |
      v
Return Answer to Client
```

### 3. Feedback and Evaluation

Users can provide positive or negative feedback on conversations. The application records these scores and uses them to help compare different retriever and LLM configurations.

The objective is to identify and promote promising configurations based on collected feedback. The results depend on the scoring methodology and the amount and quality of feedback available.

## Getting Started

### Prerequisites

- Python
- Pipenv
- Redis, if required by the Celery configuration
- A Pinecone account and configured index
- Google Gemini API credentials
- Credentials for any additional LLM providers used by the application

### 1. Clone the Repository

### 2. Install Dependencies

Install the project dependencies using Pipenv:

```bash
pipenv install
```

### 3. Configure Environment Variables

### 4. Initialize the Database

Run the following command from the project root:

```bash
flask --app app.web init-db
```

### 5. Start the Flask Server

Open a terminal in the project directory and activate the Pipenv environment:

```bash
pipenv shell
```

Start the development server:

```bash
inv dev
```

### 6. Start the Celery Worker

Open a second terminal in the same project directory and activate the Pipenv environment:

```bash
pipenv shell
```

Start the development worker:

```bash
inv devworker
```
