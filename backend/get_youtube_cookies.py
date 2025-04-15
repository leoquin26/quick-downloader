from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import random

def get_youtube_cookies(username, password, output_file="cookies.txt"):
    # Configura las opciones del navegador
    chrome_options = Options()
    # Desactiva el modo headless para que puedas ver el navegador y resolver CAPTCHAs
    # chrome_options.add_argument("--headless")  # Comenta esta línea para modo visible
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Simula un navegador real con un user-agent común
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36")
    # Usa un perfil de Chrome existente para mantener cookies e historial
    # Reemplaza "C:/Path/To/Your/Chrome/Profile" con la ruta real de tu perfil de Chrome
    # Para encontrar tu perfil, ve a chrome://version/ y busca "Profile Path"
    # chrome_options.add_argument("user-data-dir=C:/Path/To/Your/Chrome/Profile")

    # Inicia el navegador
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager(driver_version="134.0.6998.35").install()),
        options=chrome_options
    )
    wait = WebDriverWait(driver, 15)

    try:
        # Abre la página de inicio de sesión de Google
        driver.get("https://accounts.google.com")
        print("Abriendo página de inicio de sesión de Google...")
        print(f"URL inicial: {driver.current_url}")

        # Ingresa el correo electrónico
        email_field = wait.until(EC.element_to_be_clickable((By.ID, "identifierId")))
        email_field.send_keys(username)
        next_button = wait.until(EC.element_to_be_clickable((By.ID, "identifierNext")))
        driver.execute_script("arguments[0].click();", next_button)
        print("Correo electrónico ingresado. Esperando página de contraseña...")
        print(f"URL después de 'Siguiente': {driver.current_url}")

        # Espera a que la página de contraseña cargue
        try:
            wait.until(EC.url_contains("challenge/pwd") or EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        except Exception as e:
            print("Posible CAPTCHA detectado. Por favor, resuelve el CAPTCHA manualmente en el navegador.")
            print(f"URL actual: {driver.current_url}")
            input("Presiona Enter después de resolver el CAPTCHA y avanzar a la página de contraseña...")

        time.sleep(random.uniform(1, 3))  # Espera aleatoria para simular comportamiento humano

        # Ingresa la contraseña
        password_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password']")))
        driver.execute_script("arguments[0].scrollIntoView(true);", password_field)
        password_field.send_keys(password)
        password_next_button = wait.until(EC.element_to_be_clickable((By.ID, "passwordNext")))
        driver.execute_script("arguments[0].click();", password_next_button)
        print("Contraseña ingresada. Esperando autenticación...")
        print(f"URL después de contraseña: {driver.current_url}")

        # Espera a que la autenticación se complete
        time.sleep(random.uniform(3, 5))

        # Navega a YouTube para obtener las cookies
        driver.get("https://www.youtube.com")
        wait.until(EC.url_contains("youtube.com"))
        print("Navegando a YouTube...")
        print(f"URL de YouTube: {driver.current_url}")

        # Extrae las cookies
        cookies = driver.get_cookies()
        with open(output_file, "w") as f:
            f.write("# Netscape HTTP Cookie File\n")
            f.write("# This file was generated by selenium\n")
            for cookie in cookies:
                secure = "TRUE" if cookie.get("secure") else "FALSE"
                f.write(f"{cookie['domain']}\t{secure}\t{cookie['path']}\tFALSE\t{cookie.get('expiry', '')}\t{cookie['name']}\t{cookie['value']}\n")

        print(f"Cookies guardadas en {output_file}")
        print("Cookies generadas:", cookies)

    except Exception as e:
        print(f"Error al obtener las cookies: {e}")
        print(f"URL actual: {driver.current_url}")
        print("HTML de la página actual para depuración:")
        print(driver.page_source[:2000])
    finally:
        driver.quit()

if __name__ == "__main__":
    # Usa variables de entorno para las credenciales
    USERNAME = "quickfastapi@gmail.com"
    PASSWORD = "leo3347240."
    if not USERNAME or not PASSWORD:
        raise ValueError("Debes definir las variables de entorno YOUTUBE_USERNAME y YOUTUBE_PASSWORD")

    get_youtube_cookies(USERNAME, PASSWORD)