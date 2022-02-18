
--! USER
-- name: pix!
-- fetch user's profile picture
INSERT INTO public.media (usrmed, medaddr)
VALUES (:medfor, :file_path) ON CONFLICT DO NOTHING RETURNING meid as med

-- name: pix_rit$
-- get a user
SELECT medaddr FROM PUBLIC.media WHERE meid = :med AND usrmed = :usr;

-- name: del_pix
-- get a user
DELETE FROM PUBLIC.media WHERE meid = :med AND usrmed = :usr;

-- name: pix$
-- fetch user's profile pictures
SELECT ARRAY_TO_JSON(ARRAY_AGG(row_to_json(picture)))
FROM(
   SELECT medaddr FROM PUBLIC.media
   WHERE usrmed = :usr
   ORDER BY medt;
)picture

-- name: pixs
-- fetch user's profile pictures
SELECT ARRAY_TO_JSON(ARRAY_AGG(row_to_json(pictures)))
FROM(
   SELECT medaddr FROM PUBLIC.media
   WHERE usrmed = :usr
   ORDER BY medt;
)pictures

-- name: usr_sumry
-- create user basic profile
WITH basic AS(
   SELECT U.pix, U.fullname, B.doing, FROM public.users U
),
acads AS(
   SELECT A.doing as study, R.acsre, FROM public.accademics
),
wrks AS(
   SELECT W.doing, W.strt, W.endt, Awd.titl, Awd.awdt FROM public.accademics
)
SELECT * FROM basic

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

-- name: pub$
-- fetch details of a particular publication
SELECT ARRAY_TO_JSON(ARRAY_AGG(row_to_json(publication)))
FROM(
   SELECT field, title, fyl as doc, publsdt FROM PUBLIC.pubs
   WHERE pubid = :pub
)publication

-- name: pubs
-- fetch all publications from a user
SELECT ARRAY_TO_JSON(ARRAY_AGG(row_to_json(publications)))
FROM(
   SELECT pubid as id, field, title, fyl as doc, publsdt FROM PUBLIC.pubs
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

-- name: soc$
-- fetch details of a particular social and arena performance if an arena
SELECT ARRAY_TO_JSON(ARRAY_AGG(row_to_json(social)))
FROM(
   SELECT usrso as user, titl as title, typ FROM PUBLIC.socials
   WHERE socid = :soc
)social

-- name: socs
-- fetch all non-academic social profile of user
SELECT ARRAY_TO_JSON(ARRAY_AGG(row_to_json(socials)))
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

-- name: awd$
-- fetch details of a particular award
SELECT ARRAY_TO_JSON(ARRAY_AGG(row_to_json(award)))
FROM(
   SELECT usraw as user, place, doing, titl as title, awardt FROM PUBLIC.awards
   WHERE awid = :awd
)award

-- name: awds
-- fetch all awards both from arena and created of a user
SELECT ARRAY_TO_JSON(ARRAY_AGG(row_to_json(awards)))
FROM(
   SELECT awid as id, usraw as user, place, doing, titl as title, awardt FROM PUBLIC.awards
   WHERE usraw = :usr
   ORDER BY awardt
)awards
