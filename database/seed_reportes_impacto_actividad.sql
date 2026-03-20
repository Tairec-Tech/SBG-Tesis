-- ==========================================================
-- SEED DATA PARA REPORTES DE IMPACTO Y DE ACTIVIDADES
-- ==========================================================
-- Debes ejecutar esto DESPUÉS de db_brigadas_maracaibo.sql y 
-- de tener usuarios y brigadas creadas en tu sistema.

USE `db_brigadas_maracaibo`;

-- 1. Insertar dependencias primarias garantizadas
-- Usamos IDs en el rango 9000 para evitar chocar con datos reales.
INSERT IGNORE INTO `institucion_educativa` (`idInstitucion`, `nombre_institucion`, `direccion`, `telefono`, `logo_ruta`) VALUES
(9999, 'Institución de Pruebas', 'Calle Ficticia 123', '00000000', 'logo.png');

INSERT IGNORE INTO `brigada` (`idBrigada`, `nombre_brigada`, `area_accion`, `Institucion_Educativa_idInstitucion`) VALUES
(9999, 'Brigada de Pruebas', 'Ambiental', 9999);

INSERT IGNORE INTO `usuario` (`idUsuario`, `nombre`, `apellido`, `email`, `usuario`, `contrasena`, `rol`, `Brigada_idBrigada`, `Institucion_Educativa_idInstitucion`) VALUES
(9999, 'Admin', 'Pruebas', 'admin_9999@test.com', 'admin_9999', '1234', 'Administrador', 9999, 9999);

-- 2. Insertar Actividades de prueba vinculadas a la Brigada 9999
INSERT IGNORE INTO `actividad` (`idActividad`, `estado`, `titulo`, `descripcion`, `fecha_inicio`, `fecha_fin`, `Brigada_idBrigada`) VALUES
(9997, 'Completada', 'Recolección de Plástico en la Cañada', 'Limpieza profunda de desechos plásticos en las riberas de la cañada Morillo.', '2026-02-10', '2026-02-11', 9999),
(9998, 'Completada', 'Siembra de Árboles Autóctonos', 'Reforestación con 50 especies de cují y apamate en los alrededores del parque.', '2026-02-15', '2026-02-16', 9999),
(9999, 'En Progreso', 'Campaña de Concientización Escolar', 'Charlas en liceos sobre reciclaje y separación de origen.', '2026-02-28', '2026-03-05', 9999);

-- 3. Insertar Reportes de Actividades vinculados a las Actividades (9997-9999) y al Usuario 9999
INSERT IGNORE INTO `reporte_actividad` (`idReporte_actividad`, `resumen`, `resultado`, `Actividad_idActividad`, `Usuario_idUsuario`, `fecha_reporte`) VALUES
(9997, 'La jornada se desarrolló sin contratiempos, con toda la brigada presente. Se logró limpiar un sector de 500 metros.', 'Éxito Rotundo - 50 bolsas recolectadas', 9997, 9999, '2026-02-12 10:00:00'),
(9998, 'Se plantaron todos los árboles donados por la alcaldía. Dos brigadistas sufrieron deshidratación leve pero fueron atendidos.', 'Completado con observaciones', 9998, 9999, '2026-02-17 14:30:00'),
(9999, 'Se dio inicio a la charla en el Liceo Baralt con buena receptividad por parte de los alumnos de 5to año.', 'Evaluación inicial positiva', 9999, 9999, '2026-03-01 09:15:00');

-- 4. Insertar Reportes de Impacto vinculados a las Actividades y al Usuario 9999
INSERT IGNORE INTO `reporte_de_impacto` (`idReporte_impacto`, `contenido`, `fecha_generacion`, `Actividad_idActividad`, `Usuario_idUsuario`) VALUES
(9998, 'La remoción de plásticos en la Cañada Morillo ha disminuido el estancamiento de aguas residuales en un 40% en el sector evaluado, reduciendo drásticamente la proliferación de mosquitos transmisores de dengue reportados por la comunidad adyacente.', '2026-02-14 08:00:00', 9997, 9999),
(9999, 'La siembra de los 50 árboles contribuirá a mediano plazo (3-5 años) a la reducción de hasta 1.2 toneladas de CO2 anuales. Además, se espera que el área recupere su microclima y reduzca la temperatura local en aproximadamente 1.5°C durante el verano.', '2026-02-20 11:45:00', 9998, 9999);
