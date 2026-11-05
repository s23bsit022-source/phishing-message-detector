
import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

st.set_page_config(
    page_title="Phishing Message Detector",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ Phishing Message Detector")
st.write(
    "Detect potentially suspicious messages using "
    "fine-tuned DistilBERT and GPT-2 models."
)

MODEL_REPOS = {
    "DistilBERT (Encoder-only)": "Aaqib099/distilbert-phishing-detection",
    "GPT-2 (Decoder-only)": "Aaqib099/gpt2-phishing-detection"
}

@st.cache_resource
def load_model(repo_id):
    tokenizer = AutoTokenizer.from_pretrained(repo_id)
    model = AutoModelForSequenceClassification.from_pretrained(repo_id)
    model.eval()
    return tokenizer, model

model_choice = st.selectbox(
    "Choose a model:",
    list(MODEL_REPOS.keys())
)

message = st.text_area(
    "Enter an email or message:",
    height=180,
    placeholder="Paste the message you want to analyze..."
)

if st.button("Analyze Message", type="primary"):
    if not message.strip():
        st.warning("Please enter a message first.")
    else:
        with st.spinner("Analyzing message..."):
            try:
                repo_id = MODEL_REPOS[model_choice]
                tokenizer, model = load_model(repo_id)

                inputs = tokenizer(
                    message,
                    return_tensors="pt",
                    truncation=True,
                    max_length=256
                )

                with torch.no_grad():
                    outputs = model(**inputs)
                    probabilities = torch.softmax(
                        outputs.logits, dim=-1
                    )[0]

                predicted_id = probabilities.argmax().item()
                label = model.config.id2label[predicted_id]
                confidence = probabilities[predicted_id].item()

                if predicted_id == 1:
                    st.error("⚠️ Prediction: Phishing Email")
                else:
                    st.success("✅ Prediction: Safe Email")

                st.write(f"**Model:** {model_choice}")
                st.write(f"**Confidence:** {confidence * 100:.2f}%")

                st.progress(float(confidence))

                with st.expander("Class probabilities"):
                    st.write(
                        f"Safe Email: {probabilities[0].item() * 100:.2f}%"
                    )
                    st.write(
                        f"Phishing Email: {probabilities[1].item() * 100:.2f}%"
                    )

            except Exception as e:
                st.error(f"Unable to analyze message: {e}")

st.divider()
st.caption(
    "Educational demonstration only. "
    "Predictions are not a guarantee that a message is safe."
)
