import time
import pyautogui
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from empresas import empresas_

# Configurar navegador
def iniciar_driver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Esperar imagem na tela com timeout
def esperar_imagem(nome_arquivo, timeout=60, confidence=0.90):
    fim = time.time() + timeout
    while time.time() < fim:
        pos = pyautogui.locateCenterOnScreen(nome_arquivo, confidence=confidence)
        if pos:
            print(f"{nome_arquivo} encontrado.")
            return pos
        time.sleep(1)
    print(f"❌ Timeout: {nome_arquivo} não encontrado.")
    return None

# Realizar login
def login(driver, usuario, senha):
    driver.get("https://radar.farmarcas.com.br/authentication/")
    time.sleep(3)
    try:
        user_input = driver.find_element(By.XPATH, "//input[@type='text']")
        pass_input = driver.find_element(By.XPATH, "//input[@type='password']")
        user_input.send_keys(usuario)
        pass_input.send_keys(senha)
        pass_input.send_keys(Keys.RETURN)
        time.sleep(5)
        if "dashboard" in driver.current_url:
            print("Login realizado com sucesso.")
            return True
        else:
            print("Falha no login.")
            return False
    except Exception as e:
        print("Erro ao logar:", e)
        return False

# Pressionar várias vezes TAB
def pressionar_tab(n=1, intervalo=0.3):
    for _ in range(n):
        pyautogui.press('tab')
        time.sleep(intervalo)

# Função principal
def principal():
    driver = iniciar_driver()
    if not login(driver, "29842944832", "Max1popu!ar"):
        driver.quit()
        return

    pyautogui.press('escape', presses=10)
    time.sleep(1)
    try:
        driver.find_element(By.XPATH, "//span[text()='Relatórios']").click()
        time.sleep(4)
        driver.find_element(By.XPATH, "//span[text()=' Bússola']").click()
    except Exception as e:
        print("Erro ao navegar para Bússola:", e)
        driver.quit()
        return

    # Interações com PyAutoGUI
    utc = esperar_imagem("utc.png")
    if not utc:
        driver.quit()
        return
    pyautogui.click(utc)
    time.sleep(5)

    filtro = esperar_imagem("pesquisaFiltro.png")
    if not filtro:
        driver.quit()
        return

    pyautogui.click(filtro)
    pyautogui.write("PDV")
    pressionar_tab(2)
    pyautogui.press("space")

    if not esperar_imagem("caixaSelecao.png", confidence=0.9):
        driver.quit()
        return

    pressionar_tab(2)
    pyautogui.press("space")  # Seleciona caixa

    time.sleep(15)
    pyautogui.press("escape")
    pyautogui.hotkey("ctrl", "enter")
    pressionar_tab(2)
    pyautogui.press("enter")

    pressionar_tab(14)

    btn3pontos = esperar_imagem("botao3pontos.png")
    exportar = esperar_imagem("exportar.png")
    layout = esperar_imagem("layoutAtual.png")
    exportarBTN = esperar_imagem("exportarBTN.png")

    if not all([btn3pontos, exportar, layout, exportarBTN]):
        driver.quit()
        return

    for btn in [btn3pontos, exportar, layout, exportarBTN]:
        pyautogui.click(btn)
        time.sleep(1)

    pyautogui.press("escape")

    if esperar_imagem("exportacaoConcluida.png", timeout=100, confidence=0.8):
        print("Exportação concluída com sucesso.")
    else:
        print("Exportação não foi concluída.")

    driver.quit()

if __name__ == "__main__":
    principal()
