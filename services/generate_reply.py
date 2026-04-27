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
    output = llm.create_chat_completion(
        messages= [
            {"role": "user", "content": prompt}
        ], 
        max_tokens=120, 
        temperature=0.7, 
        stop=["\n", "Peanut:", "Owner:", "You:"],
        )

    reply = output["choices"][0]["message"]["content"].strip()

    save_creature(creature)

    return {
        "intent": result["intent"],
        "action_result": result["action_result"],
        "reply": reply,
    }

def generate_dev_reply(user_input: str, system_prompt: str | None = None) -> str:
    # for testing and development purposes, allows direct access to the llm
    llm = get_llm()

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_input})

    result = llm.create_chat_completion(
        messages=messages,
        temperature=0.7,
        max_tokens=120,
    )

    return result["choices"][0]["message"]["content"].strip()