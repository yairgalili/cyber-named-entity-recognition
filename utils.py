import numpy as np
import pickle
import time
from tqdm import tqdm


def predictions_to_iob(sentences_tokens, predictions):
    pred_sequences = []
    for tokens, preds in zip(sentences_tokens, predictions):
        pred_tags = ['O'] * len(tokens)
        char_to_token = {}
        current_char = 0
        for idx, token in enumerate(tokens):
            char_to_token[current_char] = idx
            current_char += len(token) + 1  # +1 for space

        for ent in preds:
            start_char = ent['start']
            end_char = ent['end']
            label = ent['entity']

            # Find which tokens overlap with this span
            start_token_idx = char_to_token.get(start_char, None)
            if start_token_idx is None:
                # Find closest token
                keys = sorted(char_to_token.keys())
                start_token_idx = char_to_token[keys[np.searchsorted(keys, start_char) - 1]]

            # Mark all overlapping tokens
            for i in range(start_token_idx, min(len(tokens), start_token_idx + 5)):
                token_start = sum(len(t) + 1 for t in tokens[:i])
                token_end = token_start + len(tokens[i])
                if token_start >= end_char:
                    break
                if token_end > start_char and token_start < end_char:
                  pred_tags[i] = label
        pred_sequences.append(pred_tags)
    return pred_sequences


# Map DNRTI labels to SecureBERT label space
# One can add mapping for multiple labels to the same DNRTI label
dnrti_to_securebert = {
    "HackOrg": "APT",
    "SecTeam": "SECTEAM",
    "Idus": "IDTY",
    "Org": "IDTY",
    "OffAct": "ACT", 
    "OffAct": "OS", 
    "OffAct": "TOOL",
    "Way": "ACT", 
    "Way": "OS", 
    "Way": "TOOL",
    "Exp": "VULID", 
    "Exp": "VULNAME",
    "Tool": "MAL",
    "SamFile": "File",
    "O": "DOM", 
    "O": "ENCR", 
    "O": "IP", 
    "O": "URL", 
    "O": "MD5", 
    "O": "PROT", 
    "O": "EMAIL", 
    "O": "SHA1", 
    "O": "SHA2",
    "Time": "TIME",
    "Area": "LOC",
    "Purp": "O",
    "Features": "O"
}

dnrti_to_cyner = {
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

def remove_prefix(label):
    return label.split('-')[1] if '-' in label else label

def map_predicted_to_true(predicted_labels, true_labels, mapping):
    mapped_predicted_labels = []
    for pred_sent, true_sent in zip(predicted_labels, true_labels):
        mapped_pred_sent = []
        for pred_label, true_label in zip(pred_sent, true_sent):
            pred_no_prefix = remove_prefix(pred_label)
            true_no_prefix = remove_prefix(true_label)
            if (true_no_prefix, pred_no_prefix) in mapping.items():
                # If there are multiple mapping - choose 1 of them
                mapped_pred_sent.append(pred_label.replace(pred_no_prefix, true_no_prefix))
            else:
                mapped_pred_sent.append(pred_label)
        mapped_predicted_labels.append(mapped_pred_sent)
    return mapped_predicted_labels


# Use a pipeline as a high-level helper
def apply_model(sentences_tokens, ner_pipeline):

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

    return all_predictions, latency_per_sentence


# if __name__ == "__main__":
#     data = {"sentences_tokens": sentences_tokens, "predictions": predictions}
#     with open('predictions.pkl', 'wb') as f:
#         pickle.dump(data, f)
if __name__ == "__main__":
    with open('predictions_cyner.pkl', 'rb') as f:
        data = pickle.load(f)
        sentences_tokens = data['sentences_tokens']
        predictions = data['predictions']
        predicted_iob_tags = predictions_to_iob(sentences_tokens, predictions)

    with open('dataset.pkl', 'rb') as f:
        loaded_data = pickle.load(f)
        sentences_tokens = loaded_data['sentences_tokens']
        true_labels = loaded_data['true_labels']

    result = map_predicted_to_true(predicted_iob_tags, true_labels, dnrti_to_syner)
    print(result)
    all_dnrti_labels = sorted(set(label for x in true_labels for label in x))
    all_dnrti_labels = sorted(set(label["entity"] for x in predictions for label in x))
