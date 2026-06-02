import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv

# Cargar las variables del archivo .env al entorno
load_dotenv()

app = Flask(__name__)

# Configuración de Flask-Mail usando variables de entorno
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

# Aquí os.environ.get busca los valores que guardaste en el archivo .env
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

# Configurar una Secret Key para que los mensajes 'flash' funcionen sin romperse
app.secret_key = os.environ.get('SECRET_KEY', 'mi_clave_secreta_local')

mail = Mail(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/mail", methods=["GET","POST"])
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
            # Creamos un mensaje
            msg = Message(
                "Hola Julián, tienes un nuevo contacto desde la web",
                body=f"Nombre. {name} \nCorreo: <{email}>\n\nMensaje: \n\n{message}",
                sender=app.config['MAIL_USERNAME'],
                recipients=[app.config['MAIL_USERNAME']],
                reply_to=email
            )

            mail.send(msg)
            return render_template("send_mail.html")
        
        except Exception as e:
            flash("Hubo un problema al enviar el correo. Inténtalo más tarde.", "danger")
            return redirect(url_for('index'))
    
    # 💥 CORREGIDO: Ahora sí tiene la palabra 'return' para evitar el bloqueo del navegador
    return redirect(url_for('index'))



if __name__ == '__main__':
    # Ejecuta el servidor local en modo desarrollo (debug)
    app.run(debug=True, port=5000)