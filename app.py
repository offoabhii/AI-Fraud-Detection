import streamlit as st
import joblib
import pandas as pd
import datetime
import sqlite3 # Built-in database

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('fraud_audit.db')
    c = conn.cursor()
    # Create a table to store every check we perform
    c.execute('''CREATE TABLE IF NOT EXISTS logs 
                 (timestamp TEXT, amount REAL, probability REAL, verdict TEXT)''')
    conn.commit()
    conn.close()

def log_prediction(amount, prob, verdict):
    conn = sqlite3.connect('fraud_audit.db')
    c = conn.cursor()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO logs VALUES (?, ?, ?, ?)", (now, amount, prob, verdict))
    conn.commit()
    conn.close()

init_db()

# --- PREVIOUS APP LOGIC ---
st.set_page_config(page_title="AI Fraud Detection", layout="wide")
model = joblib.load('fraud_detection_model.pkl')
scaler = joblib.load('scaler.pkl')

st.title("🛡️ AI Fraud Detection")

# --- IMPROVED INPUT AREA ---
st.subheader("Simulate Transaction Behavior")
col1, col2, col3 = st.columns(3)

with col1:
    amount = st.number_input("Amount ($)", value=100.0)
    v1 = st.slider("V1 (General Pattern)", -15.0, 5.0, 0.0)

with col2:
    v14 = st.slider("V14 (Critical - Integrity)", -15.0, 5.0, 0.0)
    v17 = st.slider("V17 (Critical - Risk)", -15.0, 5.0, 0.0)

with col3:
    v12 = st.slider("V12 (Critical - Trust)", -15.0, 5.0, 0.0)
    v10 = st.slider("V10 (Critical - Velocity)", -15.0, 5.0, 0.0)

if st.button("RUN FRAUD CHECK", type="primary"):
    scaled_amt = scaler.transform([[amount]])[0][0]
    
    # Create the full 30-feature vector
    features = [0.0] * 30
    features[0] = scaled_amt # index 0: scaled_amount
    features[1] = 0.0        # index 1: scaled_time
    features[2] = v1         # index 2: V1
    features[11] = v10       # index 11: V10
    features[13] = v12       # index 13: V12
    features[15] = v14       # index 15: V14
    features[18] = v17       # index 18: V17
    
    prob = model.predict_proba([features])[0][1]
    # In enterprise, we often set a threshold. Let's say > 50% is Fraud.
    verdict = "FRAUD" if prob > 0.5 else "NORMAL"

    # --- SAVE TO DATABASE ---
    log_prediction(amount, prob, verdict)

    if verdict == "FRAUD":
        st.error(f"🚨 ALERT: FRAUD DETECTED ({prob*100:.2f}%)")
    else:
        st.success(f"✅ APPROVED ({prob*100:.2f}%)")

# --- DISPLAY AUDIT TRAIL ---
st.divider()
st.subheader("📋 Real-Time Audit Log (From Database)")
conn = sqlite3.connect('fraud_audit.db')
df_logs = pd.read_sql_query("SELECT * FROM logs ORDER BY timestamp DESC", conn)
st.table(df_logs.head(10)) # Show last 10 transactions
