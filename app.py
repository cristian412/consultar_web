from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Ruta del driver
DRIVER_PATH = '/ruta/al/chromedriver'

@app.route('/buscar', methods=['GET'])
def buscar():
    parametro = request.args.get('q')
    if not parametro:
        return jsonify({"error": "Parámetro 'q' requerido"}), 400

    # Configuración de Selenium
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Ejecuta sin abrir el navegador
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)

    try:
        # Acceder a Google
        driver.get('https://www.google.com')
        search_box = driver.find_element(By.NAME, 'q')
        search_box.send_keys(parametro + Keys.RETURN)

        # Extraer el primer resultado
        result = driver.find_element(By.CSS_SELECTOR, 'h3').text

        return jsonify({"parametro": parametro, "resultado": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True)
