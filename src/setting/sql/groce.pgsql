
--! USER
-- name: usr_prof^
-- fetch user's profile data
SELECT JSON_BUILD_OBJECT(
   'pix', ROW_TO_JSON((SELECT pix FROM(
   SELECT addr FROM PUBLIC.media WHERE usrmed = :usr ORDER BY medt
   )pix)),
   'base', ROW_TO_JSON((SELECT skill FROM(
   SELECT B.basid as id, B.place as plc, B.doing as dspln, B.strt, B.endt FROM public.basics B
   WHERE B.usrba = :usr AND B.acad = TRUE
   )skill)), 'skilled', JSON_AGG(ROW_TO_JSON((SELECT unskill FROM(
   SELECT B.basid as id, B.place as plc, B.doing as dspln, B.strt, B.endt FROM public.basics B
   WHERE B.usrba = :usr AND B.acad = FALSE
   )unskill))),
   'academic', JSON_AGG(ROW_TO_JSON((SELECT acads FROM(
   SELECT A.acmid as id, A.place as plc, A.doing as dspln, A.strt, A.endt, A.stage as ttl FROM public.academics A
   JOIN public.basics B ON B.basid = A.bacid
   WHERE B.usrba = :usr AND B.acad = TRUE
   )acads))),
   'reseacher', JSON_AGG(ROW_TO_JSON((SELECT reseach FROM(
   SELECT R.resid as resacha, C.cont as emel, I.place as plc, I.doing as dspln, I.strt, I.endt FROM public.research R
   JOIN public.contacts C  ON C.cntid = R.cntres JOIN public.institution I ON I.resin = R.resid
   JOIN public.users U ON U.ddot = C.usrcont WHERE C.usrcont = :usr
   )reseach))),
   'work', JSON_AGG(ROW_TO_JSON((SELECT works FROM(
   SELECT W.wkpid as id, W.place as plc,W.doing as dspln, W.strt, W.endt FROM public.workplace W
   WHERE W.usrwkp = :usr
   )works))),
   'publications', JSON_AGG(ROW_TO_JSON((SELECT pubs FROM(
   SELECT P.pubid as id, I.place as plc, I.doing as dspln, P.pubid as pub, P.field as area, P.title, P.publsdt FROM PUBLIC.pubs P
   JOIN public.institution I ON I.insid = P.inpub
   WHERE usrpb = :usr
   )pubs))), 'socials', JSON_AGG(ROW_TO_JSON((SELECT socs FROM(
   SELECT socid as id, usrso as user, titl as title, typ FROM PUBLIC.socials
   WHERE usrso = :usr
   ORDER BY socdt
   )socs))),
   'awards', JSON_AGG(ROW_TO_JSON((SELECT awds FROM(
   SELECT awid as id, usraw as user, place, doing, titl as title, awardt FROM PUBLIC.awards
   WHERE usraw = :usr
   ORDER BY awardt
   )awds))),
   'summary', ROW_TO_JSON((SELECT plcs FROM(
   SELECT U.fullname as name, B.acad as typ, B.place as plc, B.doing as dspln, A.place as instn, 
   A.doing as fld, A.stage as ttl, W.place as at, W.doing as wrk FROM public.basics B
   JOIN public.users U ON U.ddot = B.usrba JOIN public.academics A ON A.bacid = B.basid
   JOIN public.workplace W ON W.usrwkp = U.ddot WHERE U.ddot = :usr
   )plcs)),
   'totals', ROW_TO_JSON((SELECT totl FROM(
      SELECT COUNT(P.pubid ) as pubno, COUNT(A.awid) as awdno FROM public.users U
      JOIN PUBLIC.awards A ON A.usraw = U.ddot JOIN PUBLIC.pubs P ON P.usrpb = A.usraw
      WHERE A.usraw = :usr OR P.usrpb = :usr
   )totl))
   );
-- name: init_arena
-- fetch user's profile data that grants arena rights
SELECT ROW_TO_JSON(init)
   FROM(
      SELECT DISTINCT B.place as plc, B.doing as dspln, A.place as instn, 
      A.doing as fld, A.stage as ttl W.place as at, W.doing as wrk FROM public.basics B
      JOIN public.users U ON U.ddot = B.usrba JOIN public.academics A ON B.usrba = A.basid
      JOIN public.workplace W ON W.usrwkp = U.ddot WHERE usraw = :usr
   )init

-- name: pix!
-- insert address of user's profile picture
INSERT INTO public.media (usrmed, medaddr)
VALUES (:medfor, :file_path) ON CONFLICT DO NOTHING RETURNING meid as med;

-- name: pix_rit$
-- get a user
SELECT medaddr FROM PUBLIC.media WHERE meid = :med AND usrmed = :usr;

-- name: del_pix
-- get a user
DELETE FROM PUBLIC.media WHERE meid = :med AND usrmed = :usr;

-- name: pix$
-- fetch user's profile pictures
SELECT ROW_TO_JSON(picture)
FROM(
   SELECT addr FROM PUBLIC.media
   WHERE usrmed = :usr
   ORDER BY medt
)picture

-- name: pixs
-- fetch user's profile pictures
SELECT ROW_TO_JSON(pictures)
FROM(
   SELECT addr FROM PUBLIC.media
   WHERE usrmed = :usr
   ORDER BY medt
)pictures

-- name: cr8_pub<!
-- add a users research publication
INSERT INTO public.pubs (usrpb, inpub, field, title, fyl, publsdt)
VALUES (:usr, :instn, :fld, :ttl, :fyl, :pubdt);

-- name: upd8_pub!
-- update users research publication
INSERT INTO public.pubs (pubid, inpub, usrpb, field, title, fyl, publsdt)
VALUES (:pub, :instn, :usr, :fld, :ttl, :fyl, :pubdt) ON CONFLICT(pubid) DO UPDATE
SET field = :fld, title = :ttl, fyl = :fyl, publsdt = :pubdt WHERE pubid = :pub AND inpub = :instn;

-- name: pub_rit$
-- get a user
SELECT pubid FROM public.pubs WHERE pubid = :pub AND usrpb = :usr;

-- name: del_pub
-- get a user
DELETE FROM public.pubs WHERE pubid = :pub AND usrpb = :usr;

-- name: usr_pubs
-- fetch all publications from a user and institution
SELECT ROW_TO_JSON(publication)
FROM(
   SELECT field, title, file as doc, publsdt FROM PUBLIC.pubs
   WHERE pubid = :pub
)publication

-- name: pub^
-- fetch details of a particular publication
SELECT ROW_TO_JSON(publication)
FROM(
   SELECT field, title, file as doc, publsdt FROM PUBLIC.pubs
   WHERE pubid = :pub
)publication

-- name: pubs
-- fetch all publications 
SELECT ROW_TO_JSON(publications)
FROM(
   SELECT pubid as id, field, title, file as doc, publsdt FROM PUBLIC.pubs
   WHERE usrpb = :usr;
   ORDER BY pubdt
)publications

-- name: cr8_soc!
-- add a user's social life profile
INSERT INTO public.socials (usrso, titl, typ)
VALUES (:usr, :ttl, :typ);

-- name: upd8_soc!
-- create a user contact
INSERT INTO public.socials (socid, usrso, titl, typ)
VALUES (:soc, :usr, :ttl, :typ) ON CONFLICT(socid) DO UPDATE
SET titl = :ttl, typ = :typ WHERE socid = :soc AND usrso = :usr;

-- name: soc_rit$
-- get a user
SELECT socid FROM public.socials WHERE socid = :soc AND usrso = :usr;

-- name: del_soc!
-- get a user
DELETE FROM public.socials WHERE socid = :soc AND usrso = :usr;

-- name: usr_socs
-- fetch details of a particular social and arena performance if an arena
SELECT ROW_TO_JSON(social)
FROM(
   SELECT usrso as user, titl as title, typ FROM PUBLIC.socials
   WHERE socid = :soc
)social

-- name: socs
-- fetch all non-academic social profile of user
SELECT ROW_TO_JSON(socials)
FROM(
   SELECT socid as id, usrso as user, titl as title, typ FROM PUBLIC.socials
   WHERE usrso = :usr
   ORDER BY socdt;
)socials

-- name: cr8_awd!
-- add an a users award record
INSERT INTO public.awards (usraw, place, doing, titl, awardt)
VALUES (:usr, :plc, :acts, :ttl, :awdt);

-- name: upd8_awd!
-- create a user contact
INSERT INTO public.awards (awid, usraw, place, doing, titl, awardt)
VALUES (:awd, :usr, :plc, :acts, :ttl, :awdt) ON CONFLICT(awid) DO UPDATE
SET place = :plc, doing = :acts, titl = :ttl, awardt = :awdt WHERE awid = :awd AND usraw = :usr;

-- name: awd_rit$
-- get a user
SELECT awid FROM public.awards WHERE awid = :awd AND usraw = :usr;

-- name: del_awd!
-- get a user
DELETE FROM public.awards WHERE awid = :awd AND usraw = :usr;

-- name: usr_awds
-- fetch details of a particular award
SELECT  ROW_TO_JSON(award)
FROM(
   SELECT usraw as usr, place, doing, titl as title, awardt FROM PUBLIC.awards
   WHERE usr = :usr
)award;

-- name: awd^
-- fetch details of a particular award
SELECT ROW_TO_JSON(award)
FROM(
   SELECT usraw as user, place, doing, titl as title, awardt FROM PUBLIC.awards
   WHERE awid = :awd
)award

-- name: awds
-- fetch all awards both from arena and created of a user
SELECT ROW_TO_JSON(awards)
FROM(
   SELECT awid as id, usraw as user, place, doing, titl as title, awardt FROM PUBLIC.awards
   WHERE usraw = :usr
   ORDER BY awardt
)awards
