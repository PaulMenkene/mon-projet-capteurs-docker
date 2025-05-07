from flask import Flask, render_template, request
import psycopg2
import logging

app = Flask(__name__)

# Configuration du logging
logging.basicConfig(level=logging.DEBUG)

# Fonction de connexion à la base de données
def get_db_connection():
    return psycopg2.connect(
        host='db',  # ou 'localhost' si pas dans Docker
        database='postgres',
        user='postgres',
        password='postgres'
    )

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM capteurs")
        capteurs = cur.fetchall()
        conn.close()
        return render_template('index.html', capteurs=capteurs)
    except Exception as e:
        app.logger.error(f"Erreur dans / : {e}")
        return "Erreur interne du serveur", 500

@app.route('/capteur/<int:id>')
def detail_capteur(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM capteurs WHERE id = %s", (id,))
        capteur = cur.fetchone()
        conn.close()
        if capteur:
            return render_template('capteur.html', capteur=capteur)
        else:
            return "Capteur introuvable", 404
    except Exception as e:
        app.logger.error(f"Erreur dans /capteur/{id} : {e}")
        return "Erreur interne du serveur", 500

@app.route('/healthcheck')
def healthcheck():
    try:
        return {'status': 'ok'}, 200
    except Exception as e:
        app.logger.error(f"Erreur dans /healthcheck : {e}")
        return {'status': 'error'}, 500

if __name_ == '__main__':
    app.run(debug=False, host='0.0.0.0')
