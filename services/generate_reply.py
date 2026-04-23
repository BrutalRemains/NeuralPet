from data.database import save_creature
from services.action import apply_user_input
from services.prompt_builder import render_action_prompt
from services.qwenllm import get_llm

def generate_reply(creature, user_input):
    result = apply_user_input(creature, user_input)
    
    prompt = render_action_prompt(
        context=creature.prompt_context(),
        intent=result["intent"],
        action_result=result["action_result"],
        user_text=result["user_text_for_llm"],
    )

    llm = get_llm()
    output = llm(prompt, max_tokens=120, temperature=0.7, stop=["User:", "Owner:"])

    reply = output["choices"][0]["text"].strip()

    save_creature(creature)

    return {
        "intent": result["intent"],
        "action_result": result["action_result"],
        "reply": reply,
    }