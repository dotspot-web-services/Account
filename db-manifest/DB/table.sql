
CREATE DATABASE IF NOT EXISTS accountsdb;

create table IF NOT EXISTS users(
    extid BINARY(16) UNIQUE,
    ddot BIGINT PRIMARY KEY,
    fullname VARCHAR(200) NOT NULL,
    dob DATE,
    gender BOOLEAN,
    active BOOLEAN DEFAULT FALSE,
    addr VARCHAR(200) UNIQUE,
    dated TIMESTAMP with TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);
create INDEX usrdate_idx ON users USING  brin(dated);

create table IF NOT EXISTS contacts(
    cntid BIGINT PRIMARY KEY,
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
    basid BIGINT PRIMARY key,
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
    acmid BIGINT PRIMARY KEY,
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
    resid BIGINT PRIMARY KEY,
    acres INT NOT NULL,
    cntres INT NOT NULL, -- organisation/institution email for verification
    UNIQUE(acres, cntres),
    rscdt TIMESTAMP with TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT resacs_ibfk FOREIGN KEY(acres) REFERENCES academics(acmid) ON DELETE CASCADE,
    CONSTRAINT rescnt_ibfk FOREIGN KEY(cntres) REFERENCES contacts(cntid) ON DELETE CASCADE
);
CREATE INDEX rescnt_idx ON research USING btree(cntres);

CREATE TABLE IF NOT EXISTS institution(
    insid BIGINT PRIMARY KEY,
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
    wkpid BIGINT PRIMARY KEY,
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
    awid BIGINT PRIMARY KEY,
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
    socid BIGINT PRIMARY KEY,
    usrso INT NOT NULL,
    titl VARCHAR NOT NULL,
    typ VARCHAR NOT NULL,
    UNIQUE(usrso, titl),
    socdt TIMESTAMP with TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT usrawds_ibfk FOREIGN KEY(usrso) REFERENCES users(ddot) ON DELETE CASCADE
);
CREATE INDEX socdt_idx ON socials USING brin(socdt);
-- end of skill experience tables

--new phase
--DROP TABLE IF EXISTS logs;
--CREATE TABLE IF NOT EXISTS logs(--- move to mongodb as documentation data
--    usrlg INT PRIMARY KEY NOT NULL,
--    pwdlog VARCHAR(500),
--    detail JSONB,
--    logdt TIMESTAMP with TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
--    CONSTRAINT usrdlgs_ibfk FOREIGN KEY(usrlg) REFERENCES users(ddot) ON DELETE CASCADE
--);
--CREATE INDEX logdt_idx ON logs USING brin(logdt);
--CREATE INDEX logdet_idx ON logs USING gin(detail jsonb_path_ops);

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

create table IF NOT EXISTS services(
    srvceid INT PRIMARY KEY NOT NULL,
    service_ttl  VARCHAR(250) UNIQUE,
    service_desc  VARCHAR(500) UNIQUE,
    service_icon  VARCHAR(200) UNIQUE,
    approved BOOLEAN DEFAULT FALSE,
    blogdt TIMESTAMP with TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

create table IF NOT EXISTS skill(
    skilid INT PRIMARY KEY NOT NULL,
    srvce BIGINT,
    skil_ttl  VARCHAR(250) UNIQUE,
    skil_desc  VARCHAR(500) UNIQUE,
    skil_icon  VARCHAR(200) UNIQUE,
    approved BOOLEAN DEFAULT FALSE,
    skildt TIMESTAMP with TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT srvce_skfk FOREIGN KEY(srvce) REFERENCES services(srvceid) ON DELETE CASCADE
);

create table IF NOT EXISTS blog(
    blogid INT PRIMARY KEY NOT NULL,
    usr BIGINT,
    blog_title  VARCHAR(250) UNIQUE,
    blog_detail  VARCHAR(500) UNIQUE,
    approved BOOLEAN DEFAULT FALSE,
    blogdt TIMESTAMP with TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT usr_blogfk FOREIGN KEY(usr) REFERENCES users(usr) ON DELETE CASCADE
);
CREATE INDEX approved_idx ON blog USING brin(approved);

create table IF NOT EXISTS staff(
    stafid INT PRIMARY KEY NOT NULL,
    usr BIGINT,
    compromised BOOLEAN DEFAULT FALSE,
    stafdt TIMESTAMP with TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT usr_stfk FOREIGN KEY(usr) REFERENCES users(usr) ON DELETE CASCADE
);
CREATE INDEX tokdt_idx ON logToken USING brin(tokdt);

create table IF NOT EXISTS project(
    projid INT PRIMARY KEY NOT NULL,
    usr BIGINT,
    proj_title  VARCHAR(250) UNIQUE,
    proj_detail  VARCHAR(500) UNIQUE,
    proj_started BOOLEAN DEFAULT FALSE,
    projdt TIMESTAMP with TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT usr_projfk FOREIGN KEY(usr) REFERENCES users(usr) ON DELETE CASCADE
);
CREATE INDEX tokdt_idx ON logToken USING brin(tokdt);

create table IF NOT EXISTS project_resource(
    proj INT NOT NULL,
    srvce INT NOT NULL,
    strted BOOLEAN DEFAULT FALSE,
    rsrcedt TIMESTAMP with TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY(proj, srvce)
    CONSTRAINT projrestk_ibfk FOREIGN KEY(proj) REFERENCES project(projid) ON DELETE CASCADE,
    CONSTRAINT srvceprojtk_ibfk FOREIGN KEY(srvce) REFERENCES services(srvceid) ON DELETE CASCADE
);
CREATE INDEX tokdt_idx ON logToken USING brin(tokdt);

create table IF NOT EXISTS project_progress(
    proj INT PRIMARY KEY,
    token  VARCHAR(500) UNIQUE,
    logged BOOLEAN DEFAULT TRUE,
    compromised BOOLEAN DEFAULT FALSE,
    tokdt TIMESTAMP with TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT projprogtk_ibfk FOREIGN KEY(proj) REFERENCES project(projid) ON DELETE CASCADE,
);
CREATE INDEX tokdt_idx ON logToken USING brin(tokdt);
