from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
# Configurar o ChromeDriver automaticamente
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from empresas import empresas_
import os

# Configurar o navegador
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 1️⃣ Acessar a página de login
login_url = "https://radar.farmarcas.com.br/authentication/"  # Substitua pela URL real
driver.get(login_url)

# 2️⃣ Esperar a página carregar
time.sleep(3)

# 3️⃣ Encontrar os campos de login e preencher
usuario = driver.find_element(By.XPATH, "//input[@class='form-input-text ng-untouched ng-pristine ng-valid' and @type='text']") # Ajuste conforme necessário
senha = driver.find_element(By.XPATH, "//input[@class='form-input-text ng-untouched ng-pristine ng-valid' and @type='password']")

usuario.send_keys("29842944832")  # Substitua pelo seu usuário
senha.send_keys("Max1popu!ar")     # Substitua pela sua senha

# 4️⃣ Enviar o formulário (pressionand o Enter)
senha.send_keys(Keys.RETURN)

# 5️⃣ Aguardar login ser processado
time.sleep(5)

# 6️⃣ Verificar se o login foi bem-sucedido
if "dashboard" in driver.current_url:
    print("✅ Login bem-sucedido!")
else:
    print("❌ Falha no login!")

# 7️⃣ Capturar cookies de login

cookies = driver.get_cookies()
time.sleep(2)
for _ in range(1,10):
    pyautogui.press('escape')
time.sleep(0.5)
elemento = driver.find_element(By.XPATH, "//span[text()='Relatórios']")
elemento.click()
time.sleep(3)
elemento = driver.find_element(By.XPATH, "//span[text()=' Bússola']")
elemento.click()

time.sleep(65)
utc = pyautogui.locateCenterOnScreen("utc.png", confidence=0.90)
time.sleep(0.5)
pyautogui.click(utc)
time.sleep(6)

def baixarPorLoja():
    def pressionar_tab(vezes, intervalo=0.5):
        for _ in range(vezes):
            pyautogui.press('tab')
            time.sleep(intervalo)

    pulo_inicial = 20  # índice de início visual e lógico
    primeira_iteracao = True

    for idx, l in enumerate(empresas_):
        if primeira_iteracao and idx < pulo_inicial:
            continue  # Pula os primeiros até alcançar o índice desejado

        caminho = r'C:\Users\Acer\Downloads'
        caminhoAntigo = os.path.join(caminho, 'data.xlsx')
        caminhoNovo = os.path.join(caminho, f'{l}.xlsx')

        if primeira_iteracao:
            print(f"Iniciando com empresa: {l} (índice {idx})")
            pesquisaFiltro = pyautogui.locateCenterOnScreen("pesquisaFiltro.png", confidence=0.80)
            pyautogui.click(pesquisaFiltro)
            time.sleep(1)
            pyautogui.write("PDV")
            pressionar_tab(2, 0.5)
            pyautogui.press('space')
            time.sleep(25)
            pressionar_tab(2, 0.5)

            for _ in range(pulo_inicial):
                pyautogui.press('down')
                time.sleep(0.5)

            pyautogui.press('space')  # Seleciona a empresa atual
            primeira_iteracao = False

        else:
            print(f"Processando empresa: {l} (índice {idx})")
            pesquisaFiltro = pyautogui.locateCenterOnScreen("pesquisaFiltroPDV.png", confidence=0.75)
            pyautogui.click(pesquisaFiltro)
            time.sleep(0.5)
            pressionar_tab(5, 0.5)
            pyautogui.press('down')
            time.sleep(0.5)
            pyautogui.press('space')

        time.sleep(8)
        pyautogui.press('escape')
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'enter')
        time.sleep(0.5)
        pressionar_tab(2, 0.5)
        pyautogui.press('enter')
        time.sleep(0.5)
        for _ in range(1, 15):
            pyautogui.press('tab')
            time.sleep(0.3)

        time.sleep(3)
        btn3pontos = pyautogui.locateCenterOnScreen("botao3pontos.png", confidence=0.75)
        pyautogui.click(btn3pontos)
        time.sleep(1)
        exportar = pyautogui.locateCenterOnScreen("exportar.png", confidence=0.95)
        pyautogui.click(exportar)
        time.sleep(3)
        pressionar_tab(3, 0.5)
        time.sleep(3)
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.press('escape')
        time.sleep(30)

        # Aguarda o download do arquivo
        timeout = 1000
        start_time = time.time()
        while not os.path.exists(caminhoAntigo):
            if time.time() - start_time > timeout:
                print(f"⏰ Timeout esperando arquivo para {l}")
                break

        if os.path.exists(caminhoAntigo):
            try:
                # Garante que o arquivo não está sendo usado
                for _ in range(10):
                    try:
                        with open(caminhoAntigo, 'rb'):
                            break
                    except PermissionError:
                        time.sleep(1)

                os.rename(caminhoAntigo, caminhoNovo)
                print(f"✅ Arquivo renomeado para: {l}.xlsx")
            except Exception as e:
                print(f"❌ Erro ao renomear {l}: {e}")
        else:
            print(f"⚠️ Arquivo {caminhoAntigo} não encontrado para {l}")

        time.sleep(15)

    time.sleep(10)

baixarPorLoja()

# # 🔟 Fechar o navegador
driver.quit()