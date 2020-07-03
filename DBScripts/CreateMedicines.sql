CREATE TABLE allocateMedicines(
    id SERIAL PRIMARY KEY,
    medicinename VARCHAR NOT NULL,
    patient_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    rate INTEGER NOT NULL,
    total INTEGER NOT NULL
);