import psycopg2
import random

conn = psycopg2.connect(
    host="db",
    database="exem_data",
    user="paul",
    password="secret",
    port=5432
)
cur = conn.cursor()

N = 100000
batch_size = 1000
capteurs = []

print(f"Insertion de {N} capteurs en cours...")

for i in range(1, N + 1):
    nom = f"Capteur_{i}"
    valeur = round(random.uniform(10, 100), 2)
    lat = round(random.uniform(41.0, 51.0), 6)
    lon = round(random.uniform(-5.0, 9.0), 6)
    capteurs.append((nom, valeur, lat, lon))

    if i % batch_size == 0:
        cur.executemany("INSERT INTO capteurs (nom, valeur, latitude, longitude) VALUES (%s, %s, %s, %s)", capteurs)
        conn.commit()
        print(f"{i} capteurs insérés...")
        capteurs.clear()

# Insérer les éventuels restants
if capteurs:
    cur.executemany("INSERT INTO capteurs (nom, valeur, latitude, longitude) VALUES (%s, %s, %s, %s)", capteurs)
    conn.commit()

cur.close()
conn.close()
print("Insertion terminée.")
