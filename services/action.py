import json
from pathlib import Path

INTENT_THRESHOLD = 0.7

TRICKS_PATH = Path(__file__).resolve().parents[1] / "data" / "tricks.json"

def load_trick_names():
    return json.loads(TRICKS_PATH.read_text(encoding="utf-8"))

# extract trick name for the purpose of performing
def extract_trick_name(text, known_tricks):
    t = text.lower()
    for trick in known_tricks:
        if trick.lower() in t:
            return trick
    return known_tricks[0] if known_tricks else None

# extract trick name for the purpose of teaching
def extract_trick_from_teach_input(text):
    t = text.lower().strip()
    predefined_tricks = load_trick_names()

    # if it matches a predefined trick
    for trick in predefined_tricks:
        if trick.lower() in t:
            return trick.title()
    
    teach_keywords = ["teach you to", "teach you", "learn to", "train you to", "train you", "teach"]      
    for kw in teach_keywords:
        if kw in t:
            after = t.split(kw,1)[-1].strip()
            # strip filler to find the word for the trick. inelegant but for now it's best option
            for filler in ["please", "!", "?", "."]:
                after = after.replace(filler, " ").strip()
            if after:
                return after.title()
    return None

# we first check for intent ourselves using simple keyword matching, faster than llm
def local_intent_parse(text, known_tricks):
    t = text.lower().strip()

    trick = extract_trick_name(text, known_tricks)

    if any(p in t for p in ["feed", "give food", "eat"]):
        return {"intent": "feed", "confidence": 0.9}
    if any(p in t for p in ["play", "fetch", "game"]):
        return {"intent": "play", "confidence": 0.85}
    if any(p in t for p in ["rest", "sleep", "nap"]):
        return {"intent": "rest", "confidence": 0.9}
    if any(p in t for p in ["teach", "learn trick", "new trick"]):
        return {"intent": "teach", "confidence": 0.85}
    if any(p in t for p in [trick,"perform", "do a trick", "show off"]):
        return {"intent": "perform", "confidence": 0.8}
    if "status" in t:
        return {"intent": "status", "confidence": 0.95}

    return {"intent": "chat", "confidence": 0.0}

def parse_command(text):
    if not text.startswith("/"):
        return None
    return text[1:].split(" ", 1)[0].strip().lower()

def llm_intent_parse(text, known_tricks): # for allowing the llm to determine user intent. the primary reason to use an llm in the first place
    tricks_str = ", ".join(known_tricks)
    prompt = f"""You are classifying the intent of a user's message to their virtual pet. The
Known tricks the pet knows: {tricks_str}          
Respond ONLY with valid JSON, no explanation:
{{"intent": "feed|play|rest|teach|perform|chat", "confidence": 0.0, "trick": "trick name or null"}}

Message: "{text}"
"""
    try:
        out = llm.create_chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=40,
            temperature=0.0,
        )
        raw = out["choices"][0]["message"]["content"].strip()
        data = json.loads(raw)
        return {
            "intent": data.get("intent", "chat"),
            "confidence": float(data.get("confidence", 0.0)),
            "trick": data.get("trick"),
        }
    except Exception:
        return {"intent": "chat", "confidence": 0.0, "trick": None}
def run_action(creature, intent, text):
    if intent == "feed":
        return creature.feed()
    if intent == "play":
        return creature.play()
    if intent == "rest":
        return creature.rest()
    if intent == "teach":
        trick = extract_trick_from_teach_input(text)
        return creature.teach_trick(trick)
    if intent == "perform":
        trick = extract_trick_name(text, creature.known_tricks)
        return creature.perform_trick(trick)
    if intent == "status":
        return {"success": True, "reason": "status_only"}
    return {"success": True, "reason": "chat_only"}

def apply_user_input(creature, user_input):
    text = user_input.strip()
    if not text:
        return {"intent": "chat", "action_result": {"success": False, "reason": "empty_input"}}

    cmd = parse_command(text)
    if cmd:
        intent = cmd
        action_result = run_action(creature, intent, text)
        return {"intent": intent, "action_result": action_result, "user_text_for_llm": text}

    parsed = local_intent_parse(text, creature.known_tricks)
    intent = parsed["intent"]

    if parsed["confidence"] >= INTENT_THRESHOLD and intent != "chat":
        action_result = run_action(creature, intent, text)
        return {"intent": intent, "action_result": action_result, "user_text_for_llm": text}

    llm_intent = llm_intent_parse(text, creature.known_tricks)
    
    
    return {
        "intent": "chat",
        "action_result": {"success": True, "reason": "chat_only"},
        "user_text_for_llm": text,
    }