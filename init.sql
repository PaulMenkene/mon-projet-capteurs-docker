CREATE TABLE IF NOT EXISTS capteurs (
    id SERIAL PRIMARY KEY,
    nom TEXT,
    valeur REAL,
    latitude REAL,
    longitude REAL
);