--! PROFILE
-- name: usr_prof
-- fetch user's profile data
select array_to_json(array_agg(row_to_json(t)))
   from (
      SELECT U.fullname as fname, M.medadr as pix, C.cont as emel, 
      P.place as plc, P.doing as dspln, I.strt, I.endt FROM public.basics B
      JOIN public.places P ON P.plaid = B.baspl
      JOIN public.users U ON U.ddot = C.contfrom
      JOIN public.places P ON P.plaid = I.plain
      JOIN public.institution I ON I.resin = R.resid
      JOIN public.media M ON M.meid = U.ddot
      WHERE U.ddot = :usr
   ) t

-- name: pgsql
DO $$
   DECLARE 
      plc INT;
   Begin
      INSERT INTO places (usrpl, place, doing)
      VALUES (:usr, :plc, :dspln) RETURNING plaid INTO plc 
      INSERT INTO basics (basid, typ, strt, endt)
      VALUES (plc, :typ, :strtd, :endd,);
      Return ;
   End;
$$ language plpgsql;

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

-- name: base
-- accademics differentiated user basic profile
SELECT ARRAY_TO_JSON(ARRAY_AGG(row_to_json(base)))
FROM(
   SELECT B.acad as typ, B.place as plc, B.doing as dspln, B.strt, B.endt FROM public.basics B
   WHERE B.usrba = :usr
)base

-- name: skil_prof
-- general differentiated user basic profile
SELECT ARRAY_TO_JSON(ARRAY_AGG(row_to_json(base)))
FROM(
   SELECT B.acad as typ, B.place as plc, B.doing as dspln, B.strt, B.endt FROM public.basics B
   WHERE B.usrba = :usr AND B.acad = TRUE
)base

-- name: unskil_prof
-- general differentiated user basic profile
SELECT ARRAY_TO_JSON(ARRAY_AGG(row_to_json(base)))
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

-- name: acadas
-- academics profile of a user
SELECT ARRAY_TO_JSON(ARRAY_AGG(row_to_json(acadms)))
FROM(
   SELECT B.acad as typ, A.place as plc, A.doing as dspln, A.strt, A.endt, A.stage as ttl FROM public.accademics A
   JOIN public.basics B ON B.basid = A.bacid
   WHERE U.ddot = :usr
)acads

-- name: acada
-- academics profile of a user
SELECT ARRAY_TO_JSON(ARRAY_AGG(row_to_json(acadm)))
FROM(
   SELECT B.acad as typ, A.place as plc, A.doing as dspln, A.strt, A.endt, A.stage as ttl FROM public.accademics A
   JOIN public.basics B ON B.basid = A.bacid
   WHERE U.ddot = :usr ORDER BY A.strt
)acad

-- name: rsrchaqfn$
-- create user basic profile
SELECT acmid FROM public.academics A
JOIN public.basics B ON B.basid = A.bacid
WHERE B.usrba = :usr

-- name: cr8_srcha!
-- create user basic profile
WITH contat AS(
   INSERT INTO public.contacts (usrcont, cont)
   VALUES (:usr, :cnt) ON CONFLICT DO NOTHING RETURNING cntid as emel
),
base AS(
   INSERT INTO public.base (basid)
   VALUES (:base) ON CONFLICT DO NOTHING RETURNING acbas
),
rsrch AS(
   INSERT INTO public.research (basre, cntres)
   VALUES ((SELECT acbas FROM base), (SELECT emel FROM contat)) ON CONFLICT DO NOTHING RETURNING resid
)
INSERT INTO public.institution(resin, place, doing, typ, strt, endt)
VALUES((SELECT resid FROM rsrch), :org, :dspln, :typ, :strtd, :endd)
ON conflict do nothing;

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
SELECT socid FROM public.socials WHERE socid = :soc AND usrso = :usr;

-- name: del_srcha!
-- get a user
DELETE FROM public.socials WHERE socid = :soc AND usrso = :usr;

-- name: rsrchs
-- research profile of a user
SELECT ARRAY_TO_JSON(ARRAY_AGG(row_to_json(srchs)))
FROM(
   SELECT C.cont as emel, I.place as plc, I.doing as dspln, I.strt, I.endt FROM public.research R
   JOIN public.contacts C  ON C.cntid = R.cntres
   JOIN public.institution I ON I.resin = R.resid
   JOIN public.users U ON U.ddot = C.contfrom
   WHERE U.ddot = :usr
)srchs

-- name: rsrcha
-- research profile of a user
SELECT ARRAY_TO_JSON(ARRAY_AGG(row_to_json(srcha)))
FROM(
   SELECT C.cont as emel, I.place as plc, I.doing as dspln, I.strt, I.endt FROM public.research R
   JOIN public.contacts C  ON C.cntid = R.cntres
   JOIN public.institution I ON I.resin = R.resid
   JOIN public.users U ON U.ddot = C.contfrom
   WHERE U.ddot = :usr
)srcha

-- name: cr8_wrk!
-- create user basic profile
INSERT INTO public.workplace (usrwkp, place, doing, strt)
VALUES (:usr, :plc, :dng, :strtd);

-- name: cr8_Cwrk!
-- create user basic profile
INSERT INTO public.workplace (usrwkp, place, doing, strt, endt)
VALUES (:usr, :plc, :dng, :strtd, :endd);

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

-- name: wrk
-- work profile of a user
SELECT ARRAY_TO_JSON(ARRAY_AGG(row_to_json(wrk)))
FROM(
   SELECT W.place as plc,W.doing as dspln, W.strt, W.endt FROM public.workplace W
   WHERE W.usrwkp = :usr;
)wrk

-- name: wrks
-- work profile of a user
SELECT ARRAY_TO_JSON(ARRAY_AGG(row_to_json(wrks)))
FROM(
   SELECT W.place as plc,W.doing as dspln, W.strt, W.endt FROM public.workplace W
   WHERE W.usrwkp = :usr;
)wrks
