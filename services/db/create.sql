 --create database streamer;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
---drop  table  objects;

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

--drop  table  statistic;

CREATE TABLE statistic (
	"type" text NULL,
	currentime int8 NULL,
	y int2 NULL,
	hashcodes VARCHAR(410) NULL,
	cam uuid NULL
);

--drop  table  urls;

CREATE OR REPLACE FUNCTION currentime_gen()
  RETURNS int8 
  LANGUAGE PLPGSQL
  AS
$$
BEGIN
	RETURN extract(epoch from now())*1000;
END;
$$;



CREATE TABLE urls (
	id uuid NOT NULL DEFAULT uuid_generate_v4(),
	url varchar NOT NULL,
	cam int2 NOT NULL,
	email varchar NULL,
	os varchar(30) NULL,
	currenttime int8 NOT NULL DEFAULT currentime_gen(),
	CONSTRAINT urls_pkey PRIMARY KEY (id),
	CONSTRAINT urls_un UNIQUE (url)
);




CREATE OR REPLACE FUNCTION modify_urls()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS
$$
BEGIN
	IF extract(epoch from now())*1000 -  OLD.currenttime  < 10000 THEN
        RAISE EXCEPTION 'Record was not updated';
	END IF;
	RETURN NEW;
END;
$$;


CREATE TRIGGER modify_urls
  BEFORE UPDATE
  ON urls
  FOR  ROW
  EXECUTE PROCEDURE modify_urls();


CREATE TABLE Latest10min
as
select camSummary.cam , urls.url, urls.cam as rate ,"type",  count(*) from 
	(select cam ,"type" , count(*), min(objects.currentdate),  min(currentime) as starttime ,max(currentime) as endtime, (max(currentime)- min(currentime) )/1000 as seconds,  x_dim , y_dim
		from objects where extract(epoch from now()) - currentime/1000 < 36000 
		group by "type", cam, x_dim, y_dim
		having  max(currentime)- min(currentime)  > 0 and  (max(currentime)- min(currentime) )/1000 <36000
		order by cam, "type") as camSummary, urls where urls.id = camSummary.cam
group by camSummary.cam, "type", urls.url, urls.cam;

CREATE TABLE LatestHour
as
select camSummary.cam , urls.url, urls.cam as rate ,"type",  count(*) from 
	(select cam ,"type" , count(*), min(objects.currentdate),  min(currentime) as starttime ,max(currentime) as endtime, (max(currentime)- min(currentime) )/1000 as seconds,  x_dim , y_dim
		from objects where extract(epoch from now()) - currentime/1000 < 216000
		group by "type", cam, x_dim, y_dim
		having  max(currentime)- min(currentime)  > 0 and  (max(currentime)- min(currentime) )/1000 <216000
		order by cam, "type") as camSummary, urls where urls.id = camSummary.cam
group by camSummary.cam, "type", urls.url, urls.cam;

CREATE TABLE Latest6Hours
as
select camSummary.cam , urls.url, urls.cam as rate ,"type",  count(*) from 
	(select cam ,"type" , count(*), min(objects.currentdate),  min(currentime) as starttime ,max(currentime) as endtime, (max(currentime)- min(currentime) )/1000 as seconds,  x_dim , y_dim
		from objects where extract(epoch from now()) - currentime/1000 < 1296000
		group by "type", cam, x_dim, y_dim
		having  max(currentime)- min(currentime)  > 0 and  (max(currentime)- min(currentime) )/1000 <1296000
		order by cam, "type") as camSummary, urls where urls.id = camSummary.cam
group by camSummary.cam, "type", urls.url, urls.cam;

COMMIT;