-- Datos de prueba para ACTIVIDADES
-- Asegurarse de tener brigadas (ids 7, 8, 9 creadas en seed anterior)
USE db_brigadas_maracaibo;

INSERT INTO `actividad` (`titulo`, `descripcion`, `fecha_inicio`, `fecha_fin`, `estado`, `Brigada_idBrigada`) VALUES
('Limpieza de Plaza', 'Jornada de recolección de desechos sólidos.', CURDATE() - INTERVAL 5 DAY, CURDATE() - INTERVAL 5 DAY, 'Completada', 7),
('Charla Impacto Ambiental', 'Charla educativa a la comunidad.', CURDATE() - INTERVAL 2 DAY, CURDATE() - INTERVAL 2 DAY, 'Completada', 8),
('Reforestación Parque', 'Plantación de 50 árboles.', CURDATE() + INTERVAL 1 DAY, CURDATE() + INTERVAL 2 DAY, 'Pendiente', 9),
('Reciclaje en Escuela', 'Recolección de plástico.', CURDATE() + INTERVAL 3 DAY, CURDATE() + INTERVAL 3 DAY, 'Pendiente', 7),
('Mantenimiento Huerto', 'Riego y cuidado de plantas.', CURDATE(), CURDATE(), 'En Progreso', 8);

-- Datos de prueba para INDICADORES (para el KPI de impacto)
INSERT INTO `indicador_ambiental` (`valor`, `tipo_indicador`, `unidad`, `Actividad_idActividad`) VALUES
(45.5, 'Residuos Recolectados', 'kg', (SELECT idActividad FROM actividad WHERE titulo='Limpieza de Plaza' LIMIT 1)),
(50.0, 'Árboles Plantados', 'uni', (SELECT idActividad FROM actividad WHERE titulo='Reforestación Parque' LIMIT 1));
