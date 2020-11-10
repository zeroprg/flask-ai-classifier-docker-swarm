CREATE DATABASE streamer;
drop  table objects;
CREATE TABLE objects(hashcode int8 PRIMARY KEY, currentdate TEXT, currentime int8, lastdate TEXT, lasttime int8, type TEXT, frame TEXT, x_dim int, y_dim int, cam int);
drop  table statistic;
CREATE TABLE statistic(type TEXT, currentime int8, y int2,  cam int2, hashcodes TEXT);

CREATE INDEX index_currentime ON objects(currentime Desc);
CREATE INDEX index_type ON objects(type);
CREATE INDEX index_cam ON objects(cam Asc);
CREATE INDEX index_cam_hashcode ON objects(cam Asc, hashcode);
CREATE INDEX index_currentime_stat ON statistic(currentime Desc);



CREATE OR REPLACE FUNCTION modify_last_time()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS
$$
BEGIN
   IF NEW.cam = OLD.cam AND NEW.type = OLD.type AND ABS(NEW.hashcode - OLD.hashcode) < 15 THEN
         IF OLD.lasttime IS NOT NULL THEN
    		 UPDATE objects SET currentdate = NEW.currentdate , currentime = NEW.currentime, lastdate = OLD.currentdate , lasttime = OLD.currentime WHERE cam = NEW.cam AND type = NEW.TYPE AND currentime = OLD.currentime AND ABS(NEW.hashcode - hashcode) < 30;
         ELSE   
         	 UPDATE objects SET currentdate = NEW.currentdate , currentime = NEW.currentime WHERE cam = NEW.cam AND type = NEW.TYPE AND currentime = OLD.currentime AND ABS(NEW.hashcode - hashcode) < 30;
         END IF; 
        RAISE EXCEPTION 'Record was updated, not inserted';
   END IF;
   RETURN NEW;
END;
$$


CREATE TRIGGER modify_last_time
  BEFORE INSERT
  ON objects
  FOR EACH ROW
  EXECUTE PROCEDURE modify_last_time();

commit;
