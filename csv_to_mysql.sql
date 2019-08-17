LOAD DATA INFILE 'punt_csv.txt'
INTO TABLE nfl_reg_season_punts_2000 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
SET time = STR_TO_DATE(@Time, '%i:%s')
SET date = STR_TO_DATE(@Date, '%Y-%M-%d');