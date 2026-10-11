from flask import Blueprint, g, request, Response, jsonify, stream_with_context
from app.web.hooks import login_required, load_model
from app.web.db.models import Pdf, Conversation
from app.chat import build_chat, ChatArgs
from app.chat.logs.timing import timed
from langfuse import propagate_attributes
from app.chat.tracing.langfuse import  langfuse_handler

bp = Blueprint("conversation", __name__, url_prefix="/api/conversations")


@bp.route("/", methods=["GET"])
@login_required
@load_model(Pdf, lambda r: r.args.get("pdf_id"))
def list_conversations(pdf):
    return [c.as_dict() for c in pdf.conversations]


@bp.route("/", methods=["POST"])
@login_required
@load_model(Pdf, lambda r: r.args.get("pdf_id"))
def create_conversation(pdf):
    conversation = Conversation.create(user_id=g.user.id, pdf_id=pdf.id)

    return conversation.as_dict()


@bp.route("/<string:conversation_id>/messages", methods=["POST"])
@login_required
@load_model(Conversation)
def create_message(conversation):
    input = request.json.get("input")
    streaming = request.args.get("stream", False)

    pdf = conversation.pdf

    chat_args = ChatArgs(
        conversation_id=conversation.id,
        pdf_id=pdf.id,
        streaming=streaming,
        metadata={
            "conversation_id": conversation.id,
            "user_id": g.user.id,
            "pdf_id": pdf.id,
        },
    )

    chat = build_chat(chat_args)

    if not chat:
        return "Chat not yet implemented!"

    config = {
    "callbacks": [langfuse_handler],
    "configurable": {
        "session_id": chat_args.conversation_id,
        "metadata":chat_args.metadata
    }
}

    chat_input = {
        "question": input,
        "chat_args": chat_args,
    }

    # print(langfuse.auth_check())
    if streaming:
        return Response(
            stream_with_context(chat.stream(chat_input, config=config)),
            mimetype="text/event-stream",
        )

    with timed("TOTAL chat.invoke"):
        result = chat.invoke(chat_input, config=config)

    return jsonify({"role": "assistant", "content": result})


# WITHOUT TRACEBALE CLASS
    # if streaming:
    #     def generate():
    #         with langfuse.start_as_current_observation(
    #             name="chat-request",
    #             as_type="span",
    #             input=chat_input,
    #             metadata=chat_args.metadata,
    #         ) as observation:
    #             for chunk in chat.stream(chat_input, config=config):
    #                 yield chunk

    #             observation.update(
    #                 output={"status": "completed"}
    #             )

    #     return Response(
    #         stream_with_context(generate()),
    #         mimetype="text/event-stream",
    #     )

    # else:
    #     with timed("TOTAL chat.invoke"):
    #         with langfuse.start_as_current_observation(
    #             name="chat-request",
    #             as_type="span",
    #             input=chat_input,
    #             metadata=chat_args.metadata,
    #         ) as observation:
    #             result = chat.invoke(
    #                 chat_input,
    #                 config=config,
    #             )

    #             observation.update(output=result)

    #     return jsonify({"role": "assistant", "content": result })



    # if streaming:
    #     def generate():
    #         for chunk in chat.stream(chat_input, config=config):
    #             yield chunk

    #     return Response(
    #         stream_with_context(generate()),
    #         mimetype="text/event-stream",
    #     )
    # else:
    #     with timed("TOTAL chat.invoke"):
    #        result= chat.invoke(
    #         chat_input,
    #         config=config
    #         )
    #     return jsonify({"role": "assistant", "content": result })



# # ANOTHER WAY TO INTEGRATE LANGFUSE : 

# if streaming:
#     def generate():
#         with propagate_attributes(
#             session_id=str(chat_args.conversation_id),
#             metadata=chat_args.metadata,
#         ):
#             with langfuse.start_as_current_observation(
#                 name="chat-request",
#                 as_type="span",
#                 input=chat_input,
#             ) as observation:
#                 for chunk in chat.stream(
#                     chat_input,
#                     config=config,
#                 ):
#                     yield chunk

#                 observation.update(
#                     output={"status": "completed"}
#                 )

#     return Response(
#         stream_with_context(generate()),
#         mimetype="text/event-stream",
#     )

# else:
#     with propagate_attributes(
#         session_id=str(chat_args.conversation_id),
#         metadata=chat_args.metadata,
#     ):
#         with langfuse.start_as_current_observation(
#             name="chat-request",
#             as_type="span",
#             input=chat_input,
#         ) as observation:
#             with timed("TOTAL chat.invoke"):
#                 result = chat.invoke(
#                     chat_input,
#                     config=config,
#                 )

#             observation.update(output=result)

#     return result
