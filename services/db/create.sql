 --create database streamer;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
drop  table  objects cascade;

CREATE TABLE objects (
	hashcode int8 NOT NULL,
	currentdate text NULL,
	currentime int8 NULL,
	lastdate text NULL,
	lasttime int8 NULL,
	"type" text NULL,
	frame text NULL,
	x_dim int2 NULL,
	y_dim int2 NULL,
	cam uuid NULL,
	width int2 NULL,
	height int2 NULL,
	CONSTRAINT objects_pkey PRIMARY KEY (hashcode)
);

CREATE INDEX index_cam ON objects USING btree (cam);
CREATE INDEX index_cam_hashcode ON objects USING btree (cam, hashcode);
CREATE INDEX index_currentime ON objects USING btree (currentime DESC);
CREATE INDEX index_type ON objects USING btree (type);

drop  table  statistic;

CREATE TABLE statistic (
	"type" text NULL,
	currentime int8 NULL,
	y int2 NULL,
	hashcodes VARCHAR(3000) NULL,
	cam uuid NULL
);



CREATE OR REPLACE FUNCTION currentime_gen()
  RETURNS int8 
  LANGUAGE PLPGSQL
  AS
$$
BEGIN
	RETURN extract(epoch from now())*1000;
END;
$$;

drop sequence url_cam_seq cascade;
CREATE SEQUENCE url_cam_seq;

drop  table  urls;
CREATE TABLE urls (
	id uuid NOT NULL DEFAULT uuid_generate_v4(),
	url varchar NOT NULL,
	cam int2 NULL DEFAULT nextval('url_cam_seq'::regclass),
	email varchar NULL,
	os varchar(36) NULL,
    objects_counted int4,  
	currentime int8 NOT NULL DEFAULT currentime_gen(),
	last_time_updated int8,
	idle_in_mins int4,
	CONSTRAINT urls_pkey PRIMARY KEY (id),
	CONSTRAINT urls_un UNIQUE (url)
);




CREATE OR REPLACE FUNCTION modify_urls()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS
$$
BEGIN
	if old.os is not null and old.os != new.os AND EXTRACT(EPOCH FROM NOW()) - old.currentime/1000 < 120 THEN
        RAISE EXCEPTION 'Record was not updated due to lock by another less then 120 sec. ago';
	END IF;
	RETURN NEW;
END;
$$;


CREATE TRIGGER modify_urls
  BEFORE UPDATE
  ON urls
  FOR  ROW
  EXECUTE PROCEDURE modify_urls();



CREATE OR REPLACE VIEW latest10min
AS SELECT objects.cam,
    objects.type,
    count(*) AS last10min,
    min(objects.currentdate) AS date,
    min(objects.currentime) AS starttime,
    max(objects.currentime) AS endtime,
    (max(objects.currentime) - min(objects.currentime)) / 60000 AS minutes
   FROM objects
  WHERE (date_part('epoch'::text, now()) - (objects.currentime / 1000)::double precision) < (600::double precision)
  GROUP BY objects.type, objects.cam
 HAVING ((max(objects.currentime) - min(objects.currentime)) / 60000) < 10;

    
CREATE OR REPLACE VIEW latest6hours
AS SELECT objects.cam,
    objects.type,
    count(*) AS last6hours,
    min(objects.currentdate) AS date,
    min(objects.currentime) AS starttime,
    max(objects.currentime) AS endtime,
    (max(objects.currentime) - min(objects.currentime)) / 60000 AS minutes
   FROM objects
  WHERE (date_part('epoch'::text, now()) - (objects.currentime / 1000)::double precision) < (216000::double precision * 6::double precision)
  GROUP BY objects.type, objects.cam
 HAVING ((max(objects.currentime) - min(objects.currentime)) / 60000) < 360;

CREATE OR REPLACE VIEW latest12hours
AS SELECT objects.cam,
    objects.type,
    count(*) AS last12hours,
    min(objects.currentdate) AS date,
    min(objects.currentime) AS starttime,
    max(objects.currentime) AS endtime,
    (max(objects.currentime) - min(objects.currentime)) / 60000 AS minutes
   FROM objects
  WHERE (date_part('epoch'::text, now()) - (objects.currentime / 1000)::double precision) < (216000::double precision * 12::double precision)
  GROUP BY objects.type, objects.cam
 HAVING ((max(objects.currentime) - min(objects.currentime)) / 60000) < 720;

CREATE OR REPLACE VIEW latesthour
AS SELECT objects.cam,
    objects.type,
    count(*) AS lasthour,
    min(objects.currentdate) AS date,
    min(objects.currentime) AS starttime,
    max(objects.currentime) AS endtime,
    (max(objects.currentime) - min(objects.currentime)) / 60000 AS minutes
   FROM objects
  WHERE (date_part('epoch'::text, now()) - (objects.currentime / 1000)::double precision) < (216000::double precision )
  GROUP BY objects.type, objects.cam
 HAVING ((max(objects.currentime) - min(objects.currentime)) / 60000) < 60;

create or replace view obj_stat AS
	select
		distinct u.cam,
		u.url,
		lm."type" type1,
		max(lm.last10min) last10min,
		l."type" type2 ,
		max(l.lasthour) lasthour ,
		l6."type" type3,
		max(l6.last6hours) last6hours
	from
		urls u
	left join latest10min lm on
		lm.cam = u.id
	left join latesthour l on
		lm.cam = u.id
	left join latest6hours l6 on
		l6.cam = u.id
	group by
		u.cam,
		u.url,
		lm."type",
		l."type" ,
		l6."type" 
;


COMMIT;