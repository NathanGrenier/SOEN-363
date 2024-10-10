CREATE TABLE IF NOT EXISTS Museum (
    MUSEUM_ID INT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Exhibitions (
    EXHI_ID INT,
    MUS_ID INT,
    DEP_HOME_ID INT NOT NULL,
    EXHI_START_DATE DATE,
    EXHI_END_DATE DATE,
    PRIMARY KEY (EXHI_ID, MUS_ID),
    FOREIGN KEY (MUS_ID) REFERENCES Museum(MUS_ID)
    FOREIGN KEY (DEP_HOME_ID) REFERENCES Departments(DEP_ID)
);

CREATE TABLE IF NOT EXISTS Departments (
    DEP_ID INT,
    MUS_ID INT,
    PRIMARY KEY (DEP_ID, MUS_ID),
    FOREIGN KEY (MUS_ID) REFERENCES Museum(MUS_ID)
);

CREATE TABLE IF NOT EXISTS Collections (
    COLL_ID INT,
    DEP_ID INT,
    EXHI_ID INT,
    PRIMARY KEY (COLL_ID, DEP_ID),
    FOREIGN KEY (DEP_ID) REFERENCES Departments(DEP_ID),
    FOREIGN KEY (EXHI_ID) REFERENCES Exhibitions(EXHI_ID)
);

CREATE TABLE IF NOT EXISTS Countries (
    COUNTRY_ID INT PRIMARY KEY,
    COUNTRY_NAME VARCHAR(40)
);

CREATE TABLE IF NOT EXISTS Artists (
    ARTIST_ID INT PRIMARY KEY,
    ARTIST_NAME VARCHAR(40)
);

CREATE TABLE IF NOT EXISTS ArtObjectTypes (
    ARTOBJ_TYPE_ID INT PRIMARY KEY,
    ARTOBJ_TYPE_NAME VARCHAR(40)
);

CREATE TABLE IF NOT EXISTS Periods (
    PER_ID INT PRIMARY KEY,
    PER_NAME VARCHAR(40) NOT NULL,
    PER_START_DATE DATE NOT NULL,
    PER_END_DATE DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS Dimensions (
    DIM_ID INT,
    ARTOBJ_ID INT,
    DIM_LENGTH FLOAT,
    DIM_WIDTH FLOAT,
    DIM_DEPTH FLOAT,
    PRIMARY KEY (DIM_ID, ARTOBJ_ID)
);

CREATE TABLE IF NOT EXISTS ArtObjects (
    ARTOBJ_ACQUISITION_NUM INT PRIMARY KEY,
    ARTOBJ_TYPE_ID INT NOT NULL,
    COLL_ID INT NOT NULL,
    ARTIST_ID INT,
    COUNTRY_ID INT,
    PER_ID INT NOT NULL,
    DIM_ID INT NOT NULL,
    ARTOBJ_TITLE VARCHAR(40),
    ARTOBJ_DESC VARCHAR(100),
    ARTOBJ_PROD_DATE DATE,
    FOREIGN KEY (ARTOBJ_TYPE_ID) REFERENCES ArtObjectTypes(ARTOBJ_TYPE_ID),
    FOREIGN KEY (PER_ID) REFERENCES Periods(PER_ID),
    FOREIGN KEY (DIM_ID) REFERENCES Dimensions(DIM_ID),
    FOREIGN KEY (COLL_ID) REFERENCES Collections(COLL_ID),
    FOREIGN KEY (ARTIST_ID) REFERENCES Artists(ARTIST_ID),
    FOREIGN KEY (COUNTRY_ID) REFERENCES Countries(COUNTRY_ID)
);

CREATE TABLE IF NOT EXISTS Borrowed (
    EXHI_ID INT,
    ARTOBJ_ACQUISITION_NUM INT,
    B_DATE DATE,
    B_RETURN_DATE DATE,
    PRIMARY KEY (EXHI_ID, ARTOBJ_ACQUISITION_NUM),
    FOREIGN KEY (EXHI_ID) REFERENCES Exhibitions(EXHI_ID),
    FOREIGN KEY (ARTOBJ_ACQUISITION_NUM) REFERENCES ArtObjects(ARTOBJ_ACQUISITION_NUM)
);