-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema creations_db
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `creations_db` ;

-- -----------------------------------------------------
-- Schema creations_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `creations_db` DEFAULT CHARACTER SET utf8 ;
USE `creations_db` ;

-- -----------------------------------------------------
-- Table `creations_db`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `creations_db`.`users` ;

CREATE TABLE IF NOT EXISTS `creations_db`.`users` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `creations_db`.`creations`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `creations_db`.`creations` ;

CREATE TABLE IF NOT EXISTS `creations_db`.`creations` (
  `creation_id` INT NOT NULL AUTO_INCREMENT,
  `message` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`creation_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `creations_db`.`users_likes_creations`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `creations_db`.`users_likes_creations` ;

CREATE TABLE IF NOT EXISTS `creations_db`.`users_likes_creations` (
  `user_id` INT NOT NULL,
  `creation_id` INT NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`user_id`, `creation_id`),
  INDEX `fk_users_has_creations_creations1_idx` (`creation_id` ASC) VISIBLE,
  INDEX `fk_users_has_creations_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_creations_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `creations_db`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_creations_creations1`
    FOREIGN KEY (`creation_id`)
    REFERENCES `creations_db`.`creations` (`creation_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
