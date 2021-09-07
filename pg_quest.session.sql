--
drop FUNCTION new_usr;
CREATE FUNCTION new_usr(
   fname varchar(250), cnt varchar(200), mel boolean,
   bday date, pwd VARCHAR(500), emel boolean
) RETURNS SETOF uuid AS $new_usr$
DECLARE 
   ext uuid;
   usr int;
BEGIN
      INSERT INTO users (fullname, dob, gender, pwdlog)
      VALUES (fname, bday, mel, pwd)
      RETURNING ddot, extid INTO usr, ext;

      INSERT INTO contacts (contfrom, cont, email)
      VALUES (usr, cnt, emel)
      ON CONFLICT DO NOTHING;
      RETURN ext;
END;
   
$new_usr$ LANGUAGE plpgsql;

--- another option of the  SQL
WITH existn AS
   SELECT cntid FROM contacts WHERE cont = :cnt
SELECT * FROM existn WHERE NOT EXISTS(
WITH usr AS
   INSERT INTO users (fullname, dob, gender)
   VALUES (:fname, :bday, :mel)
   RETURNING extid, ddot
)

--- ctn METHOD
WITH usr AS(
   INSERT INTO users (fullname, dob, gender, pwdlog)
   VALUES (:fname, :bday, :mel, :pwd)
   RETURNING extid, ddot
),
cont AS(
   INSERT INTO contacts (contfrom, cont, email)
   SELECT ddot, :cnt, :emel FROM usr
   ON CONFLICT DO NOTHING
),
SELECT extid FROM usr;

--- anonymous FUNCTION
DO RETURNS SETOF uuid AS $NEW_USR$
DECLARE 
   ext uuid;
   usr int;
BEGIN
   IF(SELECT cntid FROM contacts WHERE cont = cnt) is NULL THEN
      INSERT INTO users (fullname, dob, gender)
      VALUES (:fname, :bday, :mel)
      RETURNING extid, ddot INTO ext, usr

      INSERT INTO contacts (contfrom, cont, email)
      VALUES (usr, :cnt, :emel)

      INSERT INTO logs (usrlg, pwdlog)
      VALUES (usr, :pwd)
   SAVEPOINT
END
RETURN ext
$NEW_USR$ LANGUAGE plpgsql;

ALTER TABLE users ADD CONSTRAINT users_extid_key UNIQUE(extid);

DROP TRIGGER log_contact on users;
DROP FUNCTION log_contact;

CREATE FUNCTION log_contact()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS
$$
BEGIN
   INSERT INTO contacts(contfrom, cont, email)
   VALUES(NEW.ddot, NEW.contact, NEW.email);
	RETURN NEW;
END;
$$;

CREATE TRIGGER log_contact
  AFTER INSERT
  ON users
  FOR EACH ROW
  EXECUTE PROCEDURE log_contact();


INSERT INTO users(fullname, dob, gender, pwdlog, contact, email)
VALUES('john mba', '02-01-1991', 't', 'jhgytbnm,.jhmbt', 'nwanjamba@gmail.com', 't')
ON CONFLICT DO NOTHING
RETURNING extid;

INSERT INTO contacts(contfrom, cont, email)
VALUES ('2132657878', 'nwanjamba@gmail.com', 't')
RETURNING cntid; 

DELETE FROM users;
DELETE FROM contacts;

SELECT * FROM contacts;
SELECT * FROM users;
SELECT * FROM basics;
TRUNCATE users;
SELECT round(pg_total_relation_size('users') / 1024.0 / 1024.0, 2);

--- solve table issue
SELECT CURRVAL(PG_GET_SERIAL_SEQUENCE('"users"', 'contact')) AS "Current Value", MAX("contact") AS "Max Value" FROM "users";
SELECT SETVAL((SELECT PG_GET_SERIAL_SEQUENCE('"Foo"', 'Foo_id')), (SELECT (MAX("Foo_id") + 1) FROM "Foo"), FALSE);

ALTER TABLE basics ALTER COLUMN bsdt SET DEFAULT now();