# class TraceableChain:
#     def  __call__(self, *args, **kwds):
#         return super().__call__(*args, **kwds)
from typing import Any

from langchain_core.runnables.history import RunnableWithMessageHistory


class TraceableRunnableWithHistory(RunnableWithMessageHistory):
    langfuse: Any = None
    trace_name: str = "chat-request"

    def invoke(self, input, config=None, **kwargs):
        metadata = (config or {}).get("metadata")
        with self.langfuse.start_as_current_observation(
            name=self.trace_name, as_type="span", input=input, metadata=metadata
        ) as observation:
            result = super().invoke(input, config, **kwargs)
            observation.update(output=result)
            return result

    def stream(self, input, config=None, **kwargs):
        metadata = (config or {}).get("metadata")
        with self.langfuse.start_as_current_observation(
            name=self.trace_name, as_type="span", input=input, metadata=metadata
        ) as observation:
            for chunk in super().stream(input, config, **kwargs):
                yield chunk
            observation.update(output={"status": "completed"})

    def __call__(self, input, config=None, **kwargs):
        return self.invoke(input, config=config, **kwargs)