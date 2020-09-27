DROP TABLE IF EXISTS equipo;
DROP TABLE IF EXISTS ciudad;
DROP TABLE IF EXISTS partido;

CREATE TABLE equipo(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [name] STRING NOT NULL
);

CREATE TABLE ciudad(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [name] STRING NOT NULL
);

CREATE TABLE partido(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [date] DATE NOT NULL,
    [fk_home_country] STRING NOT NULL REFERENCES equipo(id),
    [fk_away_country] STRING NOT NULL REFERENCES equipo(id),
    [home_score] INTEGER NOT NULL,
    [away_score] INTEGER NOT NULL,
    [tournament] STRING NOT NULL
);

------------------------------ ESQUEMA INCOMPLETO ------------------------------