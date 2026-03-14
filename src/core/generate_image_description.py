from string import Template

from src.adapters.llama import invoke_llama
from src.core.get_novel_excerpts import get_novel_excerpts


def generate_image_description(npc: str) -> str:
    excerpts = get_novel_excerpts(npc)
    prompt = Template(_prompt_template).substitute(
        npc=npc, excerpts="\n".join(excerpts)
    )
    return invoke_llama(prompt)


_prompt_template = """
Create a description of $npc and a suitable setting for a text-to-image LLM. 
The description must not mention any other character besides $npc.
Respond only with the description and do not include an introductory sentence.
                        
You can use the following excerpts from the novel as inspiration:
                            
$excerpts
"""

if __name__ == "__main__":
    while True:
        npc = input("NPC: ")
        print(get_novel_excerpts(npc))
        print(generate_image_description(npc))
