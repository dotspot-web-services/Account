
-- name: cr8_schema
--select * from pg_stat_activity WHERE datname = 'quest';

--select pg_terminate_backend (pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'quest';

CREATE DATABASE IF NOT EXISTS accountsdb;

create table IF NOT EXISTS users(
    extid UUID DEFAULT uuid_generate_v4() UNIQUE,
    glousr INT,
    ddot SERIAL PRIMARY KEY,
    fullname VARCHAR(200) NOT NULL,
    dob DATE,
    gender BOOLEAN,
    active BOOLEAN DEFAULT FALSE,   
    dated TIMESTAMP with TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);
create INDEX usrdate_idx ON users USING  brin(dated);

create table IF NOT EXISTS contacts(
    cntid serial PRIMARY KEY,
    usrcont INT NOT NULL,
    cont VARCHAR(200) NOT NULL UNIQUE,
    email BOOLEAN DEFAULT TRUE,
    verifd BOOLEAN DEFAULT FALSE,
    contdt TIMESTAMP with TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT cntusr_ibfk FOREIGN KEY(usrcont) REFERENCES users(ddot) ON DELETE CASCADE
);
CREATE INDEX conts_idx ON contacts USING brin(contdt);

DROP TABLE IF EXISTS basics;
CREATE TABLE IF NOT EXISTS basics(-- use verifylocal to check the existence of the place
    basid serial PRIMARY key,
    usrba INT NOT NULL,
    place VARCHAR(200) NOT NULL, -- schoool or any place knowledge or skill is acquired
    doing VARCHAR(100) NOT NULL, -- departments for uni and sc
    acad BOOLEAN DEFAULT FALSE,
    strt DATE NOT NULL,
    endt DATE,
    bsdt TIMESTAMP with TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT baseusr_ibfk FOREIGN KEY(usrba) REFERENCES users(ddot) ON DELETE CASCADE
);
CREATE INDEX bsacad_idx ON basics USING btree(acad);
CREATE INDEX bsusr_idx ON basics USING btree(usrba);

CREATE TABLE IF NOT EXISTS academics(
    acmid serial PRIMARY KEY,
    bacid INT NOT NULL,
    place VARCHAR(200), -- schoool or any place knowledge or skill is acquired
    doing VARCHAR(100) NOT NULL, -- departments for uni and sc
    stage VARCHAR(50), -- ond, hnd, bsc, msc
    strt DATE NOT NULL,
    endt DATE,
    acadt TIMESTAMP with TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT acsbase_ibfk FOREIGN KEY(bacid) REFERENCES basics(basid) ON DELETE CASCADE
);
CREATE INDEX acabs_idx ON academics USING btree(bacid);

CREATE TABLE IF NOT EXISTS research(
    resid serial PRIMARY KEY,
    acres INT NOT NULL,
    cntres INT NOT NULL, -- organisation/institution email for verification
    UNIQUE(acres, cntres),
    rscdt TIMESTAMP with TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT resacs_ibfk FOREIGN KEY(acres) REFERENCES academics(acmid) ON DELETE CASCADE,
    CONSTRAINT rescnt_ibfk FOREIGN KEY(cntres) REFERENCES contacts(cntid) ON DELETE CASCADE
);
CREATE INDEX rescnt_idx ON research USING btree(cntres);

CREATE TABLE IF NOT EXISTS institution(
    insid serial PRIMARY KEY,
    resin INT NOT NULL, -- organisation/institution email for verification
    place VARCHAR(200), -- schoool or any place knowledge or skill is acquired
    doing VARCHAR(100) NOT NULL, -- departments for uni and sc
    typ BOOLEAN DEFAULT FALSE, -- 0:student, 1:coperate/ngo/medcine, 3:independent
    strt DATE NOT NULL,
    endt DATE,
    rscdt TIMESTAMP with TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT insrch_ibfk FOREIGN KEY(resin) REFERENCES research(resid) ON DELETE CASCADE
);
CREATE INDEX instyp_idx ON institution USING btree(typ);

DROP TABLE IF EXISTS workplace;
CREATE TABLE IF NOT EXISTS workplace(
    wkpid serial PRIMARY KEY,
    usrwkp INT NOT NULL,
    place VARCHAR(200), -- schoool or any place knowledge or skill is acquired
    doing VARCHAR(100) NOT NULL, -- departments for uni and sc
    strt DATE NOT NULL,
    endt DATE,
    UNIQUE(usrwkp, place, doing),
    wokdt TIMESTAMP with TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT wkpusr_ibfk FOREIGN KEY(usrwkp) REFERENCES users(ddot) ON DELETE CASCADE
);
CREATE INDEX wokdt_idx ON workplace USING brin(wokdt);

DROP TABLE IF EXISTS awards;
CREATE TABLE IF NOT EXISTS awards(
    awid serial PRIMARY KEY,
    usraw INT NOT NULL,
    place VARCHAR(200), -- schoool or any place knowledge or skill is acquired
    doing VARCHAR(100) NOT NULL, -- departments for uni and sc
    titl VARCHAR NOT NULL,
    awardt DATE NOT NULL,
    UNIQUE(place, doing, awardt),
    awdt TIMESTAMP with TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT usrawds_ibfk FOREIGN KEY(usraw) REFERENCES users(ddot) ON DELETE CASCADE
);
CREATE INDEX awdt_idx ON awards USING brin(awdt);

DROP TABLE IF EXISTS socials;
CREATE TABLE socials(
    socid serial PRIMARY KEY,
    usrso INT NOT NULL,
    titl VARCHAR NOT NULL,
    typ VARCHAR NOT NULL,
    UNIQUE(usrso, titl),
    socdt TIMESTAMP with TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT usrawds_ibfk FOREIGN KEY(usrso) REFERENCES users(ddot) ON DELETE CASCADE
);
CREATE INDEX socdt_idx ON socials USING brin(socdt);
-- end of skill experience tables

create table IF NOT EXISTS media(
    meid serial PRIMARY KEY,
    usrmed INT NOT NULL,
    addr VARCHAR(200) UNIQUE,
    medt TIMESTAMP with TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT usmed_ibfk FOREIGN KEY(usrmed) REFERENCES users(ddot) ON DELETE CASCADE,
    UNIQUE(usrmed, addr)
);
CREATE INDEX medt_idx ON media USING brin(medt);

--new phase
DROP TABLE IF EXISTS logs;
CREATE TABLE IF NOT EXISTS logs(
    usrlg INT PRIMARY KEY NOT NULL,
    pwdlog VARCHAR(500),
    detail JSONB,
    logdt TIMESTAMP with TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT usrdlgs_ibfk FOREIGN KEY(usrlg) REFERENCES users(ddot) ON DELETE CASCADE
);
CREATE INDEX logdt_idx ON logs USING brin(logdt);
CREATE INDEX logdet_idx ON logs USING gin(detail jsonb_path_ops);

DROP TABLE IF EXISTS logToken;
create table IF NOT EXISTS logToken(
    tklog INT PRIMARY KEY NOT NULL,
    token  VARCHAR(500) UNIQUE,
    logged BOOLEAN DEFAULT TRUE,
    compromised BOOLEAN DEFAULT FALSE,
    tokdt TIMESTAMP with TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT lgstk_ibfk FOREIGN KEY(tklog) REFERENCES logs(usrlg) ON DELETE CASCADE
);
CREATE INDEX tokdt_idx ON logToken USING brin(tokdt);
