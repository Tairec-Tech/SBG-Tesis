-- Datos de prueba para TURNOS
-- Relacionar con brigadas existentes (ids 7, 8, 9 del seed anterior)
USE db_brigadas_maracaibo;

-- Crear tabla si no existe
CREATE TABLE IF NOT EXISTS `turno` (
  `idTurno` INT(11) NOT NULL AUTO_INCREMENT,
  `Brigada_idBrigada` INT(11) NOT NULL,
  `fecha` DATE NOT NULL,
  `hora_inicio` TIME NOT NULL,
  `hora_fin` TIME NOT NULL,
  `ubicacion` VARCHAR(200) DEFAULT NULL,
  `notas` TEXT DEFAULT NULL,
  `estado` VARCHAR(30) NOT NULL DEFAULT 'Programado',
  `creado_en` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`idTurno`),
  KEY `fk_turno_brigada_idx` (`Brigada_idBrigada`),
  CONSTRAINT `fk_turno_brigada` FOREIGN KEY (`Brigada_idBrigada`)
    REFERENCES `brigada` (`idBrigada`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- Turnos de ejemplo vinculados a las brigadas existentes
INSERT INTO `turno` (`Brigada_idBrigada`, `fecha`, `hora_inicio`, `hora_fin`, `ubicacion`, `notas`, `estado`) VALUES
-- Brigada 7: turnos pasados y futuros
(7, CURDATE() - INTERVAL 3 DAY, '07:00:00', '09:00:00', 'Plaza Baralt, Maracaibo',         'Supervisión de zona verde',        'Completado'),
(7, CURDATE() + INTERVAL 1 DAY, '07:30:00', '10:00:00', 'Parque Vereda del Lago',          'Jornada de vigilancia matutina',    'Programado'),
(7, CURDATE() + INTERVAL 4 DAY, '14:00:00', '16:00:00', 'Cancha del Sector Los Olivos',    'Charla de concientización',         'Programado'),

-- Brigada 8: turnos variados
(8, CURDATE() - INTERVAL 1 DAY, '08:00:00', '11:00:00', 'U.E. Rafael Urdaneta',            'Inspección de áreas comunes',       'Completado'),
(8, CURDATE(),                   '13:00:00', '15:30:00', 'Jardín Botánico de Maracaibo',    'Riego y mantenimiento del huerto',  'En Progreso'),
(8, CURDATE() + INTERVAL 2 DAY, '07:00:00', '09:30:00', 'Av. Bella Vista, frente al liceo','Recorrido de supervisión ambiental','Programado'),

-- Brigada 9: turnos futuros
(9, CURDATE() + INTERVAL 1 DAY, '10:00:00', '12:00:00', 'Plaza de la República',           'Taller de reciclaje creativo',      'Programado'),
(9, CURDATE() + INTERVAL 3 DAY, '08:00:00', '10:30:00', 'Colegio San Vicente de Paúl',     'Siembra de árboles escolares',      'Programado'),
(9, CURDATE() + INTERVAL 5 DAY, '14:00:00', '16:00:00', 'Parque La Marina',                'Jornada de limpieza general',       'Programado');
