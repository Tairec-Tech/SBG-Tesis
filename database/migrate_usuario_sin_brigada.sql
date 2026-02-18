-- Permitir usuarios sin brigada (Directivo/Coordinador/Profesor al registrarse).
-- Ejecutar una vez en MySQL.

USE db_brigadas_maracaibo;

-- 1. Permitir Brigada_idBrigada NULL
ALTER TABLE Usuario MODIFY COLUMN Brigada_idBrigada INT NULL;

-- 2. Vincular usuario a institución directamente (para quienes no tienen brigada)
ALTER TABLE Usuario ADD COLUMN Institucion_Educativa_idInstitucion INT NULL AFTER Brigada_idBrigada;
ALTER TABLE Usuario ADD INDEX idx_usuario_institucion (Institucion_Educativa_idInstitucion);
