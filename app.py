from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "¡Hola, bienvenido al home!"


@app.route('/buscar', methods=['GET'])
def buscar():
    parametro = request.args.get('q')
    if not parametro:
        return jsonify({"error": "Parámetro 'q' requerido"}), 400

    # Configuración de Selenium
    DRIVER_PATH = '/opt/homebrew/bin/chromedriver'
    service = Service(DRIVER_PATH)
    options = Options()
    options.add_argument("--headless")  # Ejecuta sin abrir el navegador
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Aquí puedes poner otra URL
        driver.get('https://es.wikipedia.org/wiki/{}'.format(parametro))

        # Si es Wikipedia, por ejemplo, podemos buscar el título
        title = driver.find_element(By.CSS_SELECTOR, 'h1').text

        return jsonify({"parametro": parametro, "titulo": title})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        driver.quit()


if __name__ == '__main__':
    app.run(debug=True)
