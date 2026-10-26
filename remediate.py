import json
from pathlib import Path

path = Path.home() / "ai-riskops-lab" / "lab-server.json"
original = path.read_text()
state = json.loads(original)

if state.get("server") != "lab-web-01":
    raise SystemExit("Stopped: unexpected server.")

current = state.get("admin_access")
print("SIMULATION — current admin access:", current)

if current == "restricted":
    print("Already restricted. No change needed.")
    raise SystemExit()

if current != "public":
    raise SystemExit("Stopped: unexpected access setting.")

approval = input("Type APPROVE to restrict simulated access: ")
if approval.strip() != "APPROVE":
    raise SystemExit("No change made.")

backup = path.with_suffix(".before.json")
backup.write_text(original)

state["admin_access"] = "restricted"
path.write_text(json.dumps(state, indent=2) + "\n")

saved_state = json.loads(path.read_text())
if saved_state != state:
    raise SystemExit("Verification failed. Review the lab file.")

print("Verified: simulated admin access is restricted.")
print("Original configuration saved to:", backup)
