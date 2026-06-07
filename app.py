import os
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


# 👈 MODIFICADO: Esta ruta ahora solo se encarga de mostrar la pantalla de éxito
# cuando Formspree redirige al usuario después de enviar el mensaje.
@app.route("/mail", methods=["GET", "POST"])
def send_mail():
    return render_template("send_mail.html")


if __name__ == '__main__':
    # Ejecuta el servidor local en modo desarrollo (debug)
    app.run(debug=True, port=5000)

