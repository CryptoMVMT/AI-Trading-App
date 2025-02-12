import streamlit as st
import pandas as pd
import requests
import openai

# Imposta la tua API Key di OpenAI
openai.api_key = "proj_DLPZuj4NRSECTZJDEtHesRUV"

# Funzione per comunicare con Aurius
def chat_with_aurius(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Sei Aurius, l'AI personale di Daniele."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# Configurazione dell'App
st.set_page_config(page_title="AI Trading App", layout="wide")

st.title("AI Trading App - Monitoraggio e Operazioni in Tempo Reale")

# Chat con Aurius
st.header("Aurius - La tua AI Trading Partner")
with st.expander("Chat con Aurius"):
    user_input = st.text_input("Scrivi un messaggio a Aurius:")
    if st.button("Invia"):
        response = chat_with_aurius(user_input)
        st.write(f"Aurius: {response}")

# Placeholder per i dati di mercato
st.header("Dati di Mercato in Tempo Reale")
market_data_placeholder = st.empty()

# Funzione per recuperare dati di mercato (Simulazione)
def get_market_data():
    return {
        "BTC/USDT": requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd").json()["bitcoin"]["usd"],
        "ETH/USDT": requests.get("https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd").json()["ethereum"]["usd"],
        "ADA/USDT": requests.get("https://api.coingecko.com/api/v3/simple/price?ids=cardano&vs_currencies=usd").json()["cardano"]["usd"]
    }

# Aggiornamento dei dati di mercato
if st.button("Aggiorna Dati di Mercato"):
    market_data = get_market_data()
    market_data_placeholder.write(pd.DataFrame(market_data.items(), columns=["Coppia", "Prezzo USDT"]))

# Sezione per operazioni AI
st.header("Operazioni AI")
operation_type = st.selectbox("Seleziona il tipo di operazione", ["Compra", "Vendi"])
crypto_pair = st.selectbox("Seleziona la coppia", ["BTC/USDT", "ETH/USDT", "ADA/USDT"])
amount = st.number_input("Quantità", min_value=0.01, step=0.01)

if st.button("Esegui Operazione"):
    st.success(f"Operazione AI eseguita: {operation_type} {amount} di {crypto_pair}")
    # Qui si può integrare il codice per eseguire effettivamente l'operazione tramite API dell'exchange

# Monitoraggio delle operazioni
st.header("Storico Operazioni")
operation_log = pd.read_csv("operation_history.csv") if "operation_history.csv" in st.session_state else pd.DataFrame({
    "Coppia": ["BTC/USDT", "ETH/USDT"],
    "Tipo": ["Compra", "Vendi"],
    "Quantità": [0.1, 1.5],
    "Prezzo": [40000, 2500]
})
st.write(operation_log)

# Salvare lo storico delle operazioni per riferimento futuro
operation_log.to_csv("operation_history.csv", index=False)
