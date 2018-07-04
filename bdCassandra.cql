CREATE  KEYSPACE IF NOT EXISTS bdUser WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
USE bdUser;
CREATE TABLE IF NOT EXISTS usuario (
	id_usuario int,
    nombre_usuario text,
    contra text,
    nombre text,
    apellido text,
    fecha text,
    PRIMARY KEY (id_usuario)
 );
INSERT INTO usuario (id_usuario, nombre_usuario, contra, nombre, apellido, fecha) VALUES (1,'ale','123', 'Alejo', 'Hernandez', '7/2/2018');
INSERT INTO usuario (id_usuario, nombre_usuario, contra, nombre, apellido, fecha) VALUES (2,'aylin','123', 'Aylin', 'Aroche','7/2/2018');
INSERT INTO usuario (id_usuario, nombre_usuario, contra, nombre, apellido, fecha) VALUES (3,'luigi','123', 'Miguel', 'Catalan', '7/2/2018');x