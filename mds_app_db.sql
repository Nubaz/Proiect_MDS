CREATE DATABASE IF NOT EXISTS `mds_app` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `mds_app`;

DROP TABLE IF EXISTS `pontaj`;
DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
	`id` INT NOT NULL AUTO_INCREMENT,
    `nume` VARCHAR(30) NOT NULL,
    `prenume` VARCHAR(30) NOT NULL,
    `username` VARCHAR(50) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    `parola` VARCHAR(255) NOT NULL,
    `rol` ENUM('angajat', 'manager'),
    PRIMARY KEY (`id`)
);

CREATE TABLE `pontaj` (
	`id` INT NOT NULL AUTO_INCREMENT,
    `id_ang` INT NOT NULL,
    `data_add` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `nume_pr` VARCHAR(50) NOT NULL,
    `descr_tasks` TEXT,
    `nr_ore` TINYINT UNSIGNED NOT NULL,
    `aprobat` BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY(`id`, `id_ang`),
    FOREIGN KEY(`id_ang`) REFERENCES `user`(`id`)
);