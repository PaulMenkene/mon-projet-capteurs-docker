from flask import Flask, render_template
import psycopg2
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

def get_connection():
    return psycopg2.connect(
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        database=os.getenv("PGDATABASE")
    )

@app.route("/")
def index():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()[0]
        cursor.close()
        connection.close()
        return f"Connexion réussie à PostgreSQL !<br>Version : {db_version}"
    except Exception as e:
        app.logger.error(f"Erreur dans / : {e}")
        return "Erreur lors de la connexion à PostgreSQL", 500

@app.route("/capteur")
def capteur():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nom, valeur FROM capteurs;")
        capteurs = cur.fetchall()
        cur.close()
        conn.close()
        return render_template("capteur.html", capteurs=capteurs)
    except Exception as e:
        app.logger.error(f"Erreur dans /capteur : {e}")
        return "Erreur dans /capteur", 500

@app.route("/map")
def map():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nom, latitude, longitude, valeur FROM capteurs;")
        rows = cur.fetchall()
        capteurs = [
            {"id": r[0], "nom": r[1], "latitude": float(r[2]), "longitude": float(r[3]), "valeur": r[4]}
            for r in rows
        ]
        cur.close()
        conn.close()
        return render_template("map.html", capteurs=capteurs)
    except Exception as e:
        app.logger.error(f"Erreur dans /map : {e}")
        return "Erreur dans /map", 500

@app.route("/healthcheck")
def healthcheck():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
