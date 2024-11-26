// Build a full text search index to query movie plots.

CREATE FULLTEXT INDEX moviePlots IF NOT EXISTS FOR (m:Movie) ON EACH [m.plot];
