import os
import sys
import requests  # 👈 AGREGADO: Necesario para enviar los datos a Formspree vía HTTPS
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

# Cargar las variables del archivo .env al entorno
base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, '.env'))

app = Flask(__name__)

# Configurar una Secret Key para que los mensajes 'flash' funcionen sin romperse
app.secret_key = os.environ.get('SECRET_KEY', 'mi_clave_secreta_local')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/mail", methods=["GET", "POST"])
def send_mail():
    # Si el método es post capturamos lo que se envía por el form
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        # 1. Validar que no haya campos vacíos
        if not name or not email or not message:
            flash("Todos los campos son obligatorios.", "danger")
            return redirect(url_for('index'))

        # 2. Validar longitud mínima
        if len(name) < 3:
            flash("El nombre debe tener al menos 3 caracteres.", "danger")
            return redirect(url_for('index'))
            
        if len(message) < 10:
            flash("El mensaje debe tener al menos 10 caracteres.", "danger")
            return redirect(url_for('index'))

        # 3. Validación básica de formato de correo
        if "@" not in email or "." not in email:
            flash("Por favor, introduce un correo electrónico válido.", "danger")
            return redirect(url_for('index'))
        
        try:
            # 👈 URL de tu formulario de Formspree
            formspree_url = "https://formspree.io/f/mnjypkey"
            
            # Datos estructurados que Formspree necesita recibir
            data_to_send = {
                "name": name,
                "email": email,
                "message": message
            }
            
            # Enviamos la petición POST de forma segura saltando las restricciones de puertos
            response = requests.post(formspree_url, data=data_to_send)
            
            # Validamos que Formspree haya procesado el formulario con éxito
            if response.status_code == 200:
                return render_template("send_mail.html")
            else:
                raise Exception(f"Formspree respondió con código de estado {response.status_code}")
        
        except Exception as e:
            # Si ocurre algún fallo inesperado, se registrará aquí de forma legible
            print(f"--- DETALLE DEL ERROR DE CORREO: {str(e)} ---", file=sys.stderr)
            flash("Hubo un problema al enviar el correo. Inténtalo más tarde.", "danger")
            return redirect(url_for('index'))
    
    # Mantiene la redirección para evitar congelamientos en peticiones GET accidentales
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Ejecuta el servidor local en modo desarrollo (debug)
    app.run(debug=True, port=5000)
