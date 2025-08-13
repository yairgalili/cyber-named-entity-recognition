import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from collections import defaultdict
import time
from tqdm import tqdm
from seqeval.metrics import precision_score, recall_score, f1_score, classification_report
from seqeval.scheme import IOB2
import numpy as np
import pickle

from utils import dnrti_to_securebert, map_predicted_to_true, predictions_to_iob


# Load the data back
with open('dataset.pkl', 'rb') as f:
    loaded_data = pickle.load(f)
    sentences_tokens = loaded_data['sentences_tokens']
    true_labels = loaded_data['true_labels']


# -------------------------------
# 4. SETUP NER PIPELINE
# -------------------------------

device = 0 if torch.cuda.is_available() else -1
# Use a pipeline as a high-level helper
ner_pipeline = pipeline("token-classification", model="CyberPeace-Institute/SecureBERT-NER", device=device)

print(f"Running inference on {len(sentences_tokens)} sentences...")
start_time = time.time()

all_predictions = []

for tokens in tqdm(sentences_tokens):
    sentence = " ".join(tokens)
    try:
        result = ner_pipeline(sentence)
        all_predictions.append(result)
    except Exception as e:
        print(f"Error processing sentence: {e}")
        all_predictions.append([])

inference_time = time.time() - start_time
latency_per_sentence = inference_time / len(sentences_tokens)
print(f"Total inference time: {inference_time:.2f}s")
print(f"Latency per sentence: {latency_per_sentence:.3f}s")


predicted_iob_tags = predictions_to_iob(sentences_tokens, all_predictions)

predicted_iob_tags_mapped = map_predicted_to_true(predicted_iob_tags, true_labels, dnrti_to_securebert)

# Ensure all are strings
mapped_true_labels_str = [[str(t) for t in sent] for sent in true_labels]
predicted_iob_tags_str = [[str(t) for t in sent] for sent in predicted_iob_tags_mapped]


precision = precision_score(mapped_true_labels_str, predicted_iob_tags_str, suffix=False, scheme=IOB2)
recall = recall_score(mapped_true_labels_str, predicted_iob_tags_str, suffix=False, scheme=IOB2)
f1 = f1_score(mapped_true_labels_str, predicted_iob_tags_str, suffix=False, scheme=IOB2)

print("\n=== Entity-Level Evaluation (IOB2) ===")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1-Score:  {f1:.4f}")
print(f"Latency per sentence: {latency_per_sentence:.3f} seconds")

print("\n=== Classification Report ===")
print(classification_report(mapped_true_labels_str, predicted_iob_tags_str, suffix=False, scheme=IOB2))

