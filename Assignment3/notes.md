# Overview
Create a NoSQL database of movies and their information. The movies data are directly extracted from assignment 2 and transferred into the NoSQL
database.

# Data Transfer
The data transfer is done by converting the data from each relation from the RDBMS into a csv (or tsv) or json data. You will then use the data and directly import it into Neo4j.

# Entities / Nodes
In this assignment you must create the following entities (nodes) and populate the data:
- [x] Movies:
  - [x] title
  - [x] plot
  - [x] content rating
  - [x] viewer rating
  - [x] release year
  - [x] genres
  - [x] languages
  - [x] AKAs
  - [x] watchmode id
- [x] Actors:
  - [x] first name
  - [x] last name
- [x] Countries
- [x] Keywords

# Data Files and Scripts
- [x] Extract the data from your database into the data file (csv, tsv, or json1).
- [x] Write scripts to create the database and populate the data in Neo4J.
    > Note that Neo4J supports [array attributes](https://neo4j.com/docs/cypher-manual/current/functions/list/), which are normally represented using weak entities in relational model. To populate the such data (i.e. genres, languages), you may use a separate csv file.

# Queries
Provide queries for the following questions:
- [x] Find all movies that are played by a sample actor.
- [x] Find the number of movies with and without a watch-mode info.
- [x] Find all movies that are released after the year 2023 and has a viewer rating of at least 5.
- [x] Find all movies with two countries of your choice. Make sure your query returns more than one movie. List movies that may be associated with either of the countries (not necessarily both).
- [x] Find top 2 movies with largest number of keywords.
- [x] Find top 5 movies (ordered by rating) in a language of your choice.
- [x] Build full text search index to query movie plots.
- [x] Write a full text search query and search for some sample text of your choice.

> Make sure all above queries return data. Modify the data in your database, if necessary.

# What to Submit
Include your name and student ID in the submission.
