-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema tarea2
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema tarea2
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `tarea2` DEFAULT CHARACTER SET utf8 ;
USE `tarea2` ;

-- -----------------------------------------------------
-- Table `tarea2`.`pais`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tarea2`.`pais` (
  `id` INT NOT NULL,
  `nombre` VARCHAR(300) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tarea2`.`ciudad`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tarea2`.`ciudad` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(400) NOT NULL,
  `pais` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `index2` (`pais` ASC),
  CONSTRAINT `pais_fk`
    FOREIGN KEY (`pais`)
    REFERENCES `tarea2`.`pais` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tarea2`.`kilos_encargo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tarea2`.`kilos_encargo` (
  `id` INT NOT NULL,
  `valor` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tarea2`.`espacio_encargo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tarea2`.`espacio_encargo` (
  `id` INT NOT NULL,
  `valor` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tarea2`.`viaje`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tarea2`.`viaje` (
  `id` INT NOT NULL,
  `origen` INT NOT NULL,
  `destino` INT NOT NULL,
  `fecha_ida` TIMESTAMP NOT NULL,
  `fecha_regreso` TIMESTAMP NOT NULL,
  `kilos_disponible` INT NOT NULL,
  `espacio_disponible` INT NOT NULL,
  `email_viajero` VARCHAR(30) NOT NULL,
  `celular_viajero` VARCHAR(15) NULL,
  PRIMARY KEY (`id`),
  INDEX `origen_fk_idx` (`origen` ASC),
  INDEX `destino_fk_idx` (`destino` ASC),
  INDEX `kilos_fk_idx` (`kilos_disponible` ASC),
  INDEX `espacio_fk_idx` (`espacio_disponible` ASC),
  CONSTRAINT `origen_fk`
    FOREIGN KEY (`origen`)
    REFERENCES `tarea2`.`ciudad` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `destino_fk`
    FOREIGN KEY (`destino`)
    REFERENCES `tarea2`.`ciudad` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `kilos_fk`
    FOREIGN KEY (`kilos_disponible`)
    REFERENCES `tarea2`.`kilos_encargo` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `espacio_fk`
    FOREIGN KEY (`espacio_disponible`)
    REFERENCES `tarea2`.`espacio_encargo` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tarea2`.`encargo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tarea2`.`encargo` (
  `id` INT NOT NULL,
  `descripcion` VARCHAR(100) NOT NULL,
  `espacio` INT NOT NULL,
  `kilos` INT NOT NULL,
  `origen` INT NOT NULL,
  `destino` INT NOT NULL,
  `email_encargador` VARCHAR(30) NOT NULL,
  `celular_encargador` VARCHAR(15) NULL,
  PRIMARY KEY (`id`),
  INDEX `origen_e_fk_idx` (`origen` ASC),
  INDEX `destino_e_fk_idx` (`destino` ASC),
  INDEX `espacio_e_fk_idx` (`espacio` ASC),
  INDEX `kilos_e_fk_idx` (`kilos` ASC),
  CONSTRAINT `origen_e_fk`
    FOREIGN KEY (`origen`)
    REFERENCES `tarea2`.`ciudad` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `destino_e_fk`
    FOREIGN KEY (`destino`)
    REFERENCES `tarea2`.`ciudad` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `espacio_e_fk`
    FOREIGN KEY (`espacio`)
    REFERENCES `tarea2`.`espacio_encargo` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `kilos_e_fk`
    FOREIGN KEY (`kilos`)
    REFERENCES `tarea2`.`kilos_encargo` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tarea2`.`foto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tarea2`.`foto` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `ruta_archivo` VARCHAR(300) NOT NULL,
  `nombre_archivo` VARCHAR(300) NOT NULL,
  `encargo_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_foto_encargo1_idx` (`encargo_id` ASC),
  CONSTRAINT `fk_foto_encargo1`
    FOREIGN KEY (`encargo_id`)
    REFERENCES `tarea2`.`encargo` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Data for table `tarea2`.`kilos_encargo`
-- -----------------------------------------------------
START TRANSACTION;
USE `tarea2`;
INSERT INTO `tarea2`.`kilos_encargo` (`id`, `valor`) VALUES (1, '200 gr');
INSERT INTO `tarea2`.`kilos_encargo` (`id`, `valor`) VALUES (2, '500 gr');
INSERT INTO `tarea2`.`kilos_encargo` (`id`, `valor`) VALUES (3, '800 gr');
INSERT INTO `tarea2`.`kilos_encargo` (`id`, `valor`) VALUES (4, '1 kg');
INSERT INTO `tarea2`.`kilos_encargo` (`id`, `valor`) VALUES (5, '1.5 kg');
INSERT INTO `tarea2`.`kilos_encargo` (`id`, `valor`) VALUES (6, '2 kg');

COMMIT;


-- -----------------------------------------------------
-- Data for table `tarea2`.`espacio_encargo`
-- -----------------------------------------------------
START TRANSACTION;
USE `tarea2`;
INSERT INTO `tarea2`.`espacio_encargo` (`id`, `valor`) VALUES (1, '10x10x10');
INSERT INTO `tarea2`.`espacio_encargo` (`id`, `valor`) VALUES (2, '20x20x20');
INSERT INTO `tarea2`.`espacio_encargo` (`id`, `valor`) VALUES (3, '30x30x30');

COMMIT;

