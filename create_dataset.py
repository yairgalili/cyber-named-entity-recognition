import os
import requests

# -------------------------------
# 1. DOWNLOAD AND EXTRACT DNRTI.RAR
# -------------------------------

DNRTI_URL = "https://github.com/SCreaMxp/DNRTI-A-Large-scale-Dataset-for-Named-Entity-Recognition-in-Threat-Intelligence/raw/master/DNRTI.rar"
OUTPUT_RAR = "DNRTI.rar"
EXTRACTED_DIR = "DNRTI_dataset"

if not os.path.exists(EXTRACTED_DIR):
    os.makedirs(EXTRACTED_DIR)

if not os.path.exists(OUTPUT_RAR):
    print("Downloading DNRTI.rar...")
    response = requests.get(DNRTI_URL, stream=True)
    with open(OUTPUT_RAR, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print("Download complete.")

# Extract RAR file (requires `rarfile` and system `unrar`)
try:
    import rarfile
    rarfile.UNRAR_TOOL = "unrar"  # Ensure unrar is installed: `sudo apt install unrar`
    with rarfile.RarFile(OUTPUT_RAR) as rf:
        rf.extractall(EXTRACTED_DIR)
    print(f"Extracted {OUTPUT_RAR} to {EXTRACTED_DIR}")
except Exception as e:
    print("Error: Failed to extract RAR. Install 'unrar' via: sudo apt install unrar")
    raise e

TEST_FILE = os.path.join(EXTRACTED_DIR, "test.txt")

if not os.path.exists(TEST_FILE):
    raise FileNotFoundError(f"{TEST_FILE} not found after extraction.")

# -------------------------------
# 2. LOAD TEST DATA (token \t label format)
# -------------------------------

def load_conll_format(file_path):
    sentences = []
    sentence = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                if sentence:
                    sentences.append(sentence)
                    sentence = []
            else:
                parts = line.split()
                if len(parts) >= 2:
                    token, label = parts[0], parts[1]
                    sentence.append((token, label))
    if sentence:
        sentences.append(sentence)
    return sentences

print("Loading test.txt...")
test_sentences = load_conll_format(TEST_FILE)
print(f"Loaded {len(test_sentences)} sentences from test.txt")

# Extract tokens and true labels
sentences_tokens = [[token for token, _ in sent] for sent in test_sentences]
true_labels = [[label for _, label in sent] for sent in test_sentences]

# DNRTI label list (extract all unique labels)
all_dnrti_labels = sorted(set(label for sent in test_sentences for _, label in sent))
print(f"DNRTI Labels: {all_dnrti_labels}")


if __name__ == "__main__":
    import pickle
    data = {"sentences_tokens": sentences_tokens, "true_labels": true_labels}
    with open('dataset.pkl', 'wb') as f:
        pickle.dump(data, f)