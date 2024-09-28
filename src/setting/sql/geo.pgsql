
-- name: prof_arenz
-- fetch user's profile data that grants arena rights
JSON_BUILD_OBJECT(
	"locations", (
		SELECT DISTINCT B.place as plc, A.place as skul, W.place as wrkpl, I.place as instuted, D.place as evnt
		FROM public.users U JOIN public.basics B ON B.usrba = U.ddot
		JOIN PUBLIC.awards D ON A.usraw = U.ddot JOIN public.contacts C  ON C.usrcont = U.ddot 
		JOIN public.research R ON R.cntid = R.cntres JOIN public.institution I ON I.resin = R.resid
		JOIN public.academics A ON B.usrba = A.basid JOIN public.workplace W ON W.usrwkp = U.ddot 
		WHERE ddot = :usr
	),
	"services", (
		SELECT DISTINCT B.doing as dspln, A.doing as fld, W.doing as wrk, D.doing as awd, I.doing as area, S.titl, S.typ
		FROM public.users U JOIN public.basics B ON B.usrba = U.ddot JOIN PUBLIC.socials S ON S.usrso = U.ddot
		JOIN PUBLIC.awards D ON A.usraw = U.ddot JOIN public.contacts C  ON C.usrcont = U.ddot 
		JOIN public.research R ON R.cntid = R.cntres JOIN public.institution I ON I.resin = R.resid
		JOIN public.academics A ON B.usrba = A.basid JOIN public.workplace W ON W.usrwkp = U.ddot 
		WHERE ddot = :usr
	)
	)

-- name: cr8_remotadr!
-- insert ip address 
INSERT INTO public.ips (ip)
VALUES (:remotaddr) ON CONFLICT DO NOTHING;

-- name: remotadr!
-- insert ip address 
SELECT ip as remotaddr FROM PUBLIC.ips WHERE ip = :remotaddr;

-- name: cr8_remoteadr_pro!
-- create user ip profile
WITH nental AS(
	INSERT INTO continent (continent_code, continent_name)
	VALUES (:nentcode, :nentname) ON CONFLICT DO NOTHING RETURNING nentid as nent
),
contry AS( 
	INSERT INTO country (
		nent, country_name, country_code2, country_code3, country_capital, calling_code, country_tld, languages, country_flag, curtime
    )
	VALUES (
		(SELECT nent FROM nental), :dcontry, :d2name, :d3name, :capi, :calcod, :domend, :langs, :flag, :curtim
	) ON CONFLICT DO NOTHING RETURNING coutid as cout
),
cty AS( 
	INSERT INTO city (couct, state_prov, district, city, zipcode, postalcode)
	VALUES ((SELECT cout FROM contry), :prov, :dist, :cty, :zip, :post) ON CONFLICT DO NOTHING RETURNING citid as cty
)
INSERT INTO globeip (citglo, ip, longitude, latitude)
VALUES ((SELECT cty FROM cty), :remadr, :longi, :lati);
ON CONFLICT DO NOTHING;
