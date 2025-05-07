import psycopg2

# Connexion à la base PostgreSQL
conn = psycopg2.connect(
    host="db",
    database="exem_data",
    user="paul",
    password="secret",
    port=5432
)

cur = conn.cursor()

capteurs = [
    ("Température Paris", 21.6, 48.8566, 2.3522),
    ("Température Lyon", 22.1, 45.75, 4.85),
    ("Température Marseille", 24.7, 43.2965, 5.3698),
    ("Humidité Lille", 58.3, 50.6292, 3.0573),
    ("Humidité Nantes", 62.0, 47.2184, -1.5536),
    ("CO2 Strasbourg", 410, 48.5734, 7.7521),
    ("CO2 Nice", 420, 43.7102, 7.2620),
    ("Pression Bordeaux", 1013, 44.8378, -0.5792),
    ("Température Toulouse", 23.5, 43.6047, 1.4442),
    ("Humidité Rennes", 65.1, 48.1173, -1.6778),
    ("Température Montpellier", 26.1, 43.6117, 3.8777),
    ("CO2 Grenoble", 435, 45.1885, 5.7245),
    ("Pression Dijon", 1015, 47.3220, 5.0415),
    ("Humidité Le Havre", 67.8, 49.4944, 0.1079),
    ("Température Brest", 19.4, 48.3904, -4.4861),
    ("CO2 Reims", 418, 49.2583, 4.0317),
    ("Température Perpignan", 27.0, 42.6887, 2.8948),
    ("Humidité Metz", 60.4, 49.1193, 6.1757),
    ("Température Amiens", 20.9, 49.8950, 2.3023),
    ("CO2 Orléans", 412, 47.9025, 1.9090),
]

cur.executemany(
    "INSERT INTO capteurs (nom, valeur, latitude, longitude) VALUES (%s, %s, %s, %s)", capteurs
)

conn.commit()
cur.close()
conn.close()
print("20 capteurs insérés avec succès.")
