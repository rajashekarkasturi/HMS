CREATE TABLE medicines(
    medicineid SERIAL PRIMARY KEY,
    medicinename VARCHAR NOT NULL,
    quantity INTEGER NOT NULL,
    rate INTEGER NOT NULL
);

INSERT INTO MEDICINES(medicinename, quantity, rate) VALUES ('Paracetamol', 10, 30);
INSERT INTO MEDICINES(medicinename, quantity, rate) VALUES ('Saradon', 50, 15);
INSERT INTO MEDICINES(medicinename, quantity, rate) VALUES ('Coronil', 15, 100);
INSERT INTO MEDICINES(medicinename, quantity, rate) VALUES ('Revital', 100, 50); 