CREATE DATABASE  IF NOT EXISTS `iot_db`;
USE `iot_db`;

DROP TABLE IF EXISTS `Device`;

CREATE TABLE `Device` (
  `id` int NOT NULL AUTO_INCREMENT,
  `deviceId` varchar(45) DEFAULT NULL,
  `temperature` int DEFAULT NULL,
  `location` point DEFAULT NULL,
  `time` int(11) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=772 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
