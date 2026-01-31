-- MySQL Script corregido para importación
-- Compatible con MariaDB 10.4.32 y MySQL 5.7+

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema db_brigadas_maracaibo
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `db_brigadas_maracaibo` DEFAULT CHARACTER SET utf8;
USE `db_brigadas_maracaibo`;

-- -----------------------------------------------------
-- Table `Institucion_Educativa`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Institucion_Educativa` (
  `idInstitucion` INT NOT NULL AUTO_INCREMENT,
  `nombre_institucion` VARCHAR(45) NOT NULL,
  `direccion` TEXT NOT NULL,
  `telefono` VARCHAR(15) NOT NULL,
  PRIMARY KEY (`idInstitucion`)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `Brigada`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Brigada` (
  `idBrigada` INT NOT NULL AUTO_INCREMENT,
  `nombre_brigada` VARCHAR(45) NOT NULL,
  `area_accion` VARCHAR(45) NOT NULL,
  `fecha_creacion` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Institucion_Educativa_idInstitucion` INT NOT NULL,
  PRIMARY KEY (`idBrigada`),
  INDEX `fk_Brigada_Institucion_Educativa_idx` (`Institucion_Educativa_idInstitucion`),
  CONSTRAINT `fk_Brigada_Institucion_Educativa`
    FOREIGN KEY (`Institucion_Educativa_idInstitucion`)
    REFERENCES `Institucion_Educativa` (`idInstitucion`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `Actividad`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Actividad` (
  `idActividad` INT NOT NULL AUTO_INCREMENT,
  `estado` VARCHAR(45) NOT NULL,
  `titulo` VARCHAR(45) NOT NULL,
  `descripcion` TEXT NOT NULL,
  `fecha_inicio` DATE NOT NULL,
  `fecha_fin` DATE NOT NULL,
  `Brigada_idBrigada` INT NOT NULL,
  PRIMARY KEY (`idActividad`),
  INDEX `fk_Actividad_Brigada1_idx` (`Brigada_idBrigada`),
  CONSTRAINT `fk_Actividad_Brigada1`
    FOREIGN KEY (`Brigada_idBrigada`)
    REFERENCES `Brigada` (`idBrigada`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `Indicador_ambiental`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Indicador_ambiental` (
  `idIndicador` INT NOT NULL AUTO_INCREMENT,
  `valor` DECIMAL(10,2) NOT NULL,
  `tipo_indicador` VARCHAR(45) NOT NULL,
  `unidad` VARCHAR(5) NOT NULL,
  `Actividad_idActividad` INT NOT NULL,
  PRIMARY KEY (`idIndicador`),
  INDEX `fk_Indicador_ambiental_Actividad1_idx` (`Actividad_idActividad`),
  CONSTRAINT `fk_Indicador_ambiental_Actividad1`
    FOREIGN KEY (`Actividad_idActividad`)
    REFERENCES `Actividad` (`idActividad`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `Usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Usuario` (
  `idUsuario` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `apellido` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `contrasena` VARCHAR(255) NOT NULL,
  `rol` VARCHAR(45) NOT NULL,
  `Brigada_idBrigada` INT NOT NULL,
  PRIMARY KEY (`idUsuario`),
  INDEX `fk_Usuario_Brigada1_idx` (`Brigada_idBrigada`),
  CONSTRAINT `fk_Usuario_Brigada1`
    FOREIGN KEY (`Brigada_idBrigada`)
    REFERENCES `Brigada` (`idBrigada`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `Reporte_de_impacto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Reporte_de_impacto` (
  `idReporte_impacto` INT NOT NULL AUTO_INCREMENT,
  `contenido` TEXT NOT NULL,
  `fecha_generacion` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Actividad_idActividad` INT NOT NULL,
  `Usuario_idUsuario` INT NOT NULL,
  PRIMARY KEY (`idReporte_impacto`),
  INDEX `fk_Reporte_de_impacto_Actividad1_idx` (`Actividad_idActividad`),
  INDEX `fk_Reporte_de_impacto_Usuario1_idx` (`Usuario_idUsuario`),
  CONSTRAINT `fk_Reporte_de_impacto_Actividad1`
    FOREIGN KEY (`Actividad_idActividad`)
    REFERENCES `Actividad` (`idActividad`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Reporte_de_impacto_Usuario1`
    FOREIGN KEY (`Usuario_idUsuario`)
    REFERENCES `Usuario` (`idUsuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
