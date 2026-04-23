from services.action import apply_user_input
from services.prompt_builder import render_action_prompt

def generate_reply(creature, user_input):
    result = apply_user_input(creature, user_input)
    
    promot = render_action_prompt(
        context=creature.get_context(),
        intent=result["intent"],
        action_result=result["action_result"],
        user_text=result["user_text_for_llm"],
    )