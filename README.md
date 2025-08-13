---
title: Cyber Ner
emoji: 🚀
colorFrom: red
colorTo: red
sdk: docker
app_port: 8501
tags:
- streamlit
pinned: false
short_description: Streamlit template space
---

# cyber-named-entity-recognition

# DNRTI dataset
28 classes

['B-Area', 'B-Exp', 'B-Features', 'B-HackOrg', 'B-Idus', 'B-OffAct', 'B-Org', 'B-Purp', 'B-SamFile', 'B-SecTeam', 'B-Time', 'B-Tool', 'B-Way', 'Despite', 'I-Area', 'I-Exp', 'I-Features', 'I-HackOrg', 'I-Idus', 'I-OffAct', 'I-Org', 'I-Purp', 'I-SamFile', 'I-SecTeam', 'I-Time', 'I-Tool', 'I-Way', 'O']
## Important classes
HackOrg, SecTeam, [dus, Org], [OffAct, Way], Exp, Tool, SamFile, Time, Area, [Purp, Features]

# CyberPeace-Institute/SecureBERT-NER
28 classes
['B-ACT', 'B-APT', 'B-DOM', 'B-ENCR', 'B-FILE', 'B-IDTY', 'B-IP', 'B-LOC', 'B-MAL', 'B-MD5', 'B-OS', 'B-PROT', 'B-SECTEAM', 'B-TIME', 'B-TOOL', 'B-VULID', 'B-VULNAME', 'I-ACT', 'I-APT', 'I-FILE', 'I-IDTY', 'I-LOC', 'I-MAL', 'I-OS', 'I-SECTEAM', 'I-TIME', 'I-TOOL', 'I-VULNAME']


=== Entity-Level Evaluation (IOB2) ===
Precision: 0.4605
Recall:    0.4811
F1-Score:  0.4705
Latency per sentence: 0.192s (CPU)

One can improve it by ignoring errors between similar groups.


# PranavaKailash/CyNER-2.0-DeBERTa-v3-base 
13 classes
['B-Indicator', 'B-Malware', 'B-Organization', 'B-System', 'B-Threat_group', 'B-Vulnerability', 'I-Date', 'I-Indicator', 'I-Malware', 'I-Organization', 'I-System', 'I-Threat_group', 'I-Vulnerability']


=== Entity-Level Evaluation (IOB2) ===
Precision: 0.2006
Recall:    0.1345
F1-Score:  0.1611
Latency per sentence: 0.614s

The performances are affected by my comparison and the mapping that I chose.

dnrti_to_syner = {
    "HackOrg": "Organization",
    "SecTeam": "Organization",
    "Idus": "Indicator",
    "Org": "Indicator",
    "OffAct": "System", 
    "Way": "System", 
    "Exp": "Vulnerability", 
    "Tool": "Malware",
    "SamFile": "System",
    "Time": "Date",
    "Area": "O",
    "Purp": "O",
    "Features": "O"
}


# How to run?
# evaluation
1) python install -r requirements.txt
2) python create_dataset.py
3) python evaluate.py

# service
1) docker build  -f Dockerfile_api . -t ner-app
2) docker run -p 8000:8000 ner-app
