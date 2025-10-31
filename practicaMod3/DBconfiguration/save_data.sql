-- Insertar usuarios
INSERT INTO usuarios (nombre, correo, telefono, fecha_nacimiento) VALUES
('Juan Pérez', 'juan.perez@example.com', '777-111-2233', '1990-03-15'),
('María López', 'maria.lopez@example.com', '777-444-5566', '1992-08-21'),
('Carlos Ruiz', 'carlos.ruiz@example.com', '777-777-8899', '1988-12-05');

-- Insertar credenciales
INSERT INTO credenciales (id_usuario, username, password_hash) VALUES
(1, 'juan.perez1', 'hash_juan_perez'),
(2, 'maria.lopez2', 'hash_maria_lopez'),
(3, 'carlos.ruiz3', 'hash_carlos_ruiz');