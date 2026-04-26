import json
import os

STATE_PATH = "state/cepta.state.json"

def load_state():
    with open(STATE_PATH, "r") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)

def parse_event(comment: str):
    if "/collect" in comment:
        return "COLLECT"
    if "/execute" in comment:
        return "EXECUTE"
    if "/track" in comment:
        return "TRACK"
    return None

def transition(state, event):

    if event == "COLLECT":
        state["phase"] = "EXECUTE"
        state["counter"] += 1

    elif event == "EXECUTE":
        state["phase"] = "TRACK"

    elif event == "TRACK":
        state["phase"] = "COLLECT"

    return state

def run():
    comment = os.environ.get("COMMENT_BODY", "")
    state = load_state()

    event = parse_event(comment)

    if event:
        state = transition(state, event)
        state["last_event"] = event

    save_state(state)
    print(json.dumps(state, indent=2))

if __name__ == "__main__":
    run()