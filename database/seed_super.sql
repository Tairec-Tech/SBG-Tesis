-- ================================================================
-- SUPER SEED — SBE (Sistema de Brigadas Escolares)
-- Datos completos para los 4 tipos de brigada.
-- Ejecutar DESPUÉS de db_brigadas_maracaibo.sql + migraciones.
-- ================================================================
-- Contraseñas (SHA-256 legacy):
--   director   → director123
--   profesor1-8 → profesor1 ... profesor8
--   alumnos    → alumno123
-- ================================================================

USE db_brigadas_maracaibo;

-- ══════════════════════════════════════════════════════════════
-- 1. INSTITUCIÓN
-- ══════════════════════════════════════════════════════════════
INSERT INTO `institucion_educativa`
  (`idInstitucion`, `nombre_institucion`, `direccion`, `telefono`, `logo_ruta`)
VALUES
  (1, 'U.E. Libertador Simón Bolívar', 'Av. Universidad, Maracaibo, Zulia', '04247313983', NULL)
ON DUPLICATE KEY UPDATE `nombre_institucion` = VALUES(`nombre_institucion`);

-- ══════════════════════════════════════════════════════════════
-- 2. BRIGADAS — 2 por cada tipo (8 brigadas, IDs 101-108)
-- ══════════════════════════════════════════════════════════════
INSERT INTO `brigada`
  (`idBrigada`, `nombre_brigada`, `area_accion`, `descripcion`, `coordinador`,
   `color_identificador`, `tipo_brigada`, `fecha_creacion`,
   `Institucion_Educativa_idInstitucion`, `profesor_id`, `subjefe_id`)
VALUES
-- ── Ecológica ──
(101, 'Brigada Verde',        'Medio Ambiente',    'Cuidado de áreas verdes, reciclaje y reforestación escolar.',     NULL, '#059669', 'ecologica',    NOW(), 1, NULL, NULL),
(102, 'Guardianes del Planeta','Conservación',      'Monitoreo de consumo de agua y energía en la institución.',       NULL, '#10b981', 'ecologica',    NOW(), 1, NULL, NULL),

-- ── Gestión de Riesgo ──
(103, 'Brigada de Emergencias', 'Evacuación',       'Simulacros, primeros auxilios y rutas de evacuación.',            NULL, '#dc2626', 'riesgo',       NOW(), 1, NULL, NULL),
(104, 'Centinelas del Riesgo', 'Prevención',        'Detección temprana de riesgos estructurales y ambientales.',      NULL, '#ef4444', 'riesgo',       NOW(), 1, NULL, NULL),

-- ── Patrulla Escolar ──
(105, 'Patrulla Segura',      'Tránsito Escolar',  'Control de paso peatonal y orden en las entradas y salidas.',     NULL, '#ea580c', 'patrulla',     NOW(), 1, NULL, NULL),
(106, 'Vigías del Cruce',     'Seguridad Vial',    'Señalización y apoyo a peatones en las zonas escolares.',         NULL, '#f97316', 'patrulla',     NOW(), 1, NULL, NULL),

-- ── Convivencia y Paz ──
(107, 'Promotores de Paz',    'Mediación',         'Resolución pacífica de conflictos y promoción de valores.',       NULL, '#64748b', 'convivencia',  NOW(), 1, NULL, NULL),
(108, 'Escuadrón Armonía',    'Bienestar Escolar', 'Campañas antibullying y actividades de integración.',             NULL, '#94a3b8', 'convivencia',  NOW(), 1, NULL, NULL);

-- ══════════════════════════════════════════════════════════════
-- 3. DIRECTIVO (ID 201)
-- ══════════════════════════════════════════════════════════════
-- usuario: director | contraseña: director123 (SHA-256)
INSERT INTO `usuario`
  (`idUsuario`, `nombre`, `apellido`, `cedula`, `email`, `usuario`, `contrasena`, `rol`,
   `Brigada_idBrigada`, `Institucion_Educativa_idInstitucion`)
VALUES
(201, 'Ricardo', 'Mendoza Pérez', 'V-12345678', 'director@uelibertador.edu.ve', 'director',
  '9e4d7bba246abe731743986c4dc50897b68b1d0249a066abb3530fcbaa33dab3', 'Directivo', NULL, 1);

-- ══════════════════════════════════════════════════════════════
-- 4. PROFESORES (IDs 202-209, 8 profesores)
-- ══════════════════════════════════════════════════════════════
-- Cada profesor tiene usuario = profesorN, contraseña = profesorN (SHA-256)
INSERT INTO `usuario`
  (`idUsuario`, `nombre`, `apellido`, `cedula`, `email`, `usuario`, `contrasena`, `rol`,
   `Brigada_idBrigada`, `Institucion_Educativa_idInstitucion`)
VALUES
-- Ecológica
(202, 'Carlos',   'Martínez López',   'V-11000001', 'cmartinez@uelibertador.edu.ve',  'profesor1',
  'c5feadda95f15c08186641ec217bfde3ac211298f1912798610ef6532c7ffe1f', 'Profesor', 101, 1),
(203, 'Mariana',  'Colmenares Rivas', 'V-11000002', 'mcolmenares@uelibertador.edu.ve','profesor2',
  'c59036fb2b020cac117abc9e4647f54bac565eddbb5aa209f9e78e5269e0ec42', 'Profesor', 102, 1),

-- Gestión de Riesgo
(204, 'José',     'Hernández Gil',    'V-11000003', 'jhernandez@uelibertador.edu.ve', 'profesor3',
  'fa2eef54e73154938645d3b4d6207acf5b602188f4ae96ffb0863ac5fa2ad236', 'Profesor', 103, 1),
(205, 'Laura',    'Pérez Montiel',    'V-11000004', 'lperez@uelibertador.edu.ve',     'profesor4',
  '7bea9b88144d12640909c0fbe039abd95317bd17910e9b02dce48da2b47400c8', 'Profesor', 104, 1),

-- Patrulla Escolar
(206, 'Pedro',    'Urdaneta Bracho',  'V-11000005', 'purdaneta@uelibertador.edu.ve',  'profesor5',
  '007135061d2d39a4a5d676fda2e6e5cdf36d805b7ba95702ea6be37f39016287', 'Profesor', 105, 1),
(207, 'Carmen',   'Fuentes Nava',     'V-11000006', 'cfuentes@uelibertador.edu.ve',   'profesor6',
  'c43dfb1540a445e440543b25c2cec09e1af826cf55ea3527345cce54541412d2', 'Profesor', 106, 1),

-- Convivencia y Paz
(208, 'Andrés',   'Romero Villalobos','V-11000007', 'aromero@uelibertador.edu.ve',    'profesor7',
  '916751e2461a8f8cb63a509f004a378566d51e06cd7c65f80c28ced489dfdc83', 'Profesor', 107, 1),
(209, 'Gabriela', 'Torres Dávila',    'V-11000008', 'gtorres@uelibertador.edu.ve',    'profesor8',
  '8146bfdf6da999566185928f47d02ab23ef1c296031a209ccf987bdbcc89d0c2', 'Profesor', 108, 1);

-- Asignar profesores a sus brigadas
UPDATE `brigada` SET `profesor_id` = 202 WHERE `idBrigada` = 101;
UPDATE `brigada` SET `profesor_id` = 203 WHERE `idBrigada` = 102;
UPDATE `brigada` SET `profesor_id` = 204 WHERE `idBrigada` = 103;
UPDATE `brigada` SET `profesor_id` = 205 WHERE `idBrigada` = 104;
UPDATE `brigada` SET `profesor_id` = 206 WHERE `idBrigada` = 105;
UPDATE `brigada` SET `profesor_id` = 207 WHERE `idBrigada` = 106;
UPDATE `brigada` SET `profesor_id` = 208 WHERE `idBrigada` = 107;
UPDATE `brigada` SET `profesor_id` = 209 WHERE `idBrigada` = 108;

-- ══════════════════════════════════════════════════════════════
-- 5. ALUMNOS — 6 por brigada (48 alumnos, IDs 301-348)
--    Nombres realistas venezolanos
--    contraseña: alumno123 (SHA-256)
-- ══════════════════════════════════════════════════════════════
-- Hash de alumno123:
-- c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0

-- Brigada 101 — Brigada Verde (ecologica)
INSERT INTO `usuario` (`idUsuario`, `nombre`, `apellido`, `cedula`, `email`, `usuario`, `contrasena`, `rol`, `Brigada_idBrigada`, `Institucion_Educativa_idInstitucion`) VALUES
(301, 'Miguel',    'Sánchez Ríos',     'V-30100001', 'msanchez301@uel.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 101, NULL),
(302, 'Valeria',   'Gómez Pineda',     'V-30100002', 'vgomez302@uel.edu.ve',   NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 101, NULL),
(303, 'Sebastián', 'Morales Castro',   'V-30100003', 'smorales303@uel.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 101, NULL),
(304, 'Isabella',  'Ferrer Quintero',  'V-30100004', 'iferrer304@uel.edu.ve',  NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 101, NULL),
(305, 'Daniel',    'Ochoa Villalobos', 'V-30100005', 'dochoa305@uel.edu.ve',   NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 101, NULL),
(306, 'Camila',    'Parra Briceño',    'V-30100006', 'cparra306@uel.edu.ve',   NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 101, NULL);

-- Brigada 102 — Guardianes del Planeta (ecologica)
INSERT INTO `usuario` (`idUsuario`, `nombre`, `apellido`, `cedula`, `email`, `usuario`, `contrasena`, `rol`, `Brigada_idBrigada`, `Institucion_Educativa_idInstitucion`) VALUES
(307, 'Andrés',    'Delgado Urdaneta', 'V-30100007', 'adelgado307@uel.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 102, NULL),
(308, 'Sofía',     'Linares Molina',   'V-30100008', 'slinares308@uel.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 102, NULL),
(309, 'Alejandro', 'Rincón Vargas',    'V-30100009', 'arincon309@uel.edu.ve',  NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 102, NULL),
(310, 'Gabriela',  'Chacón Nava',      'V-30100010', 'gchacon310@uel.edu.ve',  NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 102, NULL),
(311, 'Tomás',     'Vera Suárez',      'V-30100011', 'tvera311@uel.edu.ve',    NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 102, NULL),
(312, 'María',     'Zambrano Paz',     'V-30100012', 'mzambrano312@uel.edu.ve',NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 102, NULL);

-- Brigada 103 — Brigada de Emergencias (riesgo)
INSERT INTO `usuario` (`idUsuario`, `nombre`, `apellido`, `cedula`, `email`, `usuario`, `contrasena`, `rol`, `Brigada_idBrigada`, `Institucion_Educativa_idInstitucion`) VALUES
(313, 'Eduardo',   'Méndez Contreras', 'V-30200001', 'emendez313@uel.edu.ve',  NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 103, NULL),
(314, 'Fernanda',  'Araujo Becerra',   'V-30200002', 'faraujo314@uel.edu.ve',  NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 103, NULL),
(315, 'Nicolás',   'Bracho Lugo',      'V-30200003', 'nbracho315@uel.edu.ve',  NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 103, NULL),
(316, 'Daniela',   'Escalona Ruiz',    'V-30200004', 'descalona316@uel.edu.ve',NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 103, NULL),
(317, 'Rafael',    'Perozo Medina',    'V-30200005', 'rperozo317@uel.edu.ve',  NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 103, NULL),
(318, 'Lucía',     'Camacho Isea',     'V-30200006', 'lcamacho318@uel.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 103, NULL);

-- Brigada 104 — Centinelas del Riesgo (riesgo)
INSERT INTO `usuario` (`idUsuario`, `nombre`, `apellido`, `cedula`, `email`, `usuario`, `contrasena`, `rol`, `Brigada_idBrigada`, `Institucion_Educativa_idInstitucion`) VALUES
(319, 'Santiago',  'Guerrero Finol',   'V-30200007', 'sguerrero319@uel.edu.ve',NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 104, NULL),
(320, 'Antonella', 'Ávila Pacheco',    'V-30200008', 'aavila320@uel.edu.ve',   NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 104, NULL),
(321, 'Matías',    'Pirela Soto',      'V-30200009', 'mpirela321@uel.edu.ve',  NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 104, NULL),
(322, 'Valentina', 'Leal Andrade',     'V-30200010', 'vleal322@uel.edu.ve',    NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 104, NULL),
(323, 'Emilio',    'Borjas Ramírez',   'V-30200011', 'eborjas323@uel.edu.ve',  NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 104, NULL),
(324, 'Mariane',   'Quintero Díaz',    'V-30200012', 'mquintero324@uel.edu.ve',NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 104, NULL);

-- Brigada 105 — Patrulla Segura (patrulla)
INSERT INTO `usuario` (`idUsuario`, `nombre`, `apellido`, `cedula`, `email`, `usuario`, `contrasena`, `rol`, `Brigada_idBrigada`, `Institucion_Educativa_idInstitucion`) VALUES
(325, 'Diego',     'Montilla Torres',  'V-30300001', 'dmontilla325@uel.edu.ve',NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 105, NULL),
(326, 'Paula',     'Atencio Herrera',  'V-30300002', 'patencio326@uel.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 105, NULL),
(327, 'David',     'Ortega Colina',    'V-30300003', 'dortega327@uel.edu.ve',  NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 105, NULL),
(328, 'Andrea',    'Salas Moreno',     'V-30300004', 'asalas328@uel.edu.ve',   NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 105, NULL),
(329, 'Joaquín',   'Rivas Camacho',    'V-30300005', 'jrivas329@uel.edu.ve',  NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 105, NULL),
(330, 'Sara',      'Portillo León',    'V-30300006', 'sportillo330@uel.edu.ve',NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 105, NULL);

-- Brigada 106 — Vigías del Cruce (patrulla)
INSERT INTO `usuario` (`idUsuario`, `nombre`, `apellido`, `cedula`, `email`, `usuario`, `contrasena`, `rol`, `Brigada_idBrigada`, `Institucion_Educativa_idInstitucion`) VALUES
(331, 'Lucas',     'Sulbarán Conde',   'V-30300007', 'lsulbaran331@uel.edu.ve',NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 106, NULL),
(332, 'Martina',   'Navarro Petit',    'V-30300008', 'mnavarro332@uel.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 106, NULL),
(333, 'Samuel',    'Ferrer Bracho',    'V-30300009', 'sferrer333@uel.edu.ve',  NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 106, NULL),
(334, 'Elena',     'Matos Useche',     'V-30300010', 'ematos334@uel.edu.ve',   NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 106, NULL),
(335, 'Adrián',    'Labarca Ochoa',    'V-30300011', 'alabarca335@uel.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 106, NULL),
(336, 'Victoria',  'Angulo Baptista',  'V-30300012', 'vangulo336@uel.edu.ve',  NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 106, NULL);

-- Brigada 107 — Promotores de Paz (convivencia)
INSERT INTO `usuario` (`idUsuario`, `nombre`, `apellido`, `cedula`, `email`, `usuario`, `contrasena`, `rol`, `Brigada_idBrigada`, `Institucion_Educativa_idInstitucion`) VALUES
(337, 'Francisco', 'Barrios Acosta',   'V-30400001', 'fbarrios337@uel.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 107, NULL),
(338, 'Natalia',   'Villegas Cedeño',  'V-30400002', 'nvillegas338@uel.edu.ve',NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 107, NULL),
(339, 'Manuel',    'Toro Miranda',     'V-30400003', 'mtoro339@uel.edu.ve',    NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 107, NULL),
(340, 'Carolina',  'Peña Romero',      'V-30400004', 'cpena340@uel.edu.ve',    NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 107, NULL),
(341, 'Simón',     'Urdaneta Fuentes', 'V-30400005', 'surdaneta341@uel.edu.ve',NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 107, NULL),
(342, 'Irene',     'Medina Leal',      'V-30400006', 'imedina342@uel.edu.ve',  NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 107, NULL);

-- Brigada 108 — Escuadrón Armonía (convivencia)
INSERT INTO `usuario` (`idUsuario`, `nombre`, `apellido`, `cedula`, `email`, `usuario`, `contrasena`, `rol`, `Brigada_idBrigada`, `Institucion_Educativa_idInstitucion`) VALUES
(343, 'Esteban',   'Márquez Vera',     'V-30400007', 'emarquez343@uel.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 108, NULL),
(344, 'Diana',     'Montiel Rojas',    'V-30400008', 'dmontiel344@uel.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 108, NULL),
(345, 'Rodrigo',   'Cuenca Salas',     'V-30400009', 'rcuenca345@uel.edu.ve',  NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 108, NULL),
(346, 'Lorena',    'Rivas Duque',      'V-30400010', 'lrivas346@uel.edu.ve',   NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 108, NULL),
(347, 'Cristian',  'Polanco Gil',      'V-30400011', 'cpolanco347@uel.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 108, NULL),
(348, 'Rebeca',    'Olivares Paz',     'V-30400012', 'rolivares348@uel.edu.ve',NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 108, NULL);

-- ══════════════════════════════════════════════════════════════
-- 6. ACTIVIDADES — 4 por tipo de brigada (16 actividades)
--    Asignadas al profesor creador de cada brigada
-- ══════════════════════════════════════════════════════════════

-- ── Ecológica (brigadas 101, 102) ──
INSERT INTO `actividad` (`titulo`, `descripcion`, `fecha_inicio`, `fecha_fin`, `estado`, `Brigada_idBrigada`, `Usuario_idUsuarioCreador`) VALUES
('Jornada de Reforestación', 'Siembra de 80 árboles autóctonos (cují, apamate) en el perímetro escolar.', CURDATE() - INTERVAL 10 DAY, CURDATE() - INTERVAL 9 DAY, 'Completada', 101, 202),
('Eco-Auditoría del Agua',   'Medición del consumo de agua por pabellón durante una semana.',             CURDATE() - INTERVAL 3 DAY,  CURDATE(),                    'En Progreso', 101, 202),
('Taller de Compostaje',     'Capacitación sobre compostaje doméstico y escolar.',                        CURDATE() + INTERVAL 2 DAY,  CURDATE() + INTERVAL 2 DAY,   'Pendiente',    102, 203),
('Campaña Cero Plástico',    'Recolección masiva de plástico y charla sobre alternativas sostenibles.',   CURDATE() + INTERVAL 7 DAY,  CURDATE() + INTERVAL 8 DAY,   'Pendiente',    102, 203),

-- ── Gestión de Riesgo (brigadas 103, 104) ──
('Simulacro de Evacuación',      'Simulacro general con cronómetro y evaluación de tiempos de salida.',       CURDATE() - INTERVAL 15 DAY, CURDATE() - INTERVAL 15 DAY, 'Completada',  103, 204),
('Curso de Primeros Auxilios',   'Taller práctico: RCP, vendajes, manejo de fracturas.',                      CURDATE() - INTERVAL 5 DAY,  CURDATE() - INTERVAL 4 DAY,  'Completada',  103, 204),
('Inspección de Extintores',     'Revisión de fechas de vencimiento y ubicación de extintores en la escuela.', CURDATE(),                    CURDATE() + INTERVAL 1 DAY,  'En Progreso', 104, 205),
('Señalización de Rutas de Evacuación', 'Colocación de flechas y carteles de salida de emergencia.',          CURDATE() + INTERVAL 5 DAY,  CURDATE() + INTERVAL 6 DAY,  'Pendiente',   104, 205),

-- ── Patrulla Escolar (brigadas 105, 106) ──
('Operativo Paso Seguro',       'Control de tránsito peatonal en la entrada principal durante horas pico.',   CURDATE() - INTERVAL 7 DAY,  CURDATE() - INTERVAL 7 DAY,  'Completada',  105, 206),
('Charla de Seguridad Vial',    'Presentación sobre señales de tránsito y cruce seguro para primaria.',       CURDATE() - INTERVAL 2 DAY,  CURDATE() - INTERVAL 1 DAY,  'Completada',  105, 206),
('Pintura de Paso de Cebra',    'Renovación de la pintura del paso peatonal frente a la escuela.',            CURDATE() + INTERVAL 3 DAY,  CURDATE() + INTERVAL 3 DAY,  'Pendiente',   106, 207),
('Vigilancia de Salida Escolar','Acompañamiento a los alumnos de preescolar hasta el punto de encuentro.',     CURDATE() + INTERVAL 1 DAY,  CURDATE() + INTERVAL 10 DAY, 'En Progreso', 106, 207),

-- ── Convivencia y Paz (brigadas 107, 108) ──
('Jornada Anti-Bullying',       'Dinámica grupal sobre respeto, empatía y resolución de conflictos.',         CURDATE() - INTERVAL 12 DAY, CURDATE() - INTERVAL 12 DAY, 'Completada',  107, 208),
('Mediación entre Secciones',   'Sesión de mediación para resolver conflicto entre 3ero A y 3ero B.',         CURDATE() - INTERVAL 1 DAY,  CURDATE(),                    'En Progreso', 107, 208),
('Festival de la Amistad',      'Actividad recreativa con juegos cooperativos y mural colectivo.',             CURDATE() + INTERVAL 6 DAY,  CURDATE() + INTERVAL 6 DAY,  'Pendiente',   108, 209),
('Buzón de Convivencia',        'Instalación de un buzón anónimo para reportar situaciones de conflicto.',     CURDATE() + INTERVAL 2 DAY,  CURDATE() + INTERVAL 30 DAY, 'Pendiente',   108, 209);

-- ══════════════════════════════════════════════════════════════
-- 7. INDICADORES AMBIENTALES (para actividades ecológicas)
-- ══════════════════════════════════════════════════════════════
INSERT INTO `indicador_ambiental` (`valor`, `tipo_indicador`, `unidad`, `Actividad_idActividad`) VALUES
(80.0, 'Árboles Plantados',       'uni', (SELECT idActividad FROM actividad WHERE titulo='Jornada de Reforestación' LIMIT 1)),
(12.5, 'Reducción Consumo Agua',  '%',   (SELECT idActividad FROM actividad WHERE titulo='Eco-Auditoría del Agua' LIMIT 1));

-- ══════════════════════════════════════════════════════════════
-- 8. TURNOS — 3 por tipo de brigada (24 turnos)
-- ══════════════════════════════════════════════════════════════
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

INSERT INTO `turno` (`Brigada_idBrigada`, `fecha`, `hora_inicio`, `hora_fin`, `ubicacion`, `notas`, `estado`) VALUES
-- Ecológica
(101, CURDATE() - INTERVAL 5 DAY,  '07:00:00', '09:00:00', 'Jardines del Pabellón A',       'Riego y mantenimiento de jardín',        'Completado'),
(101, CURDATE() + INTERVAL 1 DAY,  '07:30:00', '10:00:00', 'Perímetro escolar zona norte',  'Siembra programada',                     'Programado'),
(102, CURDATE() + INTERVAL 3 DAY,  '14:00:00', '16:00:00', 'Laboratorio de Ciencias',       'Taller de compostaje para 4to año',      'Programado'),

-- Gestión de Riesgo
(103, CURDATE() - INTERVAL 2 DAY,  '08:00:00', '10:00:00', 'Patio Central',                 'Simulacro: evaluación de tiempos',       'Completado'),
(103, CURDATE() + INTERVAL 2 DAY,  '09:00:00', '11:30:00', 'Salón de Usos Múltiples',       'Curso práctico de primeros auxilios',    'Programado'),
(104, CURDATE() + INTERVAL 4 DAY,  '13:00:00', '15:00:00', 'Todos los pabellones',          'Inspección de extintores y señalización','Programado'),

-- Patrulla Escolar
(105, CURDATE() - INTERVAL 1 DAY,  '06:30:00', '07:30:00', 'Entrada principal',             'Operativo de cruce seguro AM',           'Completado'),
(105, CURDATE(),                    '11:30:00', '12:30:00', 'Entrada principal',             'Operativo de cruce seguro PM',           'En Progreso'),
(106, CURDATE() + INTERVAL 2 DAY,  '06:30:00', '07:30:00', 'Calle frente al portón',        'Vigilancia de paso de cebra',            'Programado'),

-- Convivencia y Paz
(107, CURDATE() - INTERVAL 3 DAY,  '10:00:00', '11:30:00', 'Aula 3ero A y B',              'Sesión de mediación',                    'Completado'),
(107, CURDATE() + INTERVAL 1 DAY,  '08:00:00', '09:30:00', 'Cancha techada',               'Dinámica anti-bullying',                 'Programado'),
(108, CURDATE() + INTERVAL 5 DAY,  '14:00:00', '16:00:00', 'Patio Central',                'Festival de la Amistad - preparación',   'Programado');

-- ══════════════════════════════════════════════════════════════
-- 9. REPORTES DE INCIDENTES — 2-3 por tipo (10 reportes)
-- ══════════════════════════════════════════════════════════════
INSERT INTO `reporte_incidente` (`titulo`, `descripcion`, `ubicacion`, `prioridad`, `estado`, `Brigada_idBrigada`, `creado_en`) VALUES
-- Ecológica
('Fuga de agua en baños',            'Grifo roto en baños del Pabellón B. Desperdicio constante de agua.',                              'Baños Pabellón B',              'Media',                          'En Proceso',  101, NOW() - INTERVAL 3 DAY),
('Basura en áreas verdes',           'Acumulación de desechos plásticos en el jardín trasero después del recreo.',                      'Jardín trasero',                'Baja - Situación menor',         'Resuelto',    101, NOW() - INTERVAL 8 DAY),
('Contenedores de reciclaje dañados','Dos contenedores azules fueron vandalizados y ya no cierran correctamente.',                      'Entrada principal',             'Media',                          'En Proceso',  102, NOW() - INTERVAL 2 DAY),

-- Gestión de Riesgo
('Extintores vencidos en Pabellón C','Se detectaron 3 extintores con fecha de vencimiento expirada en el tercer piso.',                 'Pabellón C, Piso 3',           'Alta - Requiere atención inmediata','En Proceso', 103, NOW() - INTERVAL 1 DAY),
('Grieta en pared del comedor',      'Fisura visible de 40cm en la pared norte del comedor. Posible riesgo estructural.',               'Comedor escolar',               'Alta - Requiere atención inmediata','En Proceso', 104, NOW() - INTERVAL 4 DAY),

-- Patrulla Escolar
('Señal de pare caída',              'La señal de PARE frente al portón principal fue derribada por el viento.',                        'Calle frente al portón',        'Alta - Requiere atención inmediata','En Proceso', 105, NOW() - INTERVAL 6 HOUR),
('Conductor imprudente en zona escolar','Un vehículo excedió la velocidad en la zona de cruce escolar a las 7:15 AM.',                  'Paso peatonal entrada',         'Media',                          'Resuelto',    106, NOW() - INTERVAL 2 DAY),

-- Convivencia y Paz
('Altercado entre estudiantes',      'Confrontación verbal entre dos alumnos de 4to año en el pasillo del 2do piso. No hubo agresión física.','Pasillo Piso 2',          'Media',                          'Resuelto',    107, NOW() - INTERVAL 5 DAY),
('Caso de acoso reportado',          'Un alumno reportó ser víctima de burlas repetidas por parte de compañeros de otra sección.',       'Buzón de Convivencia',          'Alta - Requiere atención inmediata','En Proceso', 107, NOW() - INTERVAL 1 DAY),
('Daño a propiedad de estudiante',   'Mochila de un alumno de 2do año fue escondida y dañada intencionalmente durante el recreo.',       'Aula 2do B',                   'Media',                          'En Proceso',  108, NOW() - INTERVAL 3 DAY);

-- ══════════════════════════════════════════════════════════════
-- 10. REPORTES DE ACTIVIDADES (vinculados a actividades completadas)
-- ══════════════════════════════════════════════════════════════
INSERT INTO `reporte_actividad` (`resumen`, `resultado`, `Actividad_idActividad`, `Usuario_idUsuario`, `fecha_reporte`) VALUES
('Se plantaron 80 árboles con apoyo de padres y representantes. Participaron 12 brigadistas.', 'Exitoso - 80 árboles plantados',
  (SELECT idActividad FROM actividad WHERE titulo='Jornada de Reforestación' LIMIT 1), 202, NOW() - INTERVAL 9 DAY),

('El simulacro se ejecutó en 4 minutos 30 segundos. Se identificaron 2 cuellos de botella en los pasillos.', 'Completado con observaciones',
  (SELECT idActividad FROM actividad WHERE titulo='Simulacro de Evacuación' LIMIT 1), 204, NOW() - INTERVAL 14 DAY),

('Se capacitaron 18 brigadistas en RCP y vendajes. Evaluación práctica aprobada por todos.', 'Exitoso',
  (SELECT idActividad FROM actividad WHERE titulo='Curso de Primeros Auxilios' LIMIT 1), 204, NOW() - INTERVAL 4 DAY),

('Operativo matutino: 120 alumnos cruzaron de forma segura. Sin incidentes.', 'Exitoso - Sin incidentes',
  (SELECT idActividad FROM actividad WHERE titulo='Operativo Paso Seguro' LIMIT 1), 206, NOW() - INTERVAL 6 DAY),

('Se presentaron señales de tránsito a 60 alumnos de primaria con juego interactivo.', 'Exitoso - Alta participación',
  (SELECT idActividad FROM actividad WHERE titulo='Charla de Seguridad Vial' LIMIT 1), 206, NOW() - INTERVAL 1 DAY),

('Dinámica con 35 alumnos. Se identificaron 3 casos que requieren seguimiento con orientación.', 'Completado con seguimiento requerido',
  (SELECT idActividad FROM actividad WHERE titulo='Jornada Anti-Bullying' LIMIT 1), 208, NOW() - INTERVAL 11 DAY);

-- ══════════════════════════════════════════════════════════════
-- 11. REPORTES DE IMPACTO (vinculados a actividades completadas)
-- ══════════════════════════════════════════════════════════════
INSERT INTO `reporte_de_impacto` (`contenido`, `fecha_generacion`, `Actividad_idActividad`, `Usuario_idUsuario`) VALUES
('La reforestación incrementará la absorción de CO2 en aproximadamente 1.8 toneladas anuales. Se espera reducción de temperatura local de 1-2°C en la zona escolar dentro de 3 años.',
  NOW() - INTERVAL 8 DAY, (SELECT idActividad FROM actividad WHERE titulo='Jornada de Reforestación' LIMIT 1), 202),

('El simulacro reveló que el tiempo de evacuación es 30% mayor al recomendado. Se propone ensanchar la salida del Pabellón B y agregar señalización luminosa.',
  NOW() - INTERVAL 13 DAY, (SELECT idActividad FROM actividad WHERE titulo='Simulacro de Evacuación' LIMIT 1), 204),

('El operativo redujo los cruces peligrosos de alumnos en un 85% comparado con días sin patrullaje.',
  NOW() - INTERVAL 5 DAY, (SELECT idActividad FROM actividad WHERE titulo='Operativo Paso Seguro' LIMIT 1), 206),

('La jornada redujo los reportes de conflicto entre las secciones 3ero A y B en un 60% durante la semana siguiente.',
  NOW() - INTERVAL 10 DAY, (SELECT idActividad FROM actividad WHERE titulo='Jornada Anti-Bullying' LIMIT 1), 208);

-- ══════════════════════════════════════════════════════════════
-- 12. CONFIGURACIÓN
-- ══════════════════════════════════════════════════════════════
INSERT INTO `configuracion` (`clave`, `valor`) VALUES
('mensaje_dia', '¡Bienvenidos al SBE! Recuerda: cada acción cuenta para una escuela más segura y armónica.')
ON DUPLICATE KEY UPDATE `valor` = VALUES(`valor`);

-- ══════════════════════════════════════════════════════════════
-- 13. AJUSTAR AUTO_INCREMENT
-- ══════════════════════════════════════════════════════════════
ALTER TABLE `brigada`  AUTO_INCREMENT = 200;
ALTER TABLE `usuario`  AUTO_INCREMENT = 400;
