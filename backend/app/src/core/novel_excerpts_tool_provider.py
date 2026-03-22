"""List of tools for retrieving novel excerpts."""

from src.core.novel_excerpts_retriever import (
    get_novel_excerpts_for_keyword,
    get_novel_excerpts_for_question,
)
from src.model.tool import Tool, ToolArgument, ToolSpec


def _get_novel_excerpts_for_keyword(question: str, limit: int) -> str:
    excerpts = get_novel_excerpts_for_keyword(keyword=question, limit=limit)
    return _join_excerpts(excerpts)


def _get_novel_excerpts_for_question(question: str, limit: int) -> str:
    excerpts = get_novel_excerpts_for_question(question=question, limit=limit)
    return _join_excerpts(excerpts)


novel_excerpts_tools: list[Tool] = [
    Tool(
        spec=ToolSpec(
            name="get_novel_excerpts_for_keyword",
            description="Retrieves excerpts from the novel Alice's Adventures in Wonderland for a keyword.",
            arguments=[
                ToolArgument(
                    name="keyword", description="The keyword to retrieve excerpts for"
                )
            ],
        ),
        function=_get_novel_excerpts_for_keyword,
    ),
    Tool(
        spec=ToolSpec(
            name="get_novel_excerpts_for_question",
            description="Retrieves excerpts from the novel Alice's Adventures in Wonderland related to a question.",
            arguments=[
                ToolArgument(
                    name="question", description="The question to retrieve excerpts for"
                )
            ],
        ),
        function=_get_novel_excerpts_for_question,
    ),
]


def _join_excerpts(excerpts):
    return "\n\n".join(
        f"**Excerpt {index + 1}**\n{excerpt}" for index, excerpt in enumerate(excerpts)
    )
