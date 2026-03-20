-- Seed: 1 Directivo, 3 Profesores, 10 Alumnos por profesor (30 alumnos).
-- Ejecutar después de db_brigadas_maracaibo.sql (o en una BD ya creada).
-- Contraseñas: director -> director123; profesores -> profesor1, profesor2, profesor3; alumnos -> alumno123

USE db_brigadas_maracaibo;

-- ========== INSTITUCIÓN (necesaria para FK de brigada y usuario) ==========
-- Si la BD está vacía, crear al menos una institución para que exista idInstitucion = 1
INSERT INTO `institucion_educativa` (`idInstitucion`, `nombre_institucion`, `direccion`, `telefono`, `logo_ruta`) VALUES
(1, 'Urbe', 'Maracaibo', '04247313983', NULL)
ON DUPLICATE KEY UPDATE `nombre_institucion` = VALUES(`nombre_institucion`);

-- ========== BRIGADAS para los 3 profesores (institución 1 = Urbe) ==========
INSERT INTO `brigada` (`idBrigada`, `nombre_brigada`, `area_accion`, `descripcion`, `coordinador`, `color_identificador`, `fecha_creacion`, `Institucion_Educativa_idInstitucion`, `profesor_id`, `subjefe_id`) VALUES
(7, 'Brigada Verde', 'Ambiental', 'Brigada del Prof. Martínez', NULL, '#059669', NOW(), 1, NULL, NULL),
(8, 'Brigada Eco', 'Reciclaje', 'Brigada del Prof. Rodríguez', NULL, '#047857', NOW(), 1, NULL, NULL),
(9, 'Brigada Tierra', 'Conservación', 'Brigada del Prof. García', NULL, '#10b981', NOW(), 1, NULL, NULL);

-- ========== 1 DIRECTIVO ==========
-- Usuario: director | Contraseña: director123
INSERT INTO `usuario` (`idUsuario`, `nombre`, `apellido`, `cedula`, `email`, `usuario`, `contrasena`, `rol`, `Brigada_idBrigada`, `Institucion_Educativa_idInstitucion`) VALUES
(5, 'Ricardo', 'Mendoza', 'V-12345678', 'director@urbe.edu.ve', 'director', '9e4d7bba246abe731743986c4dc50897b68b1d0249a066abb3530fcbaa33dab3', 'Directivo', NULL, 1);

-- ========== 3 PROFESORES (cada uno con su brigada) ==========
-- profesor1 | profesor1 | Prof. Martínez -> brigada 7
-- profesor2 | profesor2 | Prof. Rodríguez -> brigada 8
-- profesor3 | profesor3 | Prof. García -> brigada 9
INSERT INTO `usuario` (`idUsuario`, `nombre`, `apellido`, `cedula`, `email`, `usuario`, `contrasena`, `rol`, `Brigada_idBrigada`, `Institucion_Educativa_idInstitucion`) VALUES
(6, 'Carlos', 'Martínez', 'V-11111111', 'prof1@urbe.edu.ve', 'profesor1', 'c5feadda95f15c08186641ec217bfde3ac211298f1912798610ef6532c7ffe1f', 'Profesor', 7, 1),
(7, 'Ana', 'Rodríguez', 'V-22222222', 'prof2@urbe.edu.ve', 'profesor2', 'c59036fb2b020cac117abc9e4647f54bac565eddbb5aa209f9e78e5269e0ec42', 'Profesor', 8, 1),
(8, 'Luis', 'García', 'V-33333333', 'prof3@urbe.edu.ve', 'profesor3', 'fa2eef54e73154938645d3b4d6207acf5b602188f4ae96ffb0863ac5fa2ad236', 'Profesor', 9, 1);

-- Actualizar brigada con profesor_id
UPDATE `brigada` SET `profesor_id` = 6 WHERE `idBrigada` = 7;
UPDATE `brigada` SET `profesor_id` = 7 WHERE `idBrigada` = 8;
UPDATE `brigada` SET `profesor_id` = 8 WHERE `idBrigada` = 9;

-- ========== 10 ALUMNOS por profesor (contraseña: alumno123) ==========
-- Brigada 7 (Prof. Martínez)
INSERT INTO `usuario` (`idUsuario`, `nombre`, `apellido`, `cedula`, `email`, `usuario`, `contrasena`, `rol`, `Brigada_idBrigada`, `Institucion_Educativa_idInstitucion`) VALUES
(9, 'Alumno', 'Uno B7', 'V-20100001', 'a1b7@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 7, NULL),
(10, 'Alumno', 'Dos B7', 'V-20100002', 'a2b7@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 7, NULL),
(11, 'Alumno', 'Tres B7', 'V-20100003', 'a3b7@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 7, NULL),
(12, 'Alumno', 'Cuatro B7', 'V-20100004', 'a4b7@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 7, NULL),
(13, 'Alumno', 'Cinco B7', 'V-20100005', 'a5b7@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 7, NULL),
(14, 'Alumno', 'Seis B7', 'V-20100006', 'a6b7@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 7, NULL),
(15, 'Alumno', 'Siete B7', 'V-20100007', 'a7b7@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 7, NULL),
(16, 'Alumno', 'Ocho B7', 'V-20100008', 'a8b7@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 7, NULL),
(17, 'Alumno', 'Nueve B7', 'V-20100009', 'a9b7@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 7, NULL),
(18, 'Alumno', 'Diez B7', 'V-20100010', 'a10b7@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 7, NULL);

-- Brigada 8 (Prof. Rodríguez)
INSERT INTO `usuario` (`idUsuario`, `nombre`, `apellido`, `cedula`, `email`, `usuario`, `contrasena`, `rol`, `Brigada_idBrigada`, `Institucion_Educativa_idInstitucion`) VALUES
(19, 'Alumno', 'Uno B8', 'V-20200001', 'a1b8@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 8, NULL),
(20, 'Alumno', 'Dos B8', 'V-20200002', 'a2b8@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 8, NULL),
(21, 'Alumno', 'Tres B8', 'V-20200003', 'a3b8@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 8, NULL),
(22, 'Alumno', 'Cuatro B8', 'V-20200004', 'a4b8@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 8, NULL),
(23, 'Alumno', 'Cinco B8', 'V-20200005', 'a5b8@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 8, NULL),
(24, 'Alumno', 'Seis B8', 'V-20200006', 'a6b8@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 8, NULL),
(25, 'Alumno', 'Siete B8', 'V-20200007', 'a7b8@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 8, NULL),
(26, 'Alumno', 'Ocho B8', 'V-20200008', 'a8b8@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 8, NULL),
(27, 'Alumno', 'Nueve B8', 'V-20200009', 'a9b8@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 8, NULL),
(28, 'Alumno', 'Diez B8', 'V-20200010', 'a10b8@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 8, NULL);

-- Brigada 9 (Prof. García)
INSERT INTO `usuario` (`idUsuario`, `nombre`, `apellido`, `cedula`, `email`, `usuario`, `contrasena`, `rol`, `Brigada_idBrigada`, `Institucion_Educativa_idInstitucion`) VALUES
(29, 'Alumno', 'Uno B9', 'V-20300001', 'a1b9@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 9, NULL),
(30, 'Alumno', 'Dos B9', 'V-20300002', 'a2b9@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 9, NULL),
(31, 'Alumno', 'Tres B9', 'V-20300003', 'a3b9@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 9, NULL),
(32, 'Alumno', 'Cuatro B9', 'V-20300004', 'a4b9@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 9, NULL),
(33, 'Alumno', 'Cinco B9', 'V-20300005', 'a5b9@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 9, NULL),
(34, 'Alumno', 'Seis B9', 'V-20300006', 'a6b9@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 9, NULL),
(35, 'Alumno', 'Siete B9', 'V-20300007', 'a7b9@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 9, NULL),
(36, 'Alumno', 'Ocho B9', 'V-20300008', 'a8b9@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 9, NULL),
(37, 'Alumno', 'Nueve B9', 'V-20300009', 'a9b9@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 9, NULL),
(38, 'Alumno', 'Diez B9', 'V-20300010', 'a10b9@urbe.edu.ve', NULL, 'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0', 'Brigadista', 9, NULL);

-- Actualizar AUTO_INCREMENT para que no choque con futuros inserts
ALTER TABLE `brigada` AUTO_INCREMENT = 10;
ALTER TABLE `usuario` AUTO_INCREMENT = 39;
