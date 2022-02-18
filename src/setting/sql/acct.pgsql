
--! REGISTRY
-- name: check_acc^
-- check the existence of a user
SELECT U.extid as usr, L.pwdlog as pwd, active as status FROM public.users U
JOIN  public.contacts C
   ON U.ddot = C.usrcont
JOIN public.logs L
   ON U.ddot = L.usrlg
WHERE C.cont = :contact;

-- name: get_usr^
-- get a user
SELECT ddot as usr, active as status FROM public.users 
WHERE extid = :usr;

-- name: get_cont$
-- check if a contact already exists
SELECT row_to_json(contact)
FROM(
   SELECT C.cont as contat FROM public.contacts C
   JOIN  public.users U
      ON C.usrcont = U.ddot
   WHERE C.cont = :cnt
)contact;

-- name: usr_status^
-- check the existence of a token as blacklisted token
   SELECT U.active as user_status, COALESCE(L.token, 'None') as token, COALESCE(L.compromised, FALSE) as token_status FROM public.users U  
   LEFT JOIN public.logtoken L
      ON L.tklog = U.ddot
   LEFT JOIN public.contacts C
      ON C.usrcont = U.ddot
   WHERE C.cont = :contact;

-- name: check_tkn
-- check the existence of a token as blacklisted token
SELECT * FROM public.logtoken L WHERE L.token = :tkn;

-- name: del_tkn!
-- check the existence of a token as blacklisted token
DELETE FROM public.logtoken L WHERE L.token = :tkn;

-- name: cr8_tkn
-- check the existence of a token as blacklisted token
INSERT INTO logtoken (token, tokdt)
VALUES (:tkn, :dt);

--- name: check_cont
--- check if a user already exists
SELECT cntid FROM contacts WHERE cont = :cnt;

-- name: cr8_acc<!
-- create a user contact usrlg pwdlog detail
WITH reg AS(
   INSERT INTO public.users (fullname)
   VALUES (:fname) ON CONFLICT DO NOTHING RETURNING ddot as usr, extid as usr_id
),
contact AS(
   INSERT INTO public.contacts (usrcont, cont)
   VALUES ((SELECT usr FROM reg), :cnt)
),
login AS(
   INSERT INTO public.logs(usrlg, pwdlog)
   VALUES((SELECT usr FROM reg), :pwd)
   ON CONFLICT DO NOTHING
)
SELECT usr_id FROM reg;

-- name: usr_reg^
-- record_class: RegCheck
-- get a user registeration detail for possible changes
-- JSON_BUILD_OBJECT is used with specifying key value pairs seperated with a comma
SELECT ROW_TO_JSON(reg_data)
FROM(
   SELECT U.fullname as fname, U.gender as sex, U.dob, C.email as typ, C.cont as cont FROM public.users U
   JOIN public.contacts C
      ON U.ddot = C.usrcont
   WHERE ddot = :usr
)reg_data

-- name: upd8_acc!
-- create a user contact
WITH reg AS(
   INSERT INTO public.users (ddot, fullname, dob, gender)
   VALUES (:usr, :fname, :bday, :mel) ON CONFLICT(ddot) DO UPDATE
   SET fullname = :fname, dob = :bday, gender = :mel, active = :actv 
),
usr AS(
   SELECT ddot FROM public.users WHERE ddot = :usr
)
INSERT INTO public.contacts (usrcont, cont)
VALUES ((SELECT ddot FROM usr), :cnt) ON CONFLICT(cont) DO UPDATE
SET verifd = :verfd;

-- name: upd8_pwd!
UPDATE public.logs
   SET pwdlog = :pwd
FROM public.users
WHERE ddot = :usr;

-- name: cr8_cont
-- create a user contact
INSERT INTO contacts (usrcont, cont, contyp)
VALUES (:usr, :cnt, :typ); 

