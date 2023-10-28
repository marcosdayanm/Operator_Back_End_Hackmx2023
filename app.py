import os
import datetime

import assemblyai as aai
# import tempfile
# import shutil

# API's de texto
from werkzeug.utils import secure_filename
import nlpcloud

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, jsonify
from flask_cors import CORS
# from werkzeug.security import check_password_hash, generate_password_hash

# Nuestra librería
from relations import patrons



# Configure application
app = Flask(__name__)
# SOlving CORS between React and Flask
CORS(app, resources={r"/*": {"origins": "*"}})


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///calls.db")

# set the API key of the voice to text API
aai.settings.api_key = "c950ebc8b23b44cb94542fd711551364" # API key de Diego Abdo
config = aai.TranscriptionConfig(language_detection=True)
transcriber = aai.Transcriber(config=config)


# set API key of summarizing API
client = nlpcloud.Client(
    "finetuned-llama-2-70b", "573541c8e1266a659e108b988756a527f4322a45", gpu=True # API key de jose
)

# client = nlpcloud.Client(
#     "finetuned-llama-2-70b", "5c3c6968618c8265a327c8a39004f9beb7764bd7", gpu=True # API key de marcos
# )


# ésta ruta va a jalar la grabación, transformarla a texto, sacar las keywords y la acción en caso de que haya, meter todo a un sql, mandar a front el texto en string y la lista de keywords
@app.route("/call", methods=["GET", "POST"])
def call():

    # Si se accede con la ruta de la página
    if request.method == "POST":
    
        audio_file = request.files["audio"]
        if audio_file:

            ahora = datetime.datetime.now()

            # Formatear la información de fecha y hora en una cadena de texto
            fecha = ahora.strftime("%Y_%B_%d_%A_%H_%M_%S") # Año, Mes, Día, Día de la semana, Hora
            dmy = ahora.strftime("%d/%m/%Y")
            hms = ahora.strftime("%H_%M_%S")
            
            filename = secure_filename(audio_file.filename)
            filepath = os.path.join("audios", fecha + '.mp3')

            audio_file.save(filepath)
            transcript = transcriber.transcribe(filepath)

            trans = transcript.text
            lowertrans = trans.lower()


            # Insertar las relaciones en el SQL de calls en su respectiva fila (EN LA COLUMNA PELIGRO)
            keys, peligrosql, prioritysql = patrons(lowertrans) # regresa 3 elementos

            # Summary in string format
            summary = client.summarization(trans)["summary_text"]


            db.execute(
                "INSERT INTO calls (fecha, hora, filename, fileroute, transcript, peligro, priority, summary) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                dmy, # fecha
                hms, # hora
                filename, # filename
                filepath, # fileroute
                trans, # transcript en lowercase
                peligrosql, # peligro (popup)
                prioritysql, # priority (número)
                summary

            )
            
            # seleccionar el peligro y la prioridad
            popup =  db.execute("SELECT peligro FROM calls WHERE transcript=? AND fecha=? AND hora=?", trans, dmy, hms)
            priority =  db.execute("SELECT priority FROM calls WHERE transcript=? AND fecha=? AND hora=?", trans, dmy, hms)


            # regresar el texto, una lista de las keywords que salieron en el texto para que sean subrayadas y el popup, se regresa None como popup si no hay nada
            return jsonify({"text":trans, "summary":summary, "keys":keys, "popup":popup, "priority":priority, "date":dmy, "hour":hms}), 200
        else:
            return jsonify({"error": "No audio file provided"}), 400

    
    # # Implementar el guardado del formulario
    # else:
    #     pass


# Inserta y elimina keywords de la lusta de palabras
@app.route("/key_words", methods=["GET", "POST"])
def key_words():
    if request.method == "GET":
        words = db.execute("SELECT * FROM keywords")
        return jsonify({'words': words})
    
    elif request.method == "POST":
        data = request.get_json()
        db.execute("INSERT INTO keywords (words) VALUES (?)", data["words"])
        return jsonify({'words': data["words"]})

    

@app.route("/key_words/<int:item_id>/", methods=["DELETE", "PUT"])
def keywords_single(item_id):
    if request.method == "DELETE":
        # Delete the item from the database
        db.execute("DELETE FROM keywords WHERE id = :item_id", item_id=item_id)
        return jsonify({"success": "Yes"}), 200

    else:
        result = db.execute("SELECT * FROM keywords WHERE id = :item_id", item_id=item_id)

        if not result:
            return jsonify({"error": "Item not found"}), 404

        # Get the data to update from the request
        data = request.get_json()

        # Update the item in the database
        db.execute(
            "UPDATE keywords SET words = :value1 WHERE id = :item_id",
            value1=data["words"],
            item_id=item_id,
        )
        return jsonify({'success': "yes"})




# Inserta y elimina relations de la lista de palabras
@app.route("/relations", methods=["GET", "POST"])
def relations():
    if request.method == "GET":
        words = db.execute("SELECT * FROM relations")
        return jsonify({'words': words})
    
    elif request.method == "POST":
        data = request.get_json()
        db.execute("INSERT INTO relations (key1, key2, popup) VALUES (?, ?, ?)", data["key1"], data["key2"], data["popup"])
        return jsonify({'key1': data["key1"], 'key2': data["key2"], 'popup': data["popup"]})

    
    

@app.route("/relations/<int:item_id>/", methods=["DELETE", "PUT"])
def relations_dp(item_id):
    if request.method == "DELETE":
        # Delete the item from the database
        db.execute("DELETE FROM relations WHERE id = :item_id", item_id=item_id)
        return jsonify({"success": "Yes"}), 200

    else:
        result = db.execute("SELECT * FROM relations WHERE id = :item_id", item_id=item_id)

        if not result:
            return jsonify({"error": "Item not found"}), 404

        # Get the data to update from the request
        data = request.get_json()

        # Update the item in the database
        db.execute(
            "UPDATE relations SET key1 = :key1, key2 = :key2, popup = :popup,  WHERE id = :item_id",
            key1=data["key1"],
            key2=data["key2"],
            popup=data["popup"],
            item_id=item_id,
        )
        return jsonify({'success': "yes"})




# Desplegar todos los datos de la db en una tabla
@app.route("/overview")
def overview():
    data = db.execute("SELECT id, fecha, transcript FROM calls")
    return jsonify(data)




# Launching
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

 





"""
# Tablas de SQL

CREATE TABLE calls (
        id INTEGER PRIMARY KEY,
        fecha TEXT,
        hora TEXT,
        filename TEXT,
        fileroute TEXT,
        transcript TEXT,
        peligro, TEXT
    );


CREATE TABLE keywords (
        id INTEGER PRIMARY KEY,
        words TEXT
    );

CREATE TABLE relations (
        id INTEGER PRIMARY KEY,
        key1 TEXT,
        key2 TEXT
    );

"""  