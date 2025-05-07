from flask import Flask, render_template
import psycopg2
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Page d'accueil
@app.route("/")
def index():
    return render_template("index.html")

# Page carte Leaflet avec capteurs
@app.route("/map")
def map():
    try:
        connection = psycopg2.connect(
            host=os.getenv("PGHOST"),
            port=os.getenv("PGPORT"),
            user=os.getenv("PGUSER"),
            password=os.getenv("PGPASSWORD"),
            database=os.getenv("PGDATABASE")
        )
        cursor = connection.cursor()
        cursor.execute("SELECT id, nom, latitude, longitude, valeur FROM capteurs;")
        capteurs = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template("map.html", capteurs=capteurs)

    except Exception as e:
        app.logger.error(f"Erreur dans /map : {e}")
        return "Erreur dans /map", 500

# Affichage simple des capteurs
@app.route("/capteur")
def capteur():
    try:
        connection = psycopg2.connect(
            host=os.getenv("PGHOST"),
            port=os.getenv("PGPORT"),
            user=os.getenv("PGUSER"),
            password=os.getenv("PGPASSWORD"),
            database=os.getenv("PGDATABASE")
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM capteurs;")
        capteurs = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template("capteur.html", capteurs=capteurs)

    except Exception as e:
        app.logger.error(f"Erreur dans /capteur : {e}")
        return "Erreur dans /capteur", 500

# Healthcheck
@app.route("/healthcheck")
def healthcheck():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
