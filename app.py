from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import json
from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "¡Hola, bienvenido al home!"

# Ruta del driver
#DRIVER_PATH = '/opt/homebrew/bin/chromedriver'
DRIVER_PATH = './venv/bin/chromedriver'


@app.route('/buscar', methods=['GET'])
def buscar():
    parametro = request.args.get('q')
    if not parametro:
        return jsonify({"error": "Parámetro 'q' requerido"}), 400

    # Configuración de Selenium
    service = Service(DRIVER_PATH)
    options = Options()
    options.add_argument("--headless")  # Ejecuta sin abrir el navegador
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Aquí puedes poner otra URL, en este caso usando Google
        driver.get('https://es.m.wikipedia.org/wiki/'+parametro)
        # Extraer el primer resultado
        result = driver.find_element(By.CSS_SELECTOR, 'h1').text

        return jsonify({"parametro": parametro, "resultado": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        driver.quit()

@app.route('/actualizar', methods=['GET'])
def actualizar_chromedriver():
    try:
        subprocess.run([
            "wget", "https://storage.googleapis.com/chrome-for-testing-public/133.0.0.0/linux64/chromedriver-linux64.zip",
            "-O", "chromedriver.zip"
        ], check=True)

        subprocess.run(["unzip", "chromedriver.zip"], check=True)
        subprocess.run(["mv", "chromedriver-linux64/chromedriver", CHROMEDRIVER_PATH], check=True)
        subprocess.run(["chmod", "+x", CHROMEDRIVER_PATH], check=True)
        return jsonify({"message": "Chromedriver actualizado correctamente"}), 200
        
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Error al actualizar chromedriver: {e}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
