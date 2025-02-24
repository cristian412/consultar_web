from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "¡Hola, bienvenido al home!"

# Ruta del driver
DRIVER_PATH = '/opt/homebrew/bin/chromedriver'

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

if __name__ == '__main__':
    app.run(debug=True)
