-- Añade columnas del formulario "Nueva Brigada" a la tabla Brigada.
-- Ejecutar una vez: mysql -u usuario -p db_brigadas_maracaibo < database/migrate_brigada_campos.sql

USE db_brigadas_maracaibo;

ALTER TABLE Brigada ADD COLUMN descripcion TEXT NULL AFTER area_accion;
ALTER TABLE Brigada ADD COLUMN coordinador VARCHAR(100) NULL AFTER descripcion;
ALTER TABLE Brigada ADD COLUMN color_identificador VARCHAR(20) NULL DEFAULT '#2563eb' AFTER coordinador;
