CREATE USER IF NOT EXISTS 'mlconductor'@'localhost' IDENTIFIED BY 'password';
CREATE DATABASE IF NOT EXISTS `mlcdb`;

USE `mlcdb`;

GRANT ALL PRIVILEGES ON `mlcdb`.* TO 'mlconductor'@'localhost';

CREATE TABLE IF NOT EXISTS `feature_metadata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,   
  `feature` varchar(50) NOT NULL UNIQUE,
  `feature_table` varchar(50) NOT NULL,
  `datatype` varchar(50) NOT NULL,
  `description` varchar(200),
  `data_source` varchar(200),
  PRIMARY KEY  (`id`)
);

INSERT INTO feature_metadata (feature, feature_table, datatype) VALUES ("name", "user_store", "varchar(255)");
INSERT INTO feature_metadata (feature, feature_table, datatype) VALUES ("place", "user_store", "varchar(255)");
INSERT INTO feature_metadata (feature, feature_table, datatype) VALUES ("favorite_item", "user_store", "varchar(255)");

CREATE TABLE IF NOT EXISTS `user_store` (
  `id` int(11) NOT NULL AUTO_INCREMENT,   
  `name` varchar(50) NOT NULL UNIQUE,
  `place` varchar(50) NOT NULL UNIQUE,
  `favorite_item` varchar(50) NOT NULL UNIQUE,
  PRIMARY KEY  (`id`)
);

INSERT INTO user_store (name, place, favorite_item) VALUES ("bobbie", "stamford", "my item");
