GRANT ALL PRIVILEGES ON SCHEMA public TO odroid;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO odroid;


CREATE OR REPLACE FUNCTION generate_random_uuid()
RETURNS UUID AS $$
BEGIN
    RETURN uuid_in(
        overlay(
            overlay(
                md5(random()::text || ':' || random()::text)
                placing '4' from 13
            )
            placing to_hex(floor(random()*(11-8+1) + 8)::int)::text from 17
        )::cstring
    );
END;
$$ LANGUAGE plpgsql;


SELECT generate_random_uuid();

DROP TABLE IF EXISTS objects CASCADE;


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
CREATE UNIQUE INDEX objects_hashcode_idx ON public.objects USING btree (hashcode);
CREATE INDEX index_currentime ON objects USING btree (currentime DESC);
CREATE INDEX index_type ON objects USING btree (type);
CREATE INDEX objects_cam_idx ON public.objects (cam,currentime);


DROP TABLE IF EXISTS statistic CASCADE;


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

DROP SEQUENCE IF EXISTS url_cam_seq CASCADE;


CREATE SEQUENCE url_cam_seq;

DROP TABLE IF EXISTS urls;
CREATE TABLE urls (
	id uuid NOT NULL DEFAULT generate_random_uuid(),
	url varchar NOT NULL,
	cam int4 NULL DEFAULT nextval('url_cam_seq'::regclass),
	email varchar NULL,
	os varchar(36) NULL,
	last_time_updated int8 NOT NULL DEFAULT 0,
    objects_counted int4  NOT NULL DEFAULT -1,
	lat float4,
	lng float4,
	city varchar(25) null,
	postalcode varchar(10) null,
	region varchar(25) null,
	country varchar(25) null,
	currentime int8 NOT NULL DEFAULT currentime_gen(),
	idle_in_mins int4  DEFAULT 0,	
	"desc" varchar(500) null,
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

select count(*) from urls;
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
SELECT count(*) FROM pg_stat_activity;
select count(*) from objects WHERE currentime < (EXTRACT(EPOCH FROM NOW()) * 1000) - (14 * 24 * 60 * 60 * 1000);
delete  from objects WHERE currentime < (EXTRACT(EPOCH FROM NOW()) * 1000) - (14 * 24 * 60 * 60 * 1000);