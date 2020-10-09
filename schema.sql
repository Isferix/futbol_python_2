DROP TABLE IF EXISTS ciudad;
DROP TABLE IF EXISTS pais;
DROP TABLE IF EXISTS torneo;
DROP TABLE IF EXISTS partido;

CREATE TABLE ciudad(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [city] TEXT NOT NULL);


CREATE TABLE pais(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [country] TEXT NOT NULL);


CREATE TABLE torneo(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [tournament] TEXT NOT NULL,
    [neutral] BIT NOT NULL); 
    --Desconozco lo que significa la caracteristica Neutral y la inclui dentro de la tabla torneo 
    --como si fuera una caracteristica propia de estos


CREATE TABLE partido(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [date] DATE NOT NULL,
    [fk_home_team_pais] INTEGER NOT NULL REFERENCES pais(id),
    [fk_away_team_pais] INTEGER NOT NULL REFERENCES pais(id),
    [home_score] INTEGER NOT NULL,
    [away_score] INTEGER NOT NULL,
    [fk_tournmanet_torneo] INTEGER NOT NULL REFERENCES torneo(id),
    [fk_city_pais] INTEGER NOT NULL REFERENCES ciudad(id),
    [fk_country_pais] INTEGER NOT NULL REFERENCES pais(id));