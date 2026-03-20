-- Datos de prueba para REPORTES DE INCIDENTES
-- Relacionar con brigadas existentes (ids 7, 8, 9 del seed_activities.sql)
USE db_brigadas_maracaibo;

-- Crear tabla si no existe
CREATE TABLE IF NOT EXISTS `reporte_incidente` (
  `idReporte` INT(11) NOT NULL AUTO_INCREMENT,
  `titulo` VARCHAR(100) NOT NULL,
  `descripcion` TEXT NOT NULL,
  `ubicacion` VARCHAR(200) NOT NULL,
  `prioridad` VARCHAR(50) NOT NULL,
  `estado` VARCHAR(50) NOT NULL DEFAULT 'En Proceso',
  `Brigada_idBrigada` INT(11) NOT NULL,
  `creado_en` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `actualizado_en` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`idReporte`),
  KEY `fk_reporte_brigada_idx` (`Brigada_idBrigada`),
  CONSTRAINT `fk_reporte_brigada` FOREIGN KEY (`Brigada_idBrigada`)
    REFERENCES `brigada` (`idBrigada`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- Múltiples ejemplos reales contextualizados en escuelas y áreas ambientales
INSERT INTO `reporte_incidente` (`titulo`, `descripcion`, `ubicacion`, `prioridad`, `estado`, `Brigada_idBrigada`, `creado_en`) VALUES
-- Brigada 7
('Fuga de agua en lavamanos', 'Se detectó un grifo roto en los baños del pasillo principal, desperdiciando agua constantemente. Se requiere reparación urgente por parte de mantenimiento.', 'Baños Pabellón A', 'Media', 'En Proceso', 7, NOW() - INTERVAL 2 DAY),
('Basura acumulada en el patio trasero', 'Luego del receso quedaron muchos envoltorios de comida en las áreas verdes traseras. La jornada de limpieza programada no fue suficiente.', 'Patio Trasero Institución', 'Baja - Situación menor', 'Resuelto', 7, NOW() - INTERVAL 6 DAY),

-- Brigada 8
('Incendio cercano a la reja oeste', 'Quema de hojas secas por parte de vecinos que generó una nube de humo afectando a los salones cercanos. El fuego ya fue extinguido.', 'Muro perimetral oeste', 'Alta - Requiere atención inmediata', 'Resuelto', 8, NOW() - INTERVAL 12 DAY),
('Árbol con riesgo de caída', 'El cují grande cercano a la cancha deportiva tiene una rama principal fracturada debido a los fuertes vientos de ayer. Existe riesgo para los estudiantes durante deportes.', 'Cancha Deportiva Central', 'Alta - Requiere atención inmediata', 'En Proceso', 8, NOW() - INTERVAL 1 DAY),
('Falta de contenedores de reciclaje', 'Los recipientes azules de la entrada principal fueron robados durante el fin de semana. No hay donde separar el plástico actualmente.', 'Entrada principal', 'Media', 'En Proceso', 8, NOW() - INTERVAL 4 DAY),

-- Brigada 9
('Abejas en el parque infantil', 'Se avistó un panal de abejas formándose en el techo del área de toboganes. Se restringió el acceso a los niños de primaria preventiva.', 'Parque Infantil / Preescolar', 'Alta - Requiere atención inmediata', 'En Proceso', 9, NOW() - INTERVAL 3 HOUR),
('Daños en el huerto escolar', 'Un perro callejero entró anoche y destruyó los semilleros de tomate y pimentón que los estudiantes de 4to año habían plantado.', 'Huerto Escolar zona este', 'Media', 'Resuelto', 9, NOW() - INTERVAL 8 DAY);
