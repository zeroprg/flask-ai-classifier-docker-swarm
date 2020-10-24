CREATE DATABASE streamer;
--drop  table objects;
CREATE TABLE objects(hashcode TEXT PRIMARY KEY, currentdate DATE, currentime bigint, type TEXT, frame TEXT, x_dim int, y_dim int, cam int);
--drop  table statistic;
CREATE TABLE statistic(type TEXT, currentime bigint, y int2, text TEXT, cam int2, lastime bigint, hashcodes TEXT);

CREATE INDEX index_currentime ON objects(currentime);
CREATE INDEX index_currentime_stat ON statistic(currentime);
CREATE INDEX index_lastime_stat ON statistic(lastime);

commit;
