DROP TABLE IF EXISTS partido;
DROP TABLE IF EXISTS torneo;
DROP TABLE IF EXISTS ciudad;
DROP TABLE IF EXISTS pais;

CREATE TABLE partido(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [date] DATE NOT NULL,
    [home_team] TEXT NOT NULL,
    [away_team] TEXT NOT NULL,
    [home_score] INTEGER NOT NULL,
    [away_score] INTEGER NOT NULL,
    [tournament] TEXT NOT NULL,
    [city] TEXT NOT NULL,
    [country] TEXT NOT NULL,
    [neutral] BIT NOT NULL,
    [result] INTEGER);