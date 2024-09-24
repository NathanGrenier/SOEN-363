INSERT INTO Museum
  (MUSEUM_ID)
VALUES
  (1);

INSERT INTO Departments
  (DEP_ID, MUS_ID)
VALUES
  (12, 1), 
  (22, 1),
  (55, 1);

INSERT INTO Exhibitions
  (EXHI_ID, MUS_ID, DEP_HOME_ID, EXHI_START_DATE, EXHI_END_DATE)
VALUES
  (123, 1, 12, '2023-01-01', '2023-01-31' ), 
  (321, 1, 22, '2024-02-01', '2024-07-01' ); 

INSERT INTO Collections
  (COLL_ID, DEP_ID, EXHI_ID)
VALUES
  (1, 22, 123),
  (2, 12, 123),
  (3, 55, 321);

INSERT INTO Countries 
  (COUNTRY_ID, COUNTRY_NAME)
VALUES
  (1, 'Canada'),
  (2, 'USA'),
  (3, 'Mexico'),
  (4, 'Italy');

INSERT INTO Artists
  (ARTIST_ID, ARTIST_NAME)
VALUES
  (1, 'Pablo Picasso'),
  (2, 'Vincent Van Gogh'),
  (3, 'Leonardo Da Vinci'),
  (4, 'Myron');

INSERT INTO ArtObjectTypes
  (ARTOBJ_TYPE_ID, ARTOBJ_TYPE_NAME)
VALUES
  (1, 'Painting'),
  (2, 'Sculpture'),
  (3, 'Photography');

INSERT INTO Periods
  (PER_ID, PER_NAME, PER_START_DATE, PER_END_DATE)
VALUES
  (1, 'Renaissance', '1400-01-01', '1600-01-01'),
  (2, 'Baroque', '1600-01-01', '1700-01-01'),
  (3, 'Impressionism', '1800-01-01', '1900-01-01');

INSERT INTO ArtObjects
  (ARTOBJ_ACQUISITION_NUM, ARTOBJ_TYPE_ID, COLL_ID, ARTIST_ID, COUNTRY_ID, PER_ID, DIM_ID, ARTOBJ_TITLE, ARTOBJ_DESC, ARTOBJ_PROD_DATE)
VALUES
  (1, 1, 3, 1, 1, 1, 1, 'Starry Night', 'A painting of a starry night', '1889-06-01'),
  (2, 1, 2, 2, 2, 2, 2, 'Mona Lisa', 'A painting of Mona Lisa', '1503-01-01'),
  (3, 3, 1, 3, 3, 3, 3, 'The Persistence of Memory', 'A painting of melting clocks', '1931-01-01'),
  (4, 2, 3, 4, 4, 3, 3, 'Discobolus', 'A man throwing a disc', '1000-01-01');

INSERT INTO Dimensions
  (DIM_ID, ARTOBJ_ID, DIM_LENGTH, DIM_WIDTH, DIM_DEPTH)
VALUES
  (1, 1, 10.0, 10.0, 10.0),
  (2, 2, 20.0, 20.0, 20.0),
  (3, 3, 30.0, 30.0, 30.0);

INSERT INTO Borrowed
  (EXHI_ID, ARTOBJ_ACQUISITION_NUM, B_DATE, B_RETURN_DATE)
VALUES 
  (123, 1, '2023-01-01', '2023-01-31');
