CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
--- drop  table  objects;

CREATE TABLE public.objects (
	hashcode int8 NOT NULL,
	currentdate text NULL,
	currentime int8 NULL,
	lastdate text NULL,
	lasttime int8 NULL,
	"type" text NULL,
	frame text NULL,
	x_dim int2 NULL,
	y_dim int2 NULL,
	cam int2 NULL,
	cam_uuid uuid NULL,
	width int2 NULL,
	height int2 NULL,
	CONSTRAINT objects_pkey PRIMARY KEY (hashcode)
);
CREATE INDEX index_cam ON public.objects USING btree (cam);
CREATE INDEX index_cam_hashcode ON public.objects USING btree (cam, hashcode);
CREATE INDEX index_currentime ON public.objects USING btree (currentime DESC);
CREATE INDEX index_type ON public.objects USING btree (type);

--- drop  table  statistic;
CREATE TABLE statistic(type TEXT, currentime int8, y int2,  cam int2, hashcodes TEXT);


CREATE OR REPLACE FUNCTION currentime_gen()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS
$$
BEGIN
	RETURN extract(epoch from now())*1000;
END;
$$

-- DROP TABLE urls;

CREATE TABLE urls (
	id uuid NOT NULL DEFAULT uuid_generate_v4(),
	url varchar NOT NULL,
	cam int4 NOT NULL,
	email varchar NULL,
	os varchar(30) NULL,
	currenttime int8 NOT NULL DEFAULT currentime_gen(),
	CONSTRAINT urls_pkey PRIMARY KEY (id),
	CONSTRAINT urls_un UNIQUE (url)
);

--- drop  table  obj_stat;
CREATE TABLE obj_stat (
   cam_uuid uuid NOT NULL,
   type VARCHAR NOT NULL,
   last_10min INT,
   last_hour INT,
   last_date INT

);

CREATE INDEX index_currentime ON objects(currentime Desc);
CREATE INDEX index_type ON objects(type);
CREATE INDEX index_cam ON objects(cam Asc);
CREATE INDEX index_cam_hashcode ON objects(cam Asc, hashcode);

CREATE INDEX index_currentime_stat ON statistic(currentime Desc);


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
$$




CREATE TRIGGER modify_urls
  BEFORE UPDATE
  ON urls
  FOR  ROW
  EXECUTE PROCEDURE modify_urls();


--CREATE OR REPLACE FUNCTION modify_last_time()
--  RETURNS TRIGGER 
--  LANGUAGE PLPGSQL
--  AS
--$$
--BEGIN
--	IF NEW.cam = OLD.cam AND NEW.type = OLD.type AND ABS(NEW.hashcode - OLD.hashcode) < 1000 THEN
--         IF OLD.lasttime IS NOT NULL THEN
--    		 UPDATE objects SET currentdate = NEW.currentdate , currentime = NEW.currentime, lastdate = OLD.currentdate , lasttime = OLD.currentime WHERE cam = NEW.cam AND type = NEW.TYPE AND currentime = OLD.currentime AND ABS(NEW.hashcode - hashcode) < 30;
--         ELSE   
--         	 UPDATE objects SET currentdate = NEW.currentdate , currentime = NEW.currentime WHERE cam = NEW.cam AND type = NEW.TYPE AND currentime = OLD.currentime AND ABS(NEW.hashcode - hashcode) < 30;
--         END IF; 
--        RAISE EXCEPTION 'Record was updated, not inserted';
--	END IF;

--	IF NEW.x_dim < 60 OR NEW.y_dim < 80  THEN
---        RAISE EXCEPTION 'Image too small';
--	END IF;
--	RETURN NEW;
--END;
--$$


--CREATE TRIGGER modify_last_time
--  BEFORE INSERT
--  ON objects
--  FOR EACH ROW
--  EXECUTE PROCEDURE modify_last_time();

commit;

