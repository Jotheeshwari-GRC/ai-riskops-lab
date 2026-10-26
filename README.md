# ai-riskops-lab
AI powered risk operations lab - A hands-on AI-powered Cybersecurity Risk Operations Lab built using Python, Docker, and AWS to explore continuous risk management, security automation, and GRC.
## Project Objectives

- Learn AWS cloud infrastructure and security.
- Build Python applications using FastAPI.
- Learn Docker containerization.
- Explore IAM security and risk management.
- Develop AI-assisted cybersecurity risk assessment capabilities.

## Technologies

- AWS EC2 and IAM
- Python and FastAPI
- Docker
- Git and GitHub

## Project Status

Currently learning and building the foundation of the application.
  
## Amazon Bedrock Agent Lab

A learning exercise using fictional security findings and a simulated
server configuration. Model requests use Amazon Nova Lite through Bedrock.

### Components

- risk_agent.py: reads findings, requests recommendations and saves a proposal.
- remediate.py: asks for approval, backs up the simulated configuration,
  restricts admin access and verifies the saved change.
- riskops_agent.py: connects model tool requests to the remediation tool,
  validates the requested action and records the observed result.
- findings/: three fictional cloud, IAM and vulnerability reports.
- lab-server.json: simulated server settings.
- requirements-agent.txt: Python dependencies for this lab.

### Tested So Far

- Findings analysis and proposal saving: tested.
- Standalone simulated remediation with approval: tested.
- Combined agent workflow: syntax checked; execution testing pending.

### Scope and Next Steps

Changes affect a local JSON file, not real AWS network settings.
Generated proposals are recommendations requiring review.

Next: test the combined workflow and correlate separate findings into
a single business-risk scenario.

The scripts currently expect the working lab at ~/ai-riskops-lab.
They use the EC2 IAM role for Bedrock access; no API keys are embedded.

