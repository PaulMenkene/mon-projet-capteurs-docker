from flask import Flask, render_template
import psycopg2
import os
import logging

# Initialisation de Flask
app = Flask(_name_)

# Configuration du logging pour Railway
logging.basicConfig(level=logging.DEBUG)

# Route principale
@app.route("/")
def index():
    try:
        # Connexion à PostgreSQL via les variables Railway
        connection = psycopg2.connect(
            host=os.getenv("PGHOST"),
            port=os.getenv("PGPORT"),
            user=os.getenv("PGUSER"),
            password=os.getenv("PGPASSWORD"),
            database=os.getenv("PGDATABASE")
        )
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()[0]
        cursor.close()
        connection.close()
        return f"Connexion réussie à PostgreSQL !<br>Version : {db_version}"

    except Exception as e:
        app.logger.error(f"Erreur : {e}")
        return "Erreur lors de la connexion à PostgreSQL", 500

# Lancement de l'app (ne pas mettre en production avec debug=True)
if _name_ == "_main_":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
