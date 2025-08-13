# app.py
import io
import pandas as pd
import torch
from transformers import pipeline
import streamlit as st
from utils import apply_model

device = 0 if torch.cuda.is_available() else -1
ner_pipeline = pipeline("token-classification", model="CyberPeace-Institute/SecureBERT-NER", device=device)

st.set_page_config(page_title="NER on Text Files", page_icon="🧠", layout="centered")

st.title("🧠 Named Entity Recognition (NER)")
st.write("Upload a single **.txt** file and extract entities by class.")

# --- Sidebar: model selection / help ---
with st.sidebar:
    st.header("Settings")
    model_name = "CyberPeace-Institute/SecureBERT-NER"
 

uploaded = st.file_uploader(
    "Upload a .txt file",
    type=["txt"],
    accept_multiple_files=False,   # 🔒 Only one file at a time
    help="Plain text only."
)

if uploaded is not None:
    # Read text safely
    raw_bytes = uploaded.read()
    try:
        text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        # Fallback if not UTF-8
        text = raw_bytes.decode("latin-1", errors="ignore")

    st.subheader("Preview")
    st.text_area("File contents", text, height=220)

    if st.button("Process with NER", type="primary"):
        with st.spinner("Loading model and extracting entities…"):
            preds = apply_model([[text]], ner_pipeline)[0][0]

        # Group unique entities by class label
        by_label = {}
        for p in preds:
            label = p.get("entity_group") or p.get("entity") or "UNKNOWN"
            # Normalize the entity text
            ent_text = (p.get("word") or p.get("entity") or "").strip()
            if not ent_text:
                start, end = p.get("start"), p.get("end")
                ent_text = text[start:end] if (start is not None and end is not None) else ""
                ent_text = ent_text.strip()
            if not ent_text:
                continue
            by_label.setdefault(label, [])
            # keep unique but preserve order
            if ent_text not in by_label[label]:
                by_label[label].append(ent_text)

        # Build results table
        if by_label:
            df = pd.DataFrame(
                [{"Class": label, "Entities": ", ".join(ents)} for label, ents in by_label.items()]
            ).sort_values("Class").reset_index(drop=True)

            st.subheader("Results")
            st.dataframe(df, use_container_width=True)

            # Offer CSV download
            csv_buf = io.StringIO()
            df.to_csv(csv_buf, index=False)
            st.download_button(
                label="Download results as CSV",
                data=csv_buf.getvalue(),
                file_name="ner_results.csv",
                mime="text/csv",
            )
        else:
            st.info("No entities found by the selected model.")

else:
    st.info("Upload a single .txt file to begin.")
