CREATE DATABASE streamer;
--drop  table objects;
CREATE TABLE objects(hashcode TEXT PRIMARY KEY, currentdate DATE, currentime bigint, lastdate DATE, lasttime bigint, type TEXT, frame TEXT, x_dim int, y_dim int, cam int);
--drop  table statistic;
CREATE TABLE statistic(type TEXT, currentime bigint, y int2,  cam int2, hashcodes TEXT);

CREATE INDEX index_currentime ON objects(currentime Desc);
CREATE INDEX index_type ON objects(type);
CREATE INDEX index_cam ON objects(cam Asc);
CREATE INDEX index_currentime_stat ON statistic(currentime Desc);



CREATE OR REPLACE FUNCTION modify_last_time()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS
$$
BEGIN
	IF NEW.cam == OLD.cam AND NEW.type == OLD.type AND NEW.hashcode - OLD.hashcode < 30 AND NEW.hashcode - OLD.hashcode >-30 THEN
         IF OLD.lasttime IS NOT NULL THEN
    		 UPDATE objects SET currentdate = NEW.currentdate , currenttime = NEW.currenttime, lastdate = OLD.currentdate , lasttime = OLD.currenttime
         ELSE IF    
         	 UPDATE objects SET currentdate = NEW.currentdate , currenttime = NEW.currenttime
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
