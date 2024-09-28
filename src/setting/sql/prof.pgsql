--! PROFILE
-- name: cr8_base!
-- create user basic profile
INSERT INTO public.basics (usrba, place, doing, acad, strt, endt)
VALUES (:usr, :plc, :dspln, :typ, :strtd, :endd);

-- name: upd8_base!
-- create a user contact
INSERT INTO public.basics (basid, usrba, place, doing, acad, strt, endt)
VALUES (:base, :usr, :plc, :dspln, :typ, :strtd, :endd) ON CONFLICT(socid) DO UPDATE
SET place = :plc, doing = :dspln, strt = :strtd, endt = endt WHERE basid = :base AND usrba = :usr;

-- name: base_rit$
-- get a user
SELECT basid FROM public.basics WHERE basid = :base AND usrba = :usr;

-- name: del_base!
-- get a user
DELETE FROM public.basics WHERE basid = :base AND usrba = :usr;

-- name: usr_base^
-- accademics differentiated user basic profile
SELECT ROW_TO_JSON(base)
FROM(
   SELECT B.acad as typ, B.place as plc, B.doing as dspln, B.strt, B.endt FROM public.basics B
   WHERE B.usrba = :usr
)base

-- name: base^
-- accademics differentiated user basic profile
SELECT ROW_TO_JSON(base)
FROM(
   SELECT B.acad as typ, B.place as plc, B.doing as dspln, B.strt, B.endt FROM public.basics B
   WHERE B.basid = :base
)base

-- name: skil_prof
-- general differentiated user basic profile
SELECT ROW_TO_JSON(base)
FROM(
   SELECT B.acad as typ, B.place as plc, B.doing as dspln, B.strt, B.endt FROM public.basics B
   WHERE B.usrba = :usr AND B.acad = TRUE
)base

-- name: unskil_prof
-- general differentiated user basic profile
SELECT ROW_TO_JSON(base)
FROM(
   SELECT B.acad as typ, B.place as plc, B.doing as dspln, B.strt, B.endt FROM public.basics B
   WHERE B.usrba = :usr AND B.acad = FALSE
)base

-- name: acadqfn$
-- create user basic profile
SELECT basid FROM public.basics B WHERE B.usrba = :usr AND B.acad IS TRUE;

-- name: cr8_acad!
-- create user basic profile
INSERT INTO public.academics (bacid, place, doing, stage, strt, endt)
VALUES (:base, :plc, :dspln, :stg, :strtd, :endd);

-- name: upd8_acad!
-- create a user contact
INSERT INTO public.academics (acmid, bacid, place, doing, acad, strt, endt)
VALUES (:acad, :base, :plc, :dspln, :typ, :strtd, :endd) ON CONFLICT(acmid) DO UPDATE
SET place = :plc, doing = :dspln, strt = :strtd, endt = endt WHERE acmid = :acad AND bacid = :base;

-- name: acad_rit$
-- get a user
SELECT acmid FROM public.academics WHERE acmid = :soc AND usrso = :usr;

-- name: del_acad!
-- get a user
DELETE FROM public.academics WHERE acmid = :soc AND usrso = :usr;

-- name: usr_acada
-- academics profile of a user
SELECT ROW_TO_JSON(acadm)
FROM(
   SELECT B.acad as typ, A.place as plc, A.doing as dspln, A.strt, A.endt, A.stage as ttl FROM public.academics A
   JOIN public.basics B ON B.basid = A.bacid
   WHERE B.usrba = :usr
)acadm

-- name: acada^
-- academics profile of a user
SELECT ROW_TO_JSON(acadm)
FROM(
   SELECT B.acad as typ, A.place as plc, A.doing as dspln, A.strt, A.endt, A.stage as ttl FROM public.academics A
   JOIN public.basics B ON B.basid = A.bacid
   WHERE A.acmid = :acad
)acadm

-- name: acadas
-- academics profile of a user
SELECT ROW_TO_JSON(acadms)
FROM(
   SELECT B.acad as typ, A.place as plc, A.doing as dspln, A.strt, A.endt, A.stage as ttl FROM public.academics A
   JOIN public.basics B ON B.basid = A.bacid
   WHERE B.usrba = :usr ORDER BY A.strt
)acadms

-- name: rsrchaqfn$
-- create user basic profile
SELECT acmid FROM public.academics A
JOIN public.basics B ON B.basid = A.bacid
WHERE B.usrba = :usr

-- name: cr8_srcha!
-- create user basic profile
WITH cont AS(
   INSERT INTO public.contacts (usrcont, cont)
   VALUES (:usr, :cnt) ON CONFLICT DO NOTHING RETURNING cntid as emel
),
rsrch AS( 
   INSERT INTO public.research (cntres, acres)
   VALUES ((SELECT emel FROM cont), :base) ON CONFLICT DO NOTHING RETURNING resid
)
INSERT INTO public.institution(resin, place, doing, typ, strt, endt)
VALUES((SELECT resid FROM rsrch), :org, :dspln, :typ, :strtd, :endd)
ON CONFLICT DO NOTHING;

-- name: upd8_srcha!
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
SET verifd = :verfd WHERE acmid = :acad AND bacid = :base;

-- name: srcha_rit$
-- get a user
SELECT socid FROM public.contacts 
JOIN public.research R ON C.contfro = R.contres
JOIN public.institution I ON I.resin = R.resid
WHERE I.resin = :instn AND usrso = :usr;

-- name: del_srcha!
-- get a user
DELETE FROM public.contacts C
JOIN public.research R ON C.contfro = R.contres
JOIN public.institution I ON I.resin = R.resid
WHERE I.resin = :instn AND usrso = :usr;

-- name: rsrcha
-- research profile of a user
SELECT ROW_TO_JSON(rsrcha)
FROM(
   SELECT C.cont as emel, I.place as plc, I.doing as dspln, I.strt, I.endt FROM public.research R
   JOIN public.contacts C  ON C.cntid = R.cntres
   JOIN public.institution I ON I.resin = R.resid
   JOIN public.users U ON U.ddot = C.usrcont
   WHERE C.usrcont = :usr
)rsrcha

-- name: arsrcha
-- research profile of a user
SELECT ROW_TO_JSON(rsrcha)
FROM(
   SELECT C.cont as emel, I.place as plc, I.doing as dspln, I.strt, I.endt FROM public.research R
   JOIN public.contacts C  ON C.cntid = R.cntres
   JOIN public.institution I ON I.resin = R.resid
   JOIN public.users U ON U.ddot = C.contfrom
   WHERE C.usrcont = :usr
)rsrcha

-- name: srchas
-- research profile of a user
SELECT ROW_TO_JSON(srchas)
FROM(
   SELECT C.cont as emel, I.place as plc, I.doing as dspln, I.strt, I.endt FROM public.research R
   JOIN public.contacts C  ON C.cntid = R.cntres
   JOIN public.institution I ON I.resin = R.resid
   JOIN public.users U ON U.ddot = C.contfrom
   WHERE C.usrcont = :usr
)srchas

-- name: cr8_wrk!
-- create user basic profile
INSERT INTO public.workplace (usrwkp, place, doing, strt)
VALUES (:usr, :plc, :dng, :strtd) ON CONFLICT DO NOTHING;

-- name: cr8_Cwrk!
-- create user basic profile
INSERT INTO public.workplace (usrwkp, place, doing, strt, endt)
VALUES (:usr, :plc, :dng, :strtd, :endd) ON CONFLICT DO NOTHING;

-- name: upd8_wrk!
-- create a user contact
INSERT INTO public.workplace (wkpid, usrwkp, place, doing, acad, strt, endt)
VALUES (:wrk, :usr, :plc, :dspln, :typ, :strtd, :endd) ON CONFLICT(wkpid) DO UPDATE
SET place = :plc, doing = :dspln, strt = :strtd, endt = endt WHERE wkpid = :wrk AND usrwkp = :usr;

-- name: wrk_rit$
-- get a user
SELECT wkpid FROM public.workplace WHERE wkpid = :wrk AND usrwkp = :usr;

-- name: del_wrk!
-- get a user
DELETE FROM public.workplace WHERE wkpid = :wrk AND usrwkp = :usr;

-- name: usr_wrk
-- work profile of a user
SELECT ROW_TO_JSON(wrk)
FROM(
   SELECT W.place as plc,W.doing as dspln, W.strt, W.endt FROM public.workplace W
   WHERE W.usrwkp = :usr
)wrk

-- name: wrk
-- work profile of a user
SELECT ROW_TO_JSON(wrk)
FROM(
   SELECT W.place as plc,W.doing as dspln, W.strt, W.endt FROM public.workplace W
   WHERE W.usrwkp = :work
)wrk

-- name: wrks
-- work profile of a user
SELECT ROW_TO_JSON(wrks)
FROM(
   SELECT W.place as plc,W.doing as dspln, W.strt, W.endt FROM public.workplace W
   WHERE W.usrwkp = :usr
)wrks
