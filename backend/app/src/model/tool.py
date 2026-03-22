"""Representation of a tool that an AI agent can use."""

from dataclasses import dataclass
from typing import Callable


@dataclass
class ToolArgument:
    """Represents an argument for a tool."""

    name: str
    description: str


@dataclass
class ToolSpec:
    """Represents the specification of a tool that an agent can use."""

    name: str
    description: str
    arguments: list[ToolArgument]


@dataclass
class Tool:
    """Represents a tool that an agent can use."""

    spec: ToolSpec
    function: Callable[..., str]
