
--! REGISTRY
-- name: check_acc
-- check the existence of a user
SELECT U.extid as usr, U.pwdlog as pwd FROM public.contacts C
JOIN public.users U
   ON U.ddot = C.contfrom
WHERE C.cont = :contact;

-- name: get_usr
-- get a user
SELECT ddot as usr FROM public.users 
WHERE extid = :usr;

-- name: check_tkn
-- check the existence of a token as blacklisted token
SELECT * FROM public.logtoken L WHERE L.token = :tkn;

-- name: in_tkn
-- check the existence of a token as blacklisted token
INSERT INTO logtoken (token, tokdt)
VALUES (:tkn, :dt);

--- name: check_cont
--- check if a user already exists
SELECT cntid FROM contacts WHERE cont = :cnt;

-- name: in_acc<!
-- create a user contact
INSERT INTO public.users(fullname, dob, gender, pwdlog, contact, email)
VALUES(:fname, :bday, :mel, :pwd, :cnt, :emel)
ON CONFLICT DO NOTHING
RETURNING extid;


-- name: in_cont
-- create a user contact
INSERT INTO contacts (contfrom, cont, contyp, contdt)
VALUES (:usr, :cnt, :typ, :dt); 


--! PROFILE
-- name: in_basic<!
-- create user basic profile
INSERT INTO basics (
   usrbs, acad, place, dscp, strt, endt
)
VALUES (
   :usr, :acad, :plc, :dspln, :strtd, :endd
) ON CONFLICT DO NOTHING RETURNING basid;

-- name: acadqfn
-- create user basic profile
SELECT * FROM public.basic B
WHERE B.usrbs = :usr AND B.acad IS TRUE

-- name: in_acad<!
-- create user basic profile
INSERT INTO accademics (
   arnac, bacid, title, strt, endt
)
VALUES (
   :arena, :base, :ttl, :strt, :endt
);

-- name: rsrchaqfn
-- create user basic profile
SELECT A.title FROM public.accademics A
JOIN public.basic B
   ON B.basid = A.bacid
WHERE B.usrbs = :usr AND A.acad IS TRUE

-- name: in_rsrcha<!
-- create user basic profile
BEGIN
   DECLARE cont INT
   INSERT INTO contacts (cntid, contfrom, cont, email, verifd, contdt)
   VALUES (
      :usr, :cnt, :dt
   );
   SELECT @cont = scope_identity()
   INSERT INTO research (
      acres, cntres, typ, org, dscp, strt, endt, rscdt
   )
   VALUES (
      :acad, @cont, :typ, :org, :dspln, :strtd, :endd, :dt
   );
END

-- name: in_work<!
-- create user basic profile
INSERT INTO workplace (
   usrwkp, arwkp, place, job, strt, endt, wokdt
)
VALUES (
   :usr, :arena, :plc, :rol, :strtd, :endd, :dt
);

--! USER
-- name: in_awd<!
-- create user basic profile
INSERT INTO awards (
   usraw, typ, arnawd, org, awardt, awdt
)
VALUES (
   :usr, :typ, :arena, :org, :awdt, :dt
);

-- name: in_pub<!
-- create user basic profile
INSERT INTO pubs (
   repub, field, title, fyl, publsdt, pubdt
)
VALUES (
   :resrch, :fld, :ttl, :fyl, :pubdt, :dt
);

--! service
-- name: in_stry<!
-- create user basic profile
INSERT INTO storys (
   usrst, titl, brifn, strydt
)
VALUES (
   :usr, :ttl, :sumry, :dt
);

-- name: in_vasn<!
-- create user basic profile
INSERT INTO stryversn (
   stryvsn, usrpg, contrib, subtitl, stry, vsndt, tldt
)
VALUES (
   :stry, :usr, :trib, :ttl, :vasn, :vasndt, :dt
);

-- name: in_qot<!
-- create user basic profile
INSERT INTO qotes (vsnqot, usrqt, qote, qotdt)
VALUES (
   :vasn, :usr, :qot, :dt
);
