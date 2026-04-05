-- Migración para permitir que el profesor creador pueda completar actividades
-- Ejecutar una sola vez sobre la base de datos existente.

ALTER TABLE actividad
    ADD COLUMN Usuario_idUsuarioCreador INT NULL AFTER Brigada_idBrigada;

ALTER TABLE actividad
    ADD CONSTRAINT fk_actividad_usuario_creador
    FOREIGN KEY (Usuario_idUsuarioCreador)
    REFERENCES Usuario(idUsuario)
    ON DELETE SET NULL
    ON UPDATE NO ACTION;

CREATE INDEX idx_actividad_creador ON actividad(Usuario_idUsuarioCreador);
