// Write a full text search query and search for some sample text of your choice.

CALL db.index.fulltext.queryNodes("moviePlots", "fight") YIELD node, score
RETURN node.title, score, node.plot;
