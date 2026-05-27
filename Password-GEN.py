import streamlit as st
import random
import string
import pyperclip

st.set_page_config(page_title="Password Generator", page_icon="🔐", layout="centered")

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&display=swap');

* { font-family: 'Rajdhani', sans-serif; }

.stApp {
    background: #0a0a0f;
    background-image: radial-gradient(ellipse at 20% 50%, #0d1f3c 0%, transparent 60%),
                      radial-gradient(ellipse at 80% 20%, #1a0a2e 0%, transparent 50%);
}

h1 { 
    font-family: 'Share Tech Mono', monospace !important;
    color: #00ff88 !important;
    text-shadow: 0 0 20px #00ff8866;
    letter-spacing: 3px;
}

.password-box {
    background: #0d1117;
    border: 1px solid #00ff8844;
    border-radius: 8px;
    padding: 24px 20px;
    margin: 20px 0;
    font-family: 'Share Tech Mono', monospace;
    font-size: 22px;
    color: #00ff88;
    text-align: center;
    letter-spacing: 4px;
    word-break: break-all;
    box-shadow: 0 0 30px #00ff8822, inset 0 0 20px #00000066;
}

.strength-bar-wrap {
    background: #1a1a2e;
    border-radius: 4px;
    height: 8px;
    margin: 8px 0 4px 0;
    overflow: hidden;
}

.strength-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 13px;
    margin-bottom: 16px;
}

.stat-card {
    background: #0d1117;
    border: 1px solid #ffffff11;
    border-radius: 8px;
    padding: 14px;
    text-align: center;
    color: #aaaaaa;
    font-family: 'Share Tech Mono', monospace;
    font-size: 12px;
}

.stat-val {
    font-size: 20px;
    color: #00ff88;
    display: block;
    margin-bottom: 4px;
}

div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #00ff88, #00cc66) !important;
    color: #0a0a0f !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    letter-spacing: 2px !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 12px 24px !important;
    width: 100% !important;
    transition: all 0.2s !important;
}

div[data-testid="stButton"] button:hover {
    box-shadow: 0 0 20px #00ff8866 !important;
    transform: translateY(-1px) !important;
}

.stSlider label, .stCheckbox label, .stSelectbox label {
    color: #aaaaaa !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 15px !important;
    letter-spacing: 1px !important;
}

section[data-testid="stSidebar"] {
    background: #0d1117 !important;
    border-right: 1px solid #00ff8822 !important;
}

.footer {
    text-align: center;
    font-family: 'Share Tech Mono', monospace;
    color: #00ff8866;
    font-size: 13px;
    margin-top: 40px;
    letter-spacing: 2px;
}
</style>
""", unsafe_allow_html=True)

# ── Title ─────────────────────────────────────────────────────────────────────
st.markdown("# 🔐 PASSWORD GENERATOR")
st.markdown("<p style='color:#666; font-family:Share Tech Mono,monospace; letter-spacing:2px; font-size:13px;'>SECURE • RANDOM • INSTANT</p>", unsafe_allow_html=True)
st.divider()

# ── Settings ──────────────────────────────────────────────────────────────────
col_s1, col_s2 = st.columns(2)

with col_s1:
    length = st.slider("🔢 Password Length", 6, 64, 16, 1)
    use_upper  = st.checkbox("🔠 Uppercase (A-Z)",     value=True)
    use_lower  = st.checkbox("🔡 Lowercase (a-z)",     value=True)

with col_s2:
    count = st.slider("📋 Number of Passwords", 1, 10, 1, 1)
    use_digits = st.checkbox("🔢 Digits (0-9)",         value=True)
    use_symbols= st.checkbox("✳️ Symbols (!@#$...)",    value=False)

# Excluded characters
exclude = st.text_input("🚫 Exclude characters (optional)", placeholder="e.g. 0Ol1I")

st.divider()

# ── Generator ─────────────────────────────────────────────────────────────────
def build_charset(upper, lower, digits, symbols, exclude_chars):
    charset = ""
    if upper:   charset += string.ascii_uppercase
    if lower:   charset += string.ascii_lowercase
    if digits:  charset += string.digits
    if symbols: charset += string.punctuation
    for ch in exclude_chars:
        charset = charset.replace(ch, "")
    return charset

def generate_password(charset, length):
    if not charset:
        return None
    # Guarantee at least one char from each selected group
    pwd = [random.choice(charset)]
    pwd += [random.SystemRandom().choice(charset) for _ in range(length - 1)]
    random.shuffle(pwd)
    return "".join(pwd)

def password_strength(pwd):
    score = 0
    if len(pwd) >= 8:  score += 1
    if len(pwd) >= 12: score += 1
    if len(pwd) >= 16: score += 1
    if any(c.isupper() for c in pwd): score += 1
    if any(c.islower() for c in pwd): score += 1
    if any(c.isdigit() for c in pwd): score += 1
    if any(c in string.punctuation for c in pwd): score += 1

    if score <= 2:   return "WEAK",   "#ff4444", 20
    elif score <= 4: return "FAIR",   "#ffaa00", 45
    elif score <= 5: return "GOOD",   "#88cc00", 70
    else:            return "STRONG", "#00ff88", 100

# ── Generate button ───────────────────────────────────────────────────────────
if st.button("⚡ GENERATE PASSWORD"):
    charset = build_charset(use_upper, use_lower, use_digits, use_symbols, exclude)

    if not charset:
        st.error("⚠️ Please select at least one character type!")
    else:
        passwords = [generate_password(charset, length) for _ in range(count)]

        for i, pwd in enumerate(passwords):
            label, color, pct = password_strength(pwd)

            if count > 1:
                st.markdown(f"<p style='color:#555; font-family:Share Tech Mono,monospace; font-size:12px; margin-bottom:4px;'>PASSWORD {i+1}</p>", unsafe_allow_html=True)

            st.markdown(f"<div class='password-box'>{pwd}</div>", unsafe_allow_html=True)

            # Strength bar
            st.markdown(f"""
            <div class='strength-bar-wrap'>
                <div style='height:100%; width:{pct}%; background:{color}; border-radius:4px; transition:width 0.4s;'></div>
            </div>
            <p class='strength-label' style='color:{color};'>STRENGTH: {label}</p>
            """, unsafe_allow_html=True)

            if count > 1:
                st.divider()

        # ── Stats ─────────────────────────────────────────────────────────────
        if count == 1:
            pwd = passwords[0]
            import math
            entropy = length * math.log2(len(charset)) if charset else 0

            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown(f"<div class='stat-card'><span class='stat-val'>{length}</span>CHARS</div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div class='stat-card'><span class='stat-val'>{len(charset)}</span>POOL SIZE</div>", unsafe_allow_html=True)
            with c3:
                st.markdown(f"<div class='stat-card'><span class='stat-val'>{entropy:.0f}</span>BITS ENTROPY</div>", unsafe_allow_html=True)
            with c4:
                st.markdown(f"<div class='stat-card'><span class='stat-val'>{'✅' if entropy >= 60 else '⚠️'}</span>{'SAFE' if entropy >= 60 else 'WEAK'}</div>", unsafe_allow_html=True)

st.divider()
st.markdown("<p class='footer'>Developed by 𝑆𝑝𝑒𝑒𝑒𝑒𝑐𝑡𝑟𝑎 X</p>", unsafe_allow_html=True)