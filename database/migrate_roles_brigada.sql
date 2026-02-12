-- Migración: agregar profesor_id a Brigada y subjefe_id
-- Ejecutar en phpMyAdmin o línea de comandos MySQL

USE db_brigadas_maracaibo;

-- 1. Agregar columna profesor_id a Brigada (quién la creó/administra)
ALTER TABLE Brigada ADD COLUMN profesor_id INT NULL AFTER Institucion_Educativa_idInstitucion;

-- 2. Agregar columna subjefe_id a Brigada (brigadista designado como subjefe)
ALTER TABLE Brigada ADD COLUMN subjefe_id INT NULL AFTER profesor_id;

-- 3. Índices para las nuevas columnas
ALTER TABLE Brigada ADD INDEX idx_brigada_profesor (profesor_id);
ALTER TABLE Brigada ADD INDEX idx_brigada_subjefe (subjefe_id);

-- Nota: No agregamos FK formales porque profesor_id y subjefe_id son idUsuario
-- y puede que aún no existan usuarios al momento de crear la brigada.

-- 4. Agregar columna usuario (nombre de usuario para login) en Usuario. Único en todo el sistema.
ALTER TABLE Usuario ADD COLUMN usuario VARCHAR(45) NULL AFTER email;
CREATE UNIQUE INDEX idx_usuario_unique ON Usuario (usuario);

-- 5. Logo de institución (ruta del archivo subido)
ALTER TABLE Institucion_Educativa ADD COLUMN logo_ruta VARCHAR(255) NULL AFTER telefono;

-- Roles válidos para el sistema:
-- 'Directivo'      - Director, admin total, no puede ser parte de brigada
-- 'Coordinador'    - Admin, puede ver todo, no puede ser parte de brigada
-- 'Profesor'       - Crea brigadas, ve sus brigadas y las de otros profesores
-- 'Brigadista Jefe'- Jefe de brigada (visible en listado de brigadistas)
-- 'Subjefe'        - Alumno designado (solo visible en detalle de brigada)
-- 'Brigadista'     - Alumno normal (visible en listado de brigadistas)
