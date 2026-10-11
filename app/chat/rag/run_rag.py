import random
from app.chat.chat_chains import build_rewrite_chain ,build_answer_chain
# from app.chat.vector_stores.pinecone import build_retriever
from app.chat.vector_stores import retriever_map
from app.chat.logs.timing import timed
from app.web.api import (
    set_conversation_components,
    get_conversation_components
   )
from app.chat.score import random_component_by_score



def select_component(
        component_type,
        component_map,
        chat_args
) :
    components = get_conversation_components(
        chat_args.conversation_id
    )
    previous_component = components[component_type]

    if previous_component:
        builder = component_map[previous_component]
        return previous_component , builder(chat_args)
    else: 
        random_name = random_component_by_score(component_type , component_map)
        builder = component_map[random_name]
        return random_name , builder(chat_args)
        # random_name = random.choice(list(component_map.keys()))
        # builder = component_map[random_name]
        # return random_name , builder(chat_args)




def run_rag(question: str, history, chat_args):


    rewrite_chain = build_rewrite_chain()
    with timed("1. rewrite query (LLM)"):
        rewrite_search_query = rewrite_chain.invoke({
            "history": history,
            "question": question,
        })




    with timed("2.creating of the retriever"):
        # retriever = build_retriever(chat_args)
        retriever_name, retriever = select_component(
            "retriever",
            retriever_map,
            chat_args
        )

        print(
            f"*****Running chain  with retriever : {retriever_name}"
        )
        set_conversation_components(
                conversation_id= chat_args.conversation_id,
                llm="gemini-3.1-flash-lite",
                retriever=retriever_name
            )

    with timed("3. embed + vector search"):
        documents = retriever.invoke(rewrite_search_query)


    with timed("4. formating docs"):
        context = "\n\n".join(
            document.page_content
            for document in documents
        )
    print("context chars:", len(context))




    answer_chain = build_answer_chain()
    # with timed("5. final answer (LLM)"):
    if chat_args.streaming:
        print(chat_args.streaming)
        for chunk in answer_chain.stream({
                "history": history,
                "context": context,
                "question": question,
            }):
                yield chunk
    else:     
        with timed("5. final answer (LLM)"):
            answer_result = answer_chain.invoke({
                "history": history,
                "context": context,
                "question": question,
            })
        yield answer_result


