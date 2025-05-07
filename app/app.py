from flask import Flask, request, render_template
import psycopg2
import os
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        dbname=os.environ.get("DB_NAME", "exem_data"),
        user=os.environ.get("DB_USER", "paul"),
        password=os.environ.get("DB_PASSWORD", "secret")
    )

@app.route("/", methods=["GET", "POST"])
def index():
    logging.info("Accès à la page d'accueil")
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == "POST":
        nom = request.form["nom"]
        valeur = request.form["valeur"]
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]
        cur.execute("INSERT INTO capteurs (nom, valeur, latitude, longitude) VALUES (%s, %s, %s, %s)",
                    (nom, valeur, latitude, longitude))
        conn.commit()
        logging.info(f"Capteur ajouté : {nom}, valeur={valeur}, lat={latitude}, lon={longitude}")
    cur.execute("SELECT id, nom, valeur, latitude, longitude FROM capteurs ORDER BY id DESC")
    capteurs = cur.fetchall()
    conn.close()
    return render_template("index.html", capteurs=capteurs)

@app.route("/map")
def map():
    logging.info("Accès à la carte des capteurs")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nom, valeur, latitude, longitude FROM capteurs")
    capteurs = cur.fetchall()
    conn.close()
    return render_template("map.html", capteurs=capteurs)

@app.route("/capteur/<int:id>")
def detail_capteur(id):
    logging.info(f"Accès au détail du capteur ID={id}")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM capteurs WHERE id = %s", (id,))
    capteur = cur.fetchone()
    conn.close()
    if capteur:
        return render_template("capteur.html", capteur=capteur)
    else:
        return "Capteur introuvable", 404

@app.route("/healthcheck")
def healthcheck():
    try:
        conn = get_db_connection()
        conn.close()
        logging.info("Healthcheck: OK")
        return "OK", 200
    except Exception as e:
        logging.error(f"Healthcheck error: {e}")
        return f"Database error: {e}", 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
