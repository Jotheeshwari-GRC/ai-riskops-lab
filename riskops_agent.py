import json
import subprocess
import sys
from pathlib import Path
import boto3

import json
import subprocess
import sys
from pathlib import Path
import boto3

lab = Path.home() / "ai-riskops-lab"
model = "apac.amazon.nova-lite-v1:0"
client = boto3.client("bedrock-runtime", region_name="ap-south-1")

tool_config = {
    "tools": [
        {
            "toolSpec": {
                "name": "restrict_simulated_admin_access",
                "description": (
                    "Restrict admin access in a local simulation "
                    "for lab-web-01. Requires human approval. "
                    "Does not change real network settings."
                ),
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "server": {
                                "type": "string",
                                "description": "The simulated server: lab-web-01"
                            }
                        },
                        "required": ["server"]
                    }
                }
            }
        }
    ]
}
state = json.loads((lab / "lab-server.json").read_text())

messages = [
    {
        "role": "user",
        "content": [
            {
                "text": (
                    "This is a local configuration simulation. "
                    "The goal is restricted admin access for lab-web-01. "
                    "Use the available tool if a change is needed. "
                    "Do not claim completion before receiving tool results. "
                    "Current configuration: " + json.dumps(state)
                )
            }
        ]
    }
]

response = client.converse(
    modelId=model,
    messages=messages,
    toolConfig=tool_config,
    inferenceConfig={"maxTokens": 400, "temperature": 0},
)

message = response["output"]["message"]
messages.append(message)
requests = [
    block["toolUse"]
    for block in message["content"]
    if "toolUse" in block
]

if response["stopReason"] != "tool_use" or len(requests) != 1:
    print("No single tool request received. No change made.")
    print(json.dumps(message, indent=2))
    raise SystemExit()

request = requests[0]

if (
    request["name"] != "restrict_simulated_admin_access"
    or request["input"] != {"server": "lab-web-01"}
):
    raise SystemExit("Stopped: tool request is outside the allowed scope.")

print("Model requested:", request["name"])
print("Target:", request["input"]["server"])

before = json.loads((lab / "lab-server.json").read_text())

completed = subprocess.run(
    [sys.executable, str(lab / "remediate.py")]
)
after = json.loads((lab / "lab-server.json").read_text())
expected = dict(before)
expected["admin_access"] = "restricted"

verified = completed.returncode == 0 and after == expected

result = {
    "simulation": True,
    "tool": request["name"],
    "before": before,
    "after": after,
    "exit_code": completed.returncode,
    "verified": verified,
}

evidence = lab / "plans" / "last-tool-result.json"
evidence.write_text(json.dumps(result, indent=2) + "\n")
print("Verified simulated restriction:", verified)
print("Evidence saved to:", evidence)

messages.append({
    "role": "user",
    "content": [{
        "toolResult": {
            "toolUseId": request["toolUseId"],
            "content": [{"json": result}],
            "status": "success" if verified else "error",
        }
    }],
})

summary = client.converse(
    modelId=model,
    messages=messages,
    toolConfig=tool_config,
    inferenceConfig={"maxTokens": 300, "temperature": 0},
)

print("\nModel summary:")
for block in summary["output"]["message"]["content"]:
    if "text" in block:
        print(block["text"])
    if "toolUse" in block:
        print("Additional tool request received but not executed.")

