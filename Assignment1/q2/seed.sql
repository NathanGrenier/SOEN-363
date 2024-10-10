INSERT INTO City (C_ID) VALUES (1), (2);
INSERT INTO Province (P_ID) VALUES (1), (2);
INSERT INTO Locations (LOC_CITY, LOC_PROVINCE) VALUES (1, 1), (2, 2);

INSERT INTO LessonSchedule (LSCH_ID, DTS_ID) VALUES (1, 1), (2, 2);
INSERT INTO DayTimeSlots (DTS_ID, LSCH_ID, DTS_START_DATE, DTS_END_DATE) VALUES (1, 1, '2023-01-01', '2023-01-31'), (2, 2, '2023-02-01', '2023-02-28');

INSERT INTO Lesson (LS_ID, LOC_ID, LSCH_ID) VALUES (1, 1, 1), (2, 2, 2);
INSERT INTO Private (LS_ID) VALUES (1);
INSERT INTO Group (LS_ID) VALUES (2);

INSERT INTO LessonSpace (LS_ID, LOC_ID, LS_OWNED) VALUES (1, 1, TRUE), (2, 2, FALSE);

INSERT INTO Instructor (I_ID, I_NAME, I_PHONE) VALUES (1, 'John Doe', '123-456-7890');

INSERT INTO Specialization (S_ID, S_NAME) VALUES (1, 'Math'), (2, 'Science');

INSERT INTO Offering (O_ID, I_ID, LS_ID) VALUES (1, 1, 1), (2, 1, 2), (3, 1, 1);

INSERT INTO Client (C_ID, C_NAME, C_PHONE) VALUES (1, 'Alice', '987-654-3210'), (2, 'Bob', '654-321-0987');

INSERT INTO Registered (C_ID, O_ID) VALUES (1, 1), (2, 2);

-- Sample data for offers
-- Offer 1: Accepted
INSERT INTO Offering (O_ID, I_ID, LS_ID) VALUES (1, 1, 1);
-- Offer 2: Rejected
INSERT INTO Offering (O_ID, I_ID, LS_ID) VALUES (2, 1, 2);
-- Offer 3: Pending
INSERT INTO Offering (O_ID, I_ID, LS_ID) VALUES (3, 1, 1);