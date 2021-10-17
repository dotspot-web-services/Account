
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
INSERT INTO public.users(fullname, pwdlog, contact, email)
VALUES(:fname, :pwd, :cnt, :emel)
ON conflict do nothing
RETURNING extid;

-- name: complete_reg
-- get a user
SELECT fullname as fname, gender as sex, dob, contact as cont
FROM public.users 
WHERE ddot = :usr;

-- name: update_acc<!
-- create a user contact
INSERT INTO public.users(fullname, dob, gender, pwdlog, contact, email)
VALUES(:fname, :bday, :mel, :pwd, :cnt, :emel)
ON CONFLICT DO UPDATE
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
) ON CONFLICT UPDATE RETURNING basid;

-- name: basic_prof
-- accademics differentiated user basic profile
SELECT U.fullname as fnanme, M.med as pix, B.acad, B.place, B.dscp, B.strt, B.endt FROM public.basics B
JOIN public.users U ON U.ddot = B.usrbs
JOIN public.media M ON M.meid = U.ddot 
WHERE B.usrbs = :usr;

-- name: skil_prof
-- general differentiated user basic profile
SELECT U.fullname, M.med, S.acad, S.place, S.dscp, S.strt, S.endt FROM public.basics S
JOIN public.users U  ON U.ddot = S.usrbs
JOIN public.media M ON M.meid = U.ddot
WHERE S.usrbs = :usr;

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

-- name: acads_prof
SELECT U.fullname, M.med, B.acad, B.place, B.dscp, A.strt, A.endt, A.title FROM public.accademics A
JOIN public.basics B ON B.usrbs = A.bacid
JOIN  public.users U  ON U.ddot = B.usrbs
JOIN public.media M ON M.meid = U.ddot
WHERE B.usrbs = :usr;

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

-- name: rsrch_prof
SELECT U.fullname, M.med, C.cnt, R.typ, R.org, R.dscp, R.strt, R.endt, FROM public.users U
JOIN public.basics S ON S.usrbs = U.ddot
JOIN public.media M ON M.meid = U.ddot
JOIN public.contacts C  ON C.cntid = R.cntres
WHERE U.ddot = :usr;

-- name: in_work<!
-- create user basic profile
INSERT INTO workplace (
   usrwkp, arwkp, place, job, strt, endt, wokdt
)
VALUES (
   :usr, :arena, :plc, :rol, :strtd, :endd, :dt
);

-- name: wk_prof
SELECT U.fullname, M.med, W.place, W.job, W.strt, W.endt FROM public.users U
JOIN public.media M ON M.meid = U.ddot
JOIN public.workplace W ON W.usrwkp = U.ddot
WHERE U.ddot = :usr;

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
