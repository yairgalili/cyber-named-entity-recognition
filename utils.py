import numpy as np
import pickle

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

# if __name__ == "__main__":
#     data = {"sentences_tokens": sentences_tokens, "predictions": predictions}
#     with open('predictions.pkl', 'wb') as f:
#         pickle.dump(data, f)
if __name__ == "__main__":
    with open('predictions.pkl', 'rb') as f:
        data = pickle.load(f)
        sentences_tokens = data['sentences_tokens']
        predictions = data['predictions']
        predicted_iob_tags = predictions_to_iob(sentences_tokens, predictions)

    with open('dataset.pkl', 'rb') as f:
        loaded_data = pickle.load(f)
        sentences_tokens = loaded_data['sentences_tokens']
        true_labels = loaded_data['true_labels']

    result = map_predicted_to_true(predicted_iob_tags, true_labels, dnrti_to_securebert)
    print(result)
