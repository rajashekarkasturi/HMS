CREATE TABLE diagnostics (
    name VARCHAR NOT NULL,
    rate INTEGER NOT NULL
);

INSERT INTO diagnostics VALUES ('ECG', 200);
INSERT INTO diagnostics VALUES ('MRI',1500);
INSERT INTO diagnostics VALUES ('MRI',1000);


CREATE TABLE diagnosticsDone (
    name VARCHAR NOT NULL,
    patientid INTEGER NOT NULL,
    rate INTEGER NOT NULL
);
