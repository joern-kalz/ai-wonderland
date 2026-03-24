"""GameSession persistence for game sessions."""

import json
import os
from dataclasses import asdict
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

    json_path = os.path.join(_cache_dir, f"{session_token}.json")

    if not os.path.exists(json_path):
        return None

    with open(json_path, "r") as f:
        session_dict = json.load(f)

    for npc_name, npc_dict in session_dict["npcs_by_name"].items():
        image_path = os.path.join(_cache_dir, f"{session_token}_{npc_name}.png")
        if os.path.exists(image_path):
            with open(image_path, "rb") as f:
                npc_dict["image"] = f.read()
        else:
            npc_dict["image"] = b""

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

    os.makedirs(_cache_dir, exist_ok=True)
    session_dict = asdict(session)

    for npc_name, npc_dict in session_dict["npcs_by_name"].items():
        image = npc_dict.pop("image")
        with open(
            os.path.join(_cache_dir, f"{session_token}_{npc_name}.png"), "wb"
        ) as f:
            f.write(image)

    with open(os.path.join(_cache_dir, f"{session_token}.json"), "w") as f:
        json.dump(session_dict, f, indent=2)


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


_module_dir = os.path.dirname(__file__)
_cache_dir = os.path.join(_module_dir, ".cache")
