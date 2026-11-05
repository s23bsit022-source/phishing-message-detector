import base64
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

st.set_page_config(page_title="Phishing Shield | AI Email Security", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

MODEL_REPOS = {
    "DistilBERT · Encoder": "Aaqib099/distilbert-phishing-detection",
    "GPT-2 · Decoder": "Aaqib099/gpt2-phishing-detection",
}

@st.cache_resource(show_spinner=False)
def load_model(repo_id: str):
    tokenizer = AutoTokenizer.from_pretrained(repo_id)
    model = AutoModelForSequenceClassification.from_pretrained(repo_id)
    if tokenizer.pad_token_id is None and tokenizer.eos_token is not None:
        tokenizer.pad_token = tokenizer.eos_token
    model.eval()
    return tokenizer, model

image_path = Path(__file__).parent / "cyber_background.png"
background = ""
if image_path.exists():
    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    background = f"url('data:image/png;base64,{encoded}')"





# Decorative pointer trail: best-effort enhancement. Streamlit may isolate
# component iframes on some hosting versions; core app remains fully functional.
components.html("""
<script>
(() => {
 try {
  const doc = window.parent.document;
  if (doc.getElementById('phishing-pointer-trail')) return;
  const style = doc.createElement('style');
  style.id = 'phishing-pointer-trail';
  style.textContent = `
   .phishing-dot {position:fixed;pointer-events:none;z-index:2147483640;border-radius:50%;background:#58dfff;box-shadow:0 0 14px #17caff;transform:translate(-50%,-50%);transition:opacity .35s;}
   @media (prefers-reduced-motion: reduce) {.phishing-dot{display:none!important}}
  `;
  doc.head.appendChild(style);
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const dots = Array.from({length:12}, (_,i) => {
   const d=doc.createElement('div'); d.className='phishing-dot';
   const size=Math.max(3,11-i*.65);d.style.width=size+'px';d.style.height=size+'px';
   d.style.opacity='0';doc.body.appendChild(d);return {el:d,x:-100,y:-100};
  });
  let x=-100,y=-100,visible=false;
  doc.addEventListener('pointermove',e=>{if(e.pointerType==='touch')return;x=e.clientX;y=e.clientY;visible=true;},{passive:true});
  doc.addEventListener('pointerout',e=>{if(!e.relatedTarget)visible=false;},{passive:true});
  function frame(){let px=x,py=y;dots.forEach((dot,i)=>{const factor=i===0?.42:.27;dot.x+=(px-dot.x)*factor;dot.y+=(py-dot.y)*factor;dot.el.style.left=dot.x+'px';dot.el.style.top=dot.y+'px';dot.el.style.opacity=visible?String(Math.max(.08,.85-i*.065)):'0';px=dot.x;py=dot.y;});requestAnimationFrame(frame)}
  frame();
 } catch(err) { /* iframe isolation: harmless, CSS hover effects still work */ }
})();
</script>
""", height=0)

st.markdown('<div class="hero-kicker">AI-powered threat intelligence / Live demo</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Detect deception.<br><span>Protect your inbox.</span></div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">A sleek phishing-message analyzer powered by two fine-tuned transformer models. Paste a suspicious email, select your AI model, and inspect its prediction.</div>', unsafe_allow_html=True)
st.markdown('<span class="model-pill">✦ DistilBERT &nbsp; • &nbsp; GPT-2 &nbsp; • &nbsp; Binary classification</span>', unsafe_allow_html=True)

left, right = st.columns([1.5, 1], gap="large")
with left:
    with st.container(border=True):
        st.markdown('<div class="glass-title">🔍 Message scanner</div><div class="glass-sub">Choose your model and enter the message you want to inspect.</div>', unsafe_allow_html=True)
        model_choice = st.selectbox("Detection engine", list(MODEL_REPOS), help="Switch between encoder-only DistilBERT and decoder-only GPT-2.")
        message = st.text_area("Email or message", height=220, placeholder="Paste an email or SMS here...", max_chars=20000)
        analyze = st.button("✦ Analyze message", type="primary", use_container_width=True)
        st.caption("For demonstration only · Do not paste passwords or sensitive personal information.")

with right:
    with st.container(border=True):
        st.markdown('<div class="glass-title">🛡️ Threat analysis</div><div class="glass-sub">Your model prediction will appear here.</div>', unsafe_allow_html=True)
        if not analyze:
            st.info("Ready to scan. Enter a message and press **Analyze message**.", icon="🔎")
        elif not message.strip():
            st.warning("Please enter a message before analyzing it.")
        else:
            try:
                with st.spinner("Loading model and analyzing message..."):
                    tokenizer, model = load_model(MODEL_REPOS[model_choice])
                    inputs = tokenizer(message, return_tensors="pt", truncation=True, max_length=256)
                    # DistilBERT does not accept token_type_ids; removing them is
                    # safe for this binary-classification app and for GPT-2.
                    inputs.pop("token_type_ids", None)
                    with torch.inference_mode():
                        logits = model(**inputs).logits
                        probs = torch.softmax(logits, dim=-1)[0]
                    predicted_id = int(torch.argmax(probs).item())
                    confidence = float(probs[predicted_id].item())
                    safe_prob = float(probs[0].item())
                    phishing_prob = float(probs[1].item())
                if predicted_id == 1:
                    st.error("⚠️ **Potential phishing detected**")
                else:
                    st.success("✓ **Likely safe email**")
                st.metric("Model confidence", f"{confidence * 100:.2f}%")
                st.progress(confidence)
                st.caption(f"Model: {model_choice} · Label: {model.config.id2label[predicted_id]}")
                with st.expander("View classification probabilities", expanded=True):
                    st.write(f"🟢 Safe email: **{safe_prob * 100:.2f}%**")
                    st.progress(safe_prob)
                    st.write(f"🔴 Phishing email: **{phishing_prob * 100:.2f}%**")
                    st.progress(phishing_prob)
            except Exception as exc:
                st.error("Unable to analyze this message. Check the application logs if the issue continues.")
                st.code(f"{type(exc).__name__}: {exc}")


# Developer Credit
st.markdown("""
<style>
.developer-credit {
    text-align: center;
    margin-top: 45px;
    padding: 22px;
    border-top: 1px solid rgba(0, 212, 255, 0.35);
    color: #a9c5dc;
    font-size: 14px;
    letter-spacing: 1px;
}

.developer-credit strong {
    color: #55e6ff;
    font-size: 18px;
    font-weight: 800;
    text-shadow: 0 0 12px rgba(0, 212, 255, 0.6);
    transition: all 0.3s ease;
}

.developer-credit strong:hover {
    color: #ffffff;
    text-shadow: 0 0 20px #00d4ff;
}

</style>

<div class="developer-credit">
    🛡️ Designed & Developed by
    <strong>AAQIB ALI</strong>
    <div style="margin-top:8px; font-size:12px;">
        AI-Powered Phishing Detection System
    </div>
</div>
""", unsafe_allow_html=True)

# Responsive full-screen layout
st.markdown("""
<style>
/* Reduce Streamlit's default spacing */
.block-container {
    max-width: 1200px !important;
    padding-top: 0.6rem !important;
    padding-bottom: 0.3rem !important;
}

/* Compact headings and paragraphs */
h1, h2, h3 {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

div[data-testid="stVerticalBlock"] {
    gap: 0.45rem;
}

/* Compact message input */
textarea {
    min-height: 110px !important;
    max-height: 22vh !important;
}

/* Compact buttons */
.stButton button {
    min-height: 42px !important;
}

/* Compact developer credit */
.developer-credit {
    margin-top: 8px !important;
    padding: 8px !important;
}

/* Desktop screen-fit adjustments */
@media (min-width: 900px) and (min-height: 650px) {
    .block-container {
        padding-top: 0.4rem !important;
    }

    div[data-testid="stTextArea"] textarea {
        height: clamp(100px, 18vh, 160px) !important;
    }
}

/* Keep mobile layout scrollable for usability */
@media (max-width: 768px) {
    .block-container {
        padding: 1rem !important;
    }

    textarea {
        max-height: none !important;
    }
}
</style>
""", unsafe_allow_html=True)


