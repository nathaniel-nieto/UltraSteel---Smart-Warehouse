CREATE DATABASE IF NOT EXISTS ultrasteeldata;
USE ultrasteeldata;

CREATE TABLE almacen (
  id varchar(20) NOT NULL,
  tipo int DEFAULT NULL,
  operador varchar(50) DEFAULT NULL,
  fecha date DEFAULT NULL,
  hora time DEFAULT NULL,
  turno enum('Matutino','Vespertino','Nocturno') DEFAULT NULL,
  estatus varchar(50) DEFAULT 'En almacén',
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
