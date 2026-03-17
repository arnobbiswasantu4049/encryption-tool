import streamlit as st
from cryptography.fernet import Fernet
import base64
import hashlib
import datetime
import qrcode
from io import BytesIO
import streamlit.components.v1 as components
import time

st.set_page_config(page_title="Encryption Tool", page_icon="💀", layout="centered")

if "key" not in st.session_state:
    st.session_state.key = Fernet.generate_key()
if "history" not in st.session_state:
    st.session_state.history = []
if "show_qr" not in st.session_state:
    st.session_state.show_qr = None
if "result" not in st.session_state:
    st.session_state.result = None

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

    * { font-family: 'Share Tech Mono', monospace !important; }

    .stApp { background: #000000; }

    h1 {
        text-align: center;
        color: #00ff41 !important;
        font-size: 2.8rem !important;
        text-shadow: 0 0 10px #00ff41, 0 0 30px #00ff41, 0 0 60px #00ff41;
        letter-spacing: 6px;
        -webkit-text-fill-color: #00ff41 !important;
    }

    .card {
        background: #000000;
        border: 1px solid #00ff41;
        border-radius: 4px;
        padding: 18px;
        margin: 10px 0;
        color: #00ff41;
        box-shadow: 0 0 10px rgba(0,255,65,0.3), inset 0 0 10px rgba(0,255,65,0.05);
    }

    .stButton>button {
        width: 100%;
        background: transparent;
        color: #00ff41;
        border: 1px solid #00ff41;
        border-radius: 2px;
        padding: 12px;
        font-weight: bold;
        font-size: 1rem;
        letter-spacing: 3px;
        box-shadow: 0 0 10px rgba(0,255,65,0.3);
        transition: all 0.3s ease;
    }
   .stButton>button:hover {
    background: #003b00 !important;
    color: #00ff41 !important;
    box-shadow: 0 0 20px rgba(0,255,65,0.8) !important;
    border: 1px solid #00ff41 !important;
}

.stButton>button:active, .stButton>button:focus {
    background: #003b00 !important;
    color: #00ff41 !important;
    box-shadow: 0 0 20px rgba(0,255,65,0.8) !important;
}

    .stTextArea textarea, .stTextInput input {
        background: #000000 !important;
        color: #00ff41 !important;
        border: 1px solid #00ff41 !important;
        border-radius: 2px !important;
        font-family: 'Share Tech Mono', monospace !important;
        box-shadow: 0 0 8px rgba(0,255,65,0.2) !important;
    }

    .stSelectbox > div > div {
        background: #000000 !important;
        color: #00ff41 !important;
        border: 1px solid #00ff41 !important;
    }

    .stRadio label, label, p, .stCaption {
        color: #00ff41 !important;
    }

    .stCode, code, pre {
        background: #000000 !important;
        color: #00ff41 !important;
        border: 1px solid #00ff41 !important;
        box-shadow: 0 0 8px rgba(0,255,65,0.2) !important;
    }

    .stTabs [data-baseweb="tab"] {
        color: #00ff41 !important;
        background: transparent !important;
        border-bottom: 1px solid #00ff41 !important;
        letter-spacing: 2px;
    }
   .stTabs [aria-selected="true"] {
    background: #003b00 !important;
    color: #00ff41 !important;
    border: 1px solid #00ff41 !important;
    box-shadow: 0 0 10px rgba(0,255,65,0.5) !important;
}

    .stSuccess {
        background: transparent !important;
        border: 1px solid #00ff41 !important;
        color: #00ff41 !important;
    }
    .stWarning {
        background: transparent !important;
        border: 1px solid #ffff00 !important;
        color: #ffff00 !important;
    }
    .stError {
        background: transparent !important;
        border: 1px solid #ff0000 !important;
        color: #ff0000 !important;
    }
    .stInfo {
        background: transparent !important;
        border: 1px solid #00ff41 !important;
        color: #00ff41 !important;
    }

    .stSlider > div > div {
        color: #00ff41 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #00ff41 !important;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in { animation: fadeIn 0.5s ease forwards; }

    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }
    .cursor::after {
        content: '_';
        animation: blink 1s infinite;
        color: #00ff41;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .spinner {
        width: 36px; height: 36px;
        border: 3px solid #003b00;
        border-top: 3px solid #00ff41;
        border-radius: 50%;
        animation: spin 0.7s linear infinite;
        margin: 16px auto;
    }

    .stFileUploader {
        border: 1px dashed #00ff41 !important;
        background: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Matrix rain background
components.html("""
    <canvas id="matrix" style="position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;opacity:0.13;"></canvas>
    <script>
        const canvas = document.getElementById('matrix');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        const chars = '01アイウエオカキクケコABCDEFGHIJKLMNOP@#$%&';
        const cols = Math.floor(canvas.width / 16);
        const drops = Array(cols).fill(1);
        function draw() {
            ctx.fillStyle = 'rgba(0,0,0,0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#00ff41';
            ctx.font = '14px monospace';
            drops.forEach((y, i) => {
                const ch = chars[Math.floor(Math.random() * chars.length)];
                ctx.fillText(ch, i * 16, y * 16);
                if (y * 16 > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            });
        }
        setInterval(draw, 50);
    </script>
""", height=0)

st.markdown('<h1 class="cursor">// ENCRYPTION TOOL</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;color:#00ff41;letter-spacing:4px;font-size:0.8rem;">[ SECURE TERMINAL v1.0 ]</p>', unsafe_allow_html=True)

def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=6, border=3)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#00ff41", back_color="black")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

def show_confetti():
    components.html("""
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
        <script>
            confetti({
                particleCount: 100,
                spread: 70,
                origin: { y: 0.6 },
                colors: ['#00ff41', '#003b00', '#00cc33']
            });
        </script>
    """, height=0)

tab1, tab2, tab3 = st.tabs(["[ KEY / TEXT ]", "[ FILE ]", "[ HISTORY ]"])

with tab1:
    st.markdown("### > ENCRYPTION KEY")
    key_option = st.radio("Key Mode:", ["Auto-generated Key", "Custom Key"], horizontal=True)

    if key_option == "Custom Key":
        custom_input = st.text_input("Enter your password/key:")
        if custom_input:
            hashed = hashlib.sha256(custom_input.encode()).digest()
            st.session_state.key = base64.urlsafe_b64encode(hashed)
            st.success(">> CUSTOM KEY SET")
            st.code(st.session_state.key.decode())
    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.code(st.session_state.key.decode())
        with col2:
            if st.button("[REGENERATE]"):
                st.session_state.key = Fernet.generate_key()
                st.session_state.show_qr = None
                st.session_state.result = None
                st.rerun()

    cipher = Fernet(st.session_state.key)

    st.markdown("---")
    st.markdown("### > METHOD")
    method = st.selectbox("Select Algorithm:", ["Fernet (Symmetric)", "Caesar Cipher"])

    msg = st.text_area("Input Message:")
    st.caption(f">> CHAR COUNT: {len(msg)}")

    action = st.selectbox("Action:", ["Encrypt", "Decrypt"])

    if method == "Caesar Cipher":
        shift = st.slider("Shift Value:", 1, 25, 3)
        if action == "Decrypt":
            st.info(f">> Use same shift value: {shift}")

    if st.button("[ EXECUTE ]"):
        if not msg.strip():
            st.warning(">> ERROR: No input detected")
        else:
            spinner_placeholder = st.empty()
            spinner_placeholder.markdown('<div class="spinner"></div>', unsafe_allow_html=True)
            time.sleep(0.8)
            spinner_placeholder.empty()

            result = ""
            try:
                if method == "Fernet (Symmetric)":
                    if action == "Encrypt":
                        result = cipher.encrypt(msg.encode()).decode()
                    else:
                        result = cipher.decrypt(msg.encode()).decode()
                elif method == "Caesar Cipher":
                    for ch in msg:
                        if ch.isalpha():
                            base = ord('A') if ch.isupper() else ord('a')
                            s = shift if action == "Encrypt" else -shift
                            result += chr((ord(ch) - base + s) % 26 + base)
                        else:
                            result += ch

                if result:
                    st.session_state.result = result
                    st.session_state.show_qr = None
                    if action == "Encrypt":
                        show_confetti()
                    st.session_state.history.append({
                        "time": datetime.datetime.now().strftime("%H:%M:%S"),
                        "method": method,
                        "action": action,
                        "input": msg[:30] + "..." if len(msg) > 30 else msg,
                        "output": result[:30] + "..." if len(result) > 30 else result
                    })

            except Exception as e:
                st.error(f">> ERROR: {e}")

    if st.session_state.result:
        st.markdown(f"""
            <div class="fade-in card">
                >> OUTPUT:<br><br>
                <code style="word-break:break-all;color:#00ff41;">{st.session_state.result}</code>
            </div>
        """, unsafe_allow_html=True)
        st.code(st.session_state.result)

        col_dl, col_qr = st.columns(2)
        with col_dl:
            st.download_button("[ DOWNLOAD .TXT ]", data=st.session_state.result,
                               file_name="result.txt", mime="text/plain")
        with col_qr:
            if st.button("[ GENERATE QR ]"):
                st.session_state.show_qr = st.session_state.result
                st.rerun()

        if st.session_state.show_qr:
            if len(st.session_state.show_qr) > 500:
                st.warning(">> ERROR: Message too long for QR")
            else:
                qr_buf = generate_qr(st.session_state.show_qr)
                st.markdown('<div class="fade-in">', unsafe_allow_html=True)
                st.image(qr_buf, caption=">> QR CODE", width=200)
                st.markdown('</div>', unsafe_allow_html=True)
                st.download_button("[ DOWNLOAD QR ]", data=qr_buf,
                                   file_name="qr.png", mime="image/png")

with tab2:
    st.markdown("### > FILE ENCRYPTION")
    uploaded = st.file_uploader("Upload .txt file:", type=["txt"])
    file_action = st.selectbox("File Action:", ["Encrypt File", "Decrypt File"])

    if uploaded and st.button("[ PROCESS FILE ]"):
        cipher = Fernet(st.session_state.key)
        content = uploaded.read()
        spinner_placeholder = st.empty()
        spinner_placeholder.markdown('<div class="spinner"></div>', unsafe_allow_html=True)
        time.sleep(0.8)
        spinner_placeholder.empty()
        try:
            if file_action == "Encrypt File":
                output = cipher.encrypt(content)
                st.success(">> FILE ENCRYPTED SUCCESSFULLY")
                show_confetti()
                st.download_button("[ DOWNLOAD ENCRYPTED FILE ]", output, "encrypted.txt")
            else:
                output = cipher.decrypt(content)
                st.success(">> FILE DECRYPTED SUCCESSFULLY")
                st.download_button("[ DOWNLOAD DECRYPTED FILE ]", output, "decrypted.txt")
        except Exception as e:
            st.error(f">> ERROR: {e}")

with tab3:
    st.markdown("### > OPERATION HISTORY")
    if not st.session_state.history:
        st.info(">> NO RECORDS FOUND")
    else:
        if st.button("[ CLEAR HISTORY ]"):
            st.session_state.history = []
            st.rerun()
        for i, item in enumerate(reversed(st.session_state.history)):
            st.markdown(f"""
                <div class="fade-in card">
                    <strong style="color:#00ff41;">#{len(st.session_state.history)-i}</strong> &nbsp;
                    >> {item['time']} | {item['method']} | {item['action']}<br><br>
                    <small>>> INPUT:  {item['input']}</small><br>
                    <small>>> OUTPUT: {item['output']}</small>
                </div>
            """, unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
    <div style="text-align:center; color:#00ff41; font-family:'Share Tech Mono',monospace; padding:20px;">
        <p style="letter-spacing:2px;">[ DEVELOPER ]</p>
        <p style="font-size:1.1rem; text-shadow:0 0 8px #00ff41;">Arnob Biswas Antu</p>
        <p style="font-size:0.85rem; color:#00cc33; letter-spacing:1px;">
            National Institute of Textile Engineering & Research
        </p>
        <p style="margin-top:12px;">
            <a href="https://github.com/arnobbiswasantu4049" target="_blank"
               style="color:#00ff41; text-decoration:none; margin:0 10px;">
               [ GitHub ]
            </a>
            <a href="mailto:arnobbiswasantuncs13@gmail.com"
               style="color:#00ff41; text-decoration:none; margin:0 10px;">
               [ Email ]
            </a>
            <a href="https://wa.me/8801780286280" target="_blank"
               style="color:#00ff41; text-decoration:none; margin:0 10px;">
               [ WhatsApp ]
            </a>
        </p>
    </div>
""", unsafe_allow_html=True)