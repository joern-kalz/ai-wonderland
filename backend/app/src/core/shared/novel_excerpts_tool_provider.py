"""List of tools for retrieving novel excerpts."""

from src.adapters.config.global_config_provider import is_on_aws
from src.core.shared.novel_excerpts_retriever import (
    get_novel_excerpts_for_keyword,
    get_novel_excerpts_for_question,
)
from src.model.tool import Tool, ToolArgument, ToolSpec


def _get_novel_excerpts_for_question(question: str) -> str:
    excerpts = get_novel_excerpts_for_question(question=question, limit=5)
    return _join_excerpts(excerpts)


def _get_novel_excerpts_for_keyword(keyword: str) -> str:
    excerpts = get_novel_excerpts_for_keyword(keyword=keyword, limit=5)
    return _join_excerpts(excerpts)


def get_novel_excerpts_tools() -> list[Tool]:
    if is_on_aws():
        return [_keyword_tool]
    else:
        return [_question_tool]


_question_tool = Tool(
    spec=ToolSpec(
        name="get_novel_excerpts",
        description="Retrieves excerpts from the novel Alice's Adventures in Wonderland. Use this tool when a new topic comes up in the conversation and you want to retrieve information about it from the novel.",
        arguments=[
            ToolArgument(
                name="question",
                description="The question to retrieve background information for",
            )
        ],
    ),
    function=_get_novel_excerpts_for_question,
)

_keyword_tool = Tool(
    spec=ToolSpec(
        name="get_novel_excerpts",
        description="Retrieves excerpts from the novel Alice's Adventures in Wonderland. Use this tool when a new topic comes up in the conversation and you want to retrieve information about it from the novel.",
        arguments=[
            ToolArgument(
                name="keyword",
                description="A single keyword to search for in the novel",
            )
        ],
    ),
    function=_get_novel_excerpts_for_keyword,
)


def _join_excerpts(excerpts):
    return "\n\n".join(
        f"**Excerpt {index + 1}**\n{excerpt}" for index, excerpt in enumerate(excerpts)
    )
