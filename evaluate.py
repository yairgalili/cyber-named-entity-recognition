from seqeval.metrics import precision_score, recall_score, f1_score, classification_report
from seqeval.scheme import IOB2
import pickle

import torch
from transformers import pipeline

from utils import apply_model, dnrti_to_securebert, map_predicted_to_true, predictions_to_iob, dnrti_to_cyner


# Load the data back
with open('dataset.pkl', 'rb') as f:
    loaded_data = pickle.load(f)
    sentences_tokens = loaded_data['sentences_tokens']
    true_labels = loaded_data['true_labels']

def evaluate(model_name, mapping):
    device = 0 if torch.cuda.is_available() else -1

    ner_pipeline = pipeline("token-classification", model=model_name, device=device)

    predictions, latency_per_sentence = apply_model(sentences_tokens, ner_pipeline)

    predicted_iob_tags = predictions_to_iob(sentences_tokens, predictions)

    predicted_iob_tags_mapped = map_predicted_to_true(predicted_iob_tags, true_labels, mapping)

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


if __name__ == "__main__":
    model_name='CyberPeace-Institute/SecureBERT-NER'
    if model_name == 'CyberPeace-Institute/SecureBERT-NER':
        mapping = dnrti_to_securebert
    else:
        mapping = dnrti_to_cyner

    evaluate(model_name, mapping)