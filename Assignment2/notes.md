DB Requirements:
- TMDB-ids
- IMDB-ids
- Unique Primary Key (Different than TMDB, IMDB ids)
- Movies
  - Watchmode ID
  - Title
  - Plot
  - Content Rating (certificates)
    - G (General Audiences)
    - PG (Parental Guidance Suggested)
    - PG-13 (Parents Strongly Cautioned)
    - R (Restricted)
    - NC-17 (Adults Only)
  - Viewer Rating (float from 0..10 with 1 decimal of accuracy)
  - Genres
  - Actors
  - Directors
  - Release Year
  - AKA (Also Known As)
    - Alternate Name
    - Language
  - Countries
    - Name
    - Country Code
  - Languages
  - Keywords

DB Tables:
- Movies
- Content_Rating
- Genres
- Genre Types
- Actors
- Directors
- Countries
- Languages
- Keywords
- AKA

Cascades: When a Movie is Deleted:
- It's keywords should be deleted
- It's AKAs should be deleted
- It's Reviews should be deleted
- It's MovieLanguages should be deleted
- It's MovieDirectors should be deleted
- It's MovieCountries should be deleted
- It's MovieActors should be deleted
- It's MovieGenres should be deleted