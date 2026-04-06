"""GameSession persistence for game sessions."""

import json
from dataclasses import asdict
from src.adapters.cache.cache_provider import get_cache_path
from src.model.chat_message import (
    ChatMessage,
    SystemChatMessage,
    UserChatMessage,
    AssistantChatMessage,
    ToolChatMessage,
    ToolCall,
)
from src.model.game_session import GameSession
from src.model.npc import Npc


def read_session(session_token: str) -> GameSession | None:
    """Loads a session by its token."""

    json_path = get_cache_path(f"{session_token}.json")

    if not json_path.exists():
        return None

    session_dict = json.loads(json_path.read_text())

    for npc_name, npc_dict in session_dict["npcs_by_name"].items():
        image_path = get_cache_path(f"{session_token}_{npc_name}.png")
        npc_dict["image"] = image_path.read_bytes()
        npc_dict["chat_history"] = [
            deserialize_chat_message(msg) for msg in npc_dict["chat_history"]
        ]
        session_dict["npcs_by_name"][npc_name] = Npc(**npc_dict)

    session_dict["log"] = [
        [deserialize_chat_message(msg) for msg in msgs] for msgs in session_dict["log"]
    ]

    return GameSession(**session_dict)


def write_session(session_token: str, session: GameSession) -> None:
    """Saves a session by its token."""

    session_dict = asdict(session)

    for npc_name, npc_dict in session_dict["npcs_by_name"].items():
        image = npc_dict.pop("image")
        get_cache_path(f"{session_token}_{npc_name}.png").write_bytes(image)

    get_cache_path(f"{session_token}.json").write_text(
        json.dumps(session_dict, indent=2)
    )


def deserialize_chat_message(data: dict) -> ChatMessage:
    """Deserializes a chat message from dict."""
    role = data["role"]
    if role == "system":
        return SystemChatMessage(**data)
    elif role == "user":
        return UserChatMessage(**data)
    elif role == "assistant":
        tool_calls = [ToolCall(**tc) for tc in data["tool_calls"]]
        return AssistantChatMessage(
            role=role, content=data["content"], tool_calls=tool_calls
        )
    elif role == "tool":
        return ToolChatMessage(**data)
    else:
        raise ValueError(f"Unknown role {role}")
