from flask import Flask, render_template, request, session, redirect, url_for
from random import shuffle

app = Flask(__name__)
app.secret_key = "clave_secreta"

preguntas = [
    ("¿Quién es la protagonista principal de la serie?",
     ["Rainbow Dash", "Twilight Sparkle", "Pinkie Pie", "Fluttershy"],
     "Twilight Sparkle"),

    ("¿Cuál es el elemento de la armonía de Applejack?",
     ["Generosidad", "Honestidad", "Lealtad", "Bondad"],
     "Honestidad"),

    ("¿Qué mascota tiene Fluttershy?",
     ["Un búho", "Un conejo", "Un cocodrilo", "Una tortuga"],
     "Un conejo"),

    ("¿Qué pone especial a Pinkie Pie?",
     ["Su velocidad", "Su magia", "Su alegria", "Su fuerza"],
     "Su alegria"),

    ("¿Quién es la princesa que gobierna el día?",
     ["Princesa Luna", "Princesa Candance", "Princesa Celestia", "Reina Chrysalis"],
     "Princesa Celestia"),

    ("¿Cuál es el talento especial de Rainbow Dash?",
     ["Cocinar", "Volar muy rápido", "Hacer vestidos", "Cantar"],
     "Volar muy rápido"),

    ("¿Qué hace Rarity como profesión?",
     ["Pastelera", "Diseñadora de modas", "Maestra", "Jardinera"],
     "Diseñadora de modas"),

    ("¿Cómo se llama el dragón bebé que acompaña a Twilight Sparkle?",
     ["Smolder", "Garble", "Spike", "Ember"],
     "Spike"),

    ("¿Cuál es el elemento de la armonía de Rainbow Dash?",
     ["Generosidad", "Magia", "Lealtad", "Honestidad"],
     "Lealtad"),

    ("¿En qué pueblo viven principalmente las protagonistas?",
     ["Manehattan", "Ponyville", "Canterlot", "Cloudsdale"],
     "Ponyville"),
]


@app.route("/")
def inicio():
    session["i"] = 0
    session["puntaje"] = 0
    return redirect(url_for("pregunta"))


@app.route("/pregunta", methods=["GET", "POST"])
def pregunta():
    i = session.get("i", 0)
    puntaje = session.get("puntaje", 0)

    if i >= len(preguntas):
        return redirect(url_for("resultado"))

    pregunta_actual, opciones, correcta = preguntas[i]

    opciones = opciones[:]
    shuffle(opciones)

    if request.method == "POST":
        respuesta = request.form["respuesta"]

        if respuesta == correcta:
            puntaje += 1
            session["puntaje"] = puntaje

        session["i"] = i + 1
        return redirect(url_for("pregunta"))

    return render_template(
        "pregunta.html",
        pregunta=pregunta_actual,
        opciones=opciones,
        numero=i + 1,
        total=len(preguntas)
    )


@app.route("/resultado")
def resultado():
    puntaje = session.get("puntaje", 0)
    total = len(preguntas)

    porcentaje = (puntaje / total) * 100

    if porcentaje == 100:
        mensaje = "¡Excelente!"
    elif porcentaje >= 60:
        mensaje = "Muy bien."
    else:
        mensaje = "Necesitás practicar más."

    return render_template(
        "resultado.html",
        puntaje=puntaje,
        total=total,
        mensaje=mensaje
    )


if __name__ == "__main__":
    app.run(debug=True)
