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

# NER Benchmarking & On-Prem Deployment

This repository contains the complete solution for benchmarking, selecting, and deploying a Named Entity Recognition (NER) model for the DNRTI dataset, along with an optional web interface for end users.

The project was completed as part of a mission to evaluate SecureBert-NER vs CyNER, choose the best performer, and make it easy to use entirely offline.

The work was carried out in three main stages:

1) Benchmarking Analysis

    Goal: Compare SecureBert-NER and CyNER on the DNRTI dataset.

    Dataset: DNRTI, containing documents with annotated named entities.

    Evaluation Metrics:

    1) Precision

    2) Recall

    3) Latency

    Special Handling: Class mapping applied to align DNRTI labels with model outputs

2) On-Prem NER Service

    Goal: Package the chosen NER model into an offline-capable API service.

    Features:

     - HTTP-based API that accepts raw text and returns detected entities + their classes.

    - Fully Dockerized for easy on-prem installation.

    - No internet connection required after setup.

    Deliverables:

     - Dockerfile and deployment instructions.

     - Local test scripts to validate API functionality.

3) Web UI with Streamlit

    The web provides a simple, user-friendly interface for non-technical users.

    Features:

     - Upload a text file (one at a time).

     - Process file content using the deployed NER model.

     - Display results in a clean table:


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
3) python tests/test.py

# streamlit
1) docker build . -t streamlit-app
2) docker run -p 8501:8501 streamlit-app

See https://huggingface.co/spaces/yairgalili/cyber-ner