
--! REGISTRY
-- name: check_acc
-- check the existence of a user
SELECT U.extid as usr, L.pwdlog as pwd FROM public.contacts C
JOIN public.users U
   ON U.usrid = C.contfrom
JOIN public.logs L
   ON L.usrlg = C.contfrom
WHERE C.cont = :contact;

-- name: get_usr
-- get a user
SELECT usrid as usr FROM public.users 
WHERE extid = :usr;

-- name: check_tkn
-- check the existence of a token as blacklisted token
SELECT * FROM public.logtoken L WHERE L.token = :tkn;

-- name: in_tkn
-- check the existence of a token as blacklisted token
INSERT INTO logtoken (token, tokdt)
VALUES (:tkn, :dt);

-- name: in_acc<!
-- create a user contact
BEGIN
   DECLARE usr INT
   INSERT INTO users (
      usrid, iprange, active, fullname, dob, gender, dated
   )
   VALUES (
      :ip, :actv, :fname, :dob, :gend, :dtd
   );
   SELECT @usr = scope_identity()
   INSERT INTO contacts (contfrom, cont, contyp, contdt)
   VALUES (@usr, :cnt, :cntyp, :dtd);
   INSERT INTO logs (usrlg, pwdlog, logdt)
   VALUES (@usr, :pwd, :dtd);
   RETURNING usr;
END

-- name: in_cont
-- create a user contact
INSERT INTO contacts (contfrom, cont, contyp, contdt)
VALUES (:usr, :cnt, :typ, :dt); 


--! PROFILE
-- name: in_basic<!
-- create user basic profile
INSERT INTO basic (
   usrbs, arnbs, dscp, place, strt, endt, bsdt, typ
)
VALUES (
   :usr, :arena, :dspln, :plc, :strt, :endt, :dt, :typ
);

-- name: acadqfn
-- create user basic profile
SELECT * FROM public.basic B
WHERE B.usrbs = :usr AND B.acad IS TRUE

-- name: in_acad<!
-- create user basic profile
INSERT INTO accademics (
   bacid, title
)
VALUES (
   :bcid, :ttl
);

-- name: rsrchaqfn
-- create user basic profile
SELECT A.title FROM public.accademics A
JOIN public.basic B
   ON B.basid = A.bacid
WHERE B.usrbs = :usr

-- name: in_rsrcha<!
-- create user basic profile
INSERT INTO research (
   acres, usres, typ, org, dscp, email, rscdt, strt, endt
)
VALUES (
   :acad, :usr, :typ, :org, :dspln, :eml, :dt, :strtd, :endd
);

-- name: in_work<!
-- create user basic profile
INSERT INTO workplace (
   usrwkp, arwkp, place, job, strt, endt, wkdt
)
VALUES (
   :usr, :arena, :plc, :rol, :strtd, :endd, :dt
);

--! USER
-- name: in_awd<!
-- create user basic profile
INSERT INTO awards (
   usraw, typ, arnaw, org, pix, awardt, awdt
)
VALUES (
   :usr, :typ, :arena, :org, :pix, :awdt, :dt
);

-- name: in_pub<!
-- create user basic profile
INSERT INTO pubs (
   repub, field, title, fyl, publsdt, pubdt
)
VALUES (
   :resrch, :fld, :ttl, :fyl, :pubdt, :dt
);

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



-- ! arena
-- name: check_arena
-- get the one spotlight
SELECT FROM public.spotlights WHERE spotid = :spotid

-- name: in_arena!
-- insert an arena basic setup
insert INTO public.arena(uidarn,	arena, logo, about, arndt, libty)
values (:usr, :dname, :dlogo, :abt, :dt, :lty);

-- name: updt_arn!
-- insert an arena basic setup
UPDATE public.aren A
SET A.arena = :aname, A.logo = :alog, A.about = :abt
WHERE A.arenaid = :arena

-- name: in_rul!
-- insert an arena basic setup
insert INTO public.rule(arulid,	drul, approved, ruldt)
values (:arid,	:rul, :aprvd, :dt);

-- name: rules
-- get the one spotlight
SELECT R.drul FROM public.rule R
WHERE R.arulid = :arena AND R.approved > 1
ORDER BY R.ruldt

-- name: updt_rul!
-- insert an arena basic setup
UPDATE public.rule R
SET R.drul = :updt
WHERE R.rulid = :rul

-- name: in_mem!
-- insert an arena basic setup
insert INTO public.arenausrs(arenausrid,	arenausr, usrstatus, arnusrdt, privi)
values (:arena, :usr, :statu, :dt, :priv);

-- name: mems
-- get the one spotlight
SELECT U.fullname, P.pixaddr FROM public.arenausrs A
JOIN users U
   ON A.arenausr = U.usrid
JOIN pix P
   ON U.ddot = P.pixfrom
WHERE A.arenausrid = :usr
ORDER P.pixaddr BY P.pixdt

-- name: in_netwk!
-- insert an arena basic setup
insert INTO public.arenausrs(ntkusr, ntname, dscn, ntkdt)
values (:usr, :wkname, :descn, :dt);

-- name: netwks
-- get the one spotlight
SELECT N.ntname, N.dscn, N.ntkdt FROM public.network N
WHERE N.ntkusr = :usr
ORDER BY N.ntkdt

-- name: in_ppl!
-- insert an arena basic setup
insert INTO public.people(pplusr, dscn, ppldt, evnt)
values (:usr, :descn, :dt, :evnt);

-- name: ppl
-- get the one spotlight
SELECT P.dscn, P.ppldt FROM public.people P
JOIN users U
   ON A.P.pplusr = U.usrid
JOIN pix P
   ON U.usrid = P.pixfrom
WHERE P.pplusr = :usr
ORDER BY P.ppldt

-- name: in_netusr!
-- insert an arena basic setup
insert INTO public.netuser(ntkprj, pplusr, npjdt)
values (:prj, :usr, :dt);

-- name: netusrs!
-- insert an arena basic setup
SELECT N.ntname, N.dscn, N.ntkdt FROM public.network N
WHERE N.ntkusr = :usr
ORDER BY N.ntkdt

-- name: in_pjt!
-- insert an arena basic setup
insert INTO public.project(prjowner, prjname, prjdt)
values (:prjonr, :pname, :dt);

-- name: pjts!
-- insert an arena basic setup
SELECT N.ntname, N.dscn, N.ntkdt FROM public.network N
WHERE N.ntkusr = :usr
ORDER BY N.ntkdt

-- name: in_pjtmem!
-- insert an arena basic setup
insert INTO public.projmems(promems, prjmem, memdt)
values (:proj, :mem, :dt);

-- name: pjtmems!
-- insert an arena basic setup
SELECT N.ntname, N.dscn, N.ntkdt FROM public.network N
WHERE N.ntkusr = :usr
ORDER BY N.ntkdt

-- name: in_conf!
-- insert an arena basic setup
insert INTO public.configs(confrom,	conf, confdt)
values (:cfrom, :config, :dt);

-- name: confs!
-- insert an arena basic setup
SELECT N.ntname, N.dscn, N.ntkdt FROM public.network N
WHERE N.ntkusr = :usr
ORDER BY N.ntkdt

-- name: updt_conf!
-- insert an arena basic setup
UPDATE public.configs C
SET C.conf = :confupdt
WHERE C.confid = :conf

-- ! VOICE
-- name: spot_resp!
-- insert response to an external spotlight
BEGIN TRANSACTION
   DECLARE @DataID int;
   INSERT INTO DataTable (Column1 ...) VALUES (....);
   SELECT @DataID = scope_identity();
   INSERT INTO LinkTable VALUES (@ObjectID, @DataID);
COMMIT
