from typing import TypedDict, Any


class PayloadMessage(TypedDict):
    chat_id: int
    message_id: int
    payload: Any
