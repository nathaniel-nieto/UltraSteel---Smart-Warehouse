-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema ultrasteeldata
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema ultrasteeldata
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `ultrasteeldata` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `ultrasteeldata` ;

-- -----------------------------------------------------
-- Table `ultrasteeldata`.`almacen`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ultrasteeldata`.`almacen` (
  `id` VARCHAR(20) NOT NULL,
  `tipo` INT NULL DEFAULT NULL,
  `operador` VARCHAR(50) NULL DEFAULT NULL,
  `fecha` DATE NULL DEFAULT NULL,
  `hora` TIME NULL DEFAULT NULL,
  `turno` ENUM('Matutino', 'Vespertino', 'Nocturno') NULL DEFAULT NULL,
  `estatus` VARCHAR(50) NULL DEFAULT 'En almacén',
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
