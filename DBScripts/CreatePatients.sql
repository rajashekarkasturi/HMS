CREATE TABLE patients(
    puid INTEGER PRIMARY KEY,
    pname VARCHAR NOT NULL,
    page INTEGER NOT NULL,
    pdate DATE NOT NULL,
    ptypeofbed VARCHAR NOT NULL,
    paddress VARCHAR NOT NULL,
    pstate VARCHAR NOT NULL,
    pcity VARCHAR NOT NULL
);

INSERT INTO patients values(123, 'abc', 22, '2008-11-11', 'single', 'Kotagally', 'Telangana', 'Nizamabad');