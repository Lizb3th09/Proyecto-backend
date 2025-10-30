from flask import Flask
from flask import render_template
from flask import jsonify

app = Flask(__name__)


persona = {
    "nombre": "lalo",
    "edad": 22,
    "hobbies": ["programar"]
}

@app.route("/")
def hola_mundo():
    return "<h1>👻 ¡Buuu! Dulce o Puntos 🎃</h1>"

@app.route("/persona")
def personaje_json():
    datos = {
        "nombre": persona["nombre"],
        "edad": persona["edad"],
        "hobbies": ", ".join(persona["hobbies"])
    }
    return jsonify(datos)

@app.route("/invocar")
def mostrar_persona():
    return render_template('pagina.html', person=persona)