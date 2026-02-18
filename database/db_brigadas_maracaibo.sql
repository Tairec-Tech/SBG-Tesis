-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 15-02-2026 a las 00:02:14
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- Crear y seleccionar la base de datos (evita error "Base de datos no seleccionada")
CREATE DATABASE IF NOT EXISTS `db_brigadas_maracaibo` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `db_brigadas_maracaibo`;

--
-- Base de datos: `db_brigadas_maracaibo`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `actividad`
--

CREATE TABLE `actividad` (
  `idActividad` int(11) NOT NULL,
  `estado` varchar(45) NOT NULL,
  `titulo` varchar(45) NOT NULL,
  `descripcion` text NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `Brigada_idBrigada` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `brigada`
--

CREATE TABLE `brigada` (
  `idBrigada` int(11) NOT NULL,
  `nombre_brigada` varchar(45) NOT NULL,
  `area_accion` varchar(45) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `coordinador` varchar(100) DEFAULT NULL,
  `color_identificador` varchar(20) DEFAULT '#2563eb',
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  `Institucion_Educativa_idInstitucion` int(11) NOT NULL,
  `profesor_id` int(11) DEFAULT NULL,
  `subjefe_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `indicador_ambiental`
--

CREATE TABLE `indicador_ambiental` (
  `idIndicador` int(11) NOT NULL,
  `valor` decimal(10,2) NOT NULL,
  `tipo_indicador` varchar(45) NOT NULL,
  `unidad` varchar(5) NOT NULL,
  `Actividad_idActividad` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `institucion_educativa`
--

CREATE TABLE `institucion_educativa` (
  `idInstitucion` int(11) NOT NULL,
  `nombre_institucion` varchar(45) NOT NULL,
  `direccion` text NOT NULL,
  `telefono` varchar(15) NOT NULL,
  `logo_ruta` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reporte_de_impacto`
--

CREATE TABLE `reporte_de_impacto` (
  `idReporte_impacto` int(11) NOT NULL,
  `contenido` text NOT NULL,
  `fecha_generacion` timestamp NOT NULL DEFAULT current_timestamp(),
  `Actividad_idActividad` int(11) NOT NULL,
  `Usuario_idUsuario` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `idUsuario` int(11) NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `apellido` varchar(45) NOT NULL,
  `cedula` varchar(30) DEFAULT NULL,
  `email` varchar(45) NOT NULL,
  `usuario` varchar(45) DEFAULT NULL,
  `contrasena` varchar(255) NOT NULL,
  `rol` varchar(45) NOT NULL,
  `Brigada_idBrigada` int(11) DEFAULT NULL,
  `Institucion_Educativa_idInstitucion` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `configuracion` (mensaje del día, etc.)
--
CREATE TABLE IF NOT EXISTS `configuracion` (
  `clave` varchar(64) NOT NULL,
  `valor` text DEFAULT NULL,
  `actualizado_en` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`clave`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

INSERT INTO `configuracion` (`clave`, `valor`) VALUES ('mensaje_dia', '')
ON DUPLICATE KEY UPDATE `clave` = `clave`;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `actividad`
--
ALTER TABLE `actividad`
  ADD PRIMARY KEY (`idActividad`),
  ADD KEY `fk_Actividad_Brigada1_idx` (`Brigada_idBrigada`);

--
-- Indices de la tabla `brigada`
--
ALTER TABLE `brigada`
  ADD PRIMARY KEY (`idBrigada`),
  ADD KEY `fk_Brigada_Institucion_Educativa_idx` (`Institucion_Educativa_idInstitucion`),
  ADD KEY `idx_brigada_profesor` (`profesor_id`),
  ADD KEY `idx_brigada_subjefe` (`subjefe_id`);

--
-- Indices de la tabla `indicador_ambiental`
--
ALTER TABLE `indicador_ambiental`
  ADD PRIMARY KEY (`idIndicador`),
  ADD KEY `fk_Indicador_ambiental_Actividad1_idx` (`Actividad_idActividad`);

--
-- Indices de la tabla `institucion_educativa`
--
ALTER TABLE `institucion_educativa`
  ADD PRIMARY KEY (`idInstitucion`);

--
-- Indices de la tabla `reporte_de_impacto`
--
ALTER TABLE `reporte_de_impacto`
  ADD PRIMARY KEY (`idReporte_impacto`),
  ADD KEY `fk_Reporte_de_impacto_Actividad1_idx` (`Actividad_idActividad`),
  ADD KEY `fk_Reporte_de_impacto_Usuario1_idx` (`Usuario_idUsuario`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`idUsuario`),
  ADD UNIQUE KEY `idx_usuario_unique` (`usuario`),
  ADD KEY `fk_Usuario_Brigada1_idx` (`Brigada_idBrigada`),
  ADD KEY `idx_usuario_cedula` (`cedula`),
  ADD KEY `idx_usuario_institucion` (`Institucion_Educativa_idInstitucion`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `actividad`
--
ALTER TABLE `actividad`
  MODIFY `idActividad` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `brigada`
--
ALTER TABLE `brigada`
  MODIFY `idBrigada` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `indicador_ambiental`
--
ALTER TABLE `indicador_ambiental`
  MODIFY `idIndicador` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `institucion_educativa`
--
ALTER TABLE `institucion_educativa`
  MODIFY `idInstitucion` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `reporte_de_impacto`
--
ALTER TABLE `reporte_de_impacto`
  MODIFY `idReporte_impacto` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `idUsuario` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `actividad`
--
ALTER TABLE `actividad`
  ADD CONSTRAINT `fk_Actividad_Brigada1` FOREIGN KEY (`Brigada_idBrigada`) REFERENCES `brigada` (`idBrigada`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `brigada`
--
ALTER TABLE `brigada`
  ADD CONSTRAINT `fk_Brigada_Institucion_Educativa` FOREIGN KEY (`Institucion_Educativa_idInstitucion`) REFERENCES `institucion_educativa` (`idInstitucion`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `indicador_ambiental`
--
ALTER TABLE `indicador_ambiental`
  ADD CONSTRAINT `fk_Indicador_ambiental_Actividad1` FOREIGN KEY (`Actividad_idActividad`) REFERENCES `actividad` (`idActividad`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `reporte_de_impacto`
--
ALTER TABLE `reporte_de_impacto`
  ADD CONSTRAINT `fk_Reporte_de_impacto_Actividad1` FOREIGN KEY (`Actividad_idActividad`) REFERENCES `actividad` (`idActividad`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Reporte_de_impacto_Usuario1` FOREIGN KEY (`Usuario_idUsuario`) REFERENCES `usuario` (`idUsuario`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD CONSTRAINT `fk_Usuario_Brigada1` FOREIGN KEY (`Brigada_idBrigada`) REFERENCES `brigada` (`idBrigada`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
