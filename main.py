from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import firebase_admin
from firebase_admin import credentials, firestore
import time
from fastapi import FastAPI
import uvicorn

app = FastAPI()

cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "app-hospede",
    "private_key_id": "dummy",
    "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk@app-hospede.iam.gserviceaccount.com",
    "client_id": "dummy",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk"
})
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.post("/executar-robo")
def executar_robo():
    doc_ref = db.collection("reservas").document("temporario_2025-06-09")
    doc = doc_ref.get()
    if not doc.exists:
        return {"erro": "Documento não encontrado"}

    dados = doc.to_dict()
    nome = dados.get("nome", "")
    data_inicial = dados.get("dataCheckin", "")
    data_final = dados.get("dataCheckout", "")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get("https://app.econdos.com.br/login")

    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, 'input[data-testid="login-username-input"]').send_keys("tiagoddantas@me.com")
    driver.find_element(By.CSS_SELECTOR, 'input[data-testid="login-password-input"]').send_keys("Web12345")
    driver.find_element(By.CSS_SELECTOR, 'button[data-testid="login-submit-button"]').click()

    time.sleep(5)
    driver.get("https://app.econdos.com.br/feed/gate")
    time.sleep(3)

    driver.find_element(By.CSS_SELECTOR, 'button[data-testid="feed-open-liberation-modal-button"]').click()
    time.sleep(2)

    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Ex: Diarista, personal trainer, churrasco, etc"]').send_keys(nome)
    driver.find_element(By.CSS_SELECTOR, 'input[data-testid="create-authorized-person-start-date-input"]').send_keys(data_inicial)
    driver.find_element(By.CSS_SELECTOR, 'input[data-testid="create-authorized-person-end-date-input"]').send_keys(data_final)

    driver.find_element(By.CSS_SELECTOR, 'button[data-testid="create-authorized-person-submit-button"]').click()
    time.sleep(3)

    driver.quit()
    return {"status": "ok", "mensagem": "Robô executado com sucesso"}
