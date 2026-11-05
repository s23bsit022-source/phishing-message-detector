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


st.markdown("""
<style>
.security-dashboard {
    max-width: 570px;
    margin: 12px 0 18px;
    padding: 15px;
    background: rgba(3, 21, 45, 0.68);
    border: 1px solid rgba(75, 215, 255, 0.25);
    border-radius: 16px;
    backdrop-filter: blur(12px);
}
.security-heading {
    color: #51d9ff;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 10px;
}
.security-stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 9px;
}
.security-stat {
    padding: 12px 9px;
    background: rgba(10, 41, 69, 0.8);
    border: 1px solid rgba(81, 217, 255, 0.15);
    border-radius: 10px;
    transition: transform .25s, border-color .25s;
}
.security-stat:hover {
    transform: translateY(-4px);
    border-color: #51d9ff;
}
.security-number {
    font-size: 22px;
    font-weight: 800;
    color: white;
}
.security-label {
    font-size: 11px;
    color: #a8c7dd;
}
.security-credit {
    margin-top: 12px;
    padding-top: 10px;
    border-top: 1px solid rgba(81, 217, 255, .2);
    color: #a8c7dd;
    font-size: 11px;
}
.security-credit strong {
    color: #51d9ff;
    font-size: 15px;
    letter-spacing: 1px;
}
@media(max-width: 600px) {
    .security-dashboard {padding: 10px;}
    .security-number {font-size: 17px;}
    .security-label {font-size: 10px;}
}
</style>

<div class="security-dashboard">
    <div class="security-heading">
        ✦ AI SECURITY INTELLIGENCE
    </div>
    <div class="security-stats">
        <div class="security-stat">
            <div class="security-number">02</div>
            <div class="security-label">AI Models</div>
        </div>
        <div class="security-stat">
            <div class="security-number">98.86%</div>
            <div class="security-label">Best Test Accuracy</div>
        </div>
        <div class="security-stat">
            <div class="security-number">LIVE</div>
            <div class="security-label">Message Analysis</div>
        </div>
    </div>
    <div class="security-credit">
        DESIGNED & DEVELOPED BY
        <strong>AAQIB ALI</strong>
    </div>
</div>
""", unsafe_allow_html=True)




st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root {{color-scheme:dark;}}
html,body,[data-testid="stAppViewContainer"] {{font-family:'DM Sans',sans-serif;}}
[data-testid="stAppViewContainer"] {{
 background:linear-gradient(90deg,rgba(2,9,27,.95) 0%,rgba(2,11,30,.90) 42%,rgba(3,15,38,.57) 100%), {background if background else 'linear-gradient(120deg,#06152c,#092b53)'};
 background-position:center center; background-size:cover; background-attachment:fixed;
 color:#e9f4ff;
}}
[data-testid="stHeader"] {{background:transparent;}}
[data-testid="stToolbar"] {{right:1rem;}}
[data-testid="stMainBlockContainer"] {{max-width:1150px;padding-top:3rem;padding-bottom:4rem;}}
#MainMenu,footer {{visibility:hidden;}}
h1,h2,h3 {{font-family:'Space Grotesk',sans-serif!important;letter-spacing:-.04em;}}
.hero-kicker {{color:#5de3ff;font-size:.76rem;font-weight:700;letter-spacing:.24em;text-transform:uppercase;margin-bottom:.7rem;}}
.hero-title {{font-size:clamp(2.6rem,5.5vw,5rem);line-height:1.04;font-weight:700;max-width:760px;letter-spacing:-.06em;margin:0 0 1rem 0;color:#f5fbff;text-shadow:0 5px 32px #0006;}}
.hero-title span {{color:#60dfff;}}
.hero-sub {{max-width:640px;font-size:1.08rem;color:#b4c9dd;line-height:1.7;margin-bottom:2.5rem;}}
.glass-title {{font-size:1.14rem;font-weight:700;color:#f0faff;margin-bottom:.25rem;}}
.glass-sub {{color:#a9c4da;font-size:.9rem;margin-bottom:1.2rem;}}
[data-testid="stVerticalBlockBorderWrapper"] > div {{background:rgba(8,23,49,.70);border:1px solid rgba(91,202,255,.25);border-radius:22px;box-shadow:0 16px 48px rgba(0,0,0,.25),inset 0 1px rgba(255,255,255,.07);backdrop-filter:blur(16px);transition:border-color .3s,box-shadow .3s,transform .3s;}}
[data-testid="stVerticalBlockBorderWrapper"] > div:hover {{border-color:rgba(82,220,255,.57);box-shadow:0 20px 55px rgba(0,0,0,.3),0 0 26px rgba(0,166,255,.09);}}
[data-testid="stTextArea"] textarea, [data-baseweb="select"] > div {{background:rgba(4,16,36,.78)!important;color:#edf8ff!important;border:1px solid #285074!important;border-radius:12px!important;}}
[data-testid="stTextArea"] textarea:focus {{border-color:#4edcff!important;box-shadow:0 0 0 2px rgba(60,210,255,.17)!important;}}
[data-testid="stWidgetLabel"] p {{color:#d8edff!important;font-weight:600;}}
[data-testid="stButton"] button[kind="primary"] {{width:100%;min-height:3.3rem;border-radius:12px;border:1px solid #74e6ff;background:linear-gradient(110deg,#087fc3,#13b9ec);color:white;font-weight:700;font-size:1.05rem;box-shadow:0 7px 26px #008fdc55;transition:transform .22s,box-shadow .22s,filter .22s;}}
[data-testid="stButton"] button[kind="primary"]:hover {{transform:translateY(-3px);box-shadow:0 14px 36px #00b8ff88;filter:brightness(1.15);}}
[data-testid="stButton"] button[kind="primary"]:active {{transform:translateY(0) scale(.99);}}
[data-testid="stAlert"] {{border-radius:14px;}}
[data-testid="stProgressBar"] > div > div {{background:linear-gradient(90deg,#0096dc,#69edff)!important;}}
[data-testid="stMetric"] {{padding:1rem;border:1px solid #275579;border-radius:14px;background:rgba(7,28,55,.55);}}
[data-testid="stMetricValue"] {{color:#83edff;}}
hr {{border-color:#244a6b!important;}}
.note {{font-size:.82rem;color:#94b3cb;margin-top:1.6rem;}}
.model-pill {{display:inline-block;padding:.4rem .8rem;border:1px solid #287aa6;border-radius:50px;background:#0b345caa;color:#9be9ff;font-size:.8rem;font-weight:700;margin-bottom:1.4rem;}}
@media(max-width:720px) {{[data-testid="stMainBlockContainer"] {{padding-top:1.3rem;}} .hero-sub {{font-size:.98rem;}}}}
@media(prefers-reduced-motion:reduce) {{*,*::before,*::after {{animation:none!important;transition:none!important;}}}}
</style>
""", unsafe_allow_html=True)

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

st.markdown('<div class="note">Built with Streamlit · Models hosted on Hugging Face · Predictions are probabilistic and do not guarantee that any message is safe.</div>', unsafe_allow_html=True)
