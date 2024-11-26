CREATE INDEX IF NOT EXISTS FOR (a:Actor) ON (a.firstName);

CREATE INDEX IF NOT EXISTS FOR (a:Actor) ON (a.lastName);

CREATE INDEX IF NOT EXISTS FOR (m:Movie) ON (m.releaseYear, m.viewerRating);

CREATE INDEX IF NOT EXISTS FOR (c:Country) ON (c.name);

CREATE INDEX IF NOT EXISTS FOR (m:Movie) ON (m.languages);

CREATE FULLTEXT INDEX moviePlots IF NOT EXISTS FOR (m:Movie) ON EACH [m.plot];

CREATE FULLTEXT INDEX movieNames IF NOT EXISTS FOR (m:Movie) ON EACH [m.title, m.aka];
