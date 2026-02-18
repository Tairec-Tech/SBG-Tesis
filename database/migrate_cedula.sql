-- Agregar cédula a Usuario (para todos los roles). Los alumnos solo se registran desde Brigadistas.
-- Ejecutar en MySQL.

USE db_brigadas_maracaibo;

ALTER TABLE Usuario ADD COLUMN cedula VARCHAR(30) NULL AFTER apellido;
CREATE INDEX idx_usuario_cedula ON Usuario (cedula);
