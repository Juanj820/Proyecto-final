-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 15-05-2025 a las 17:12:53
-- Versión del servidor: 8.0.30
-- Versión de PHP: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- Creación de la base de datos
CREATE DATABASE IF NOT EXISTS `clinica` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `clinica`;

-- ---------------------------------------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int NOT NULL,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `usuario` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `foto` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `rol` enum('admin','doctor','recepcionita') COLLATE utf8mb4_unicode_ci NOT NULL,
  `creado_en` datetime DEFAULT  CURRENT_TIMESTAMP,
  `actualizado_en` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios`(`id`, `nombre`, `usuario`, `password`, `foto`, `rol`, `creado_en`, `actualizado_en`) VALUES
(1, 'Administrador', 'admin', 'admin', 'assets/images/perfiles/user_1.jpg', 'admin', '2025-05-08 17:23:11', '2025-05-14 10:17:12'),
(2, 'Dr. Juan Pérez', 'jperez', '1234', 'assets/images/perfiles/user_2.jpg', 'doctor', '2025-05-08 17:23:11', '2025-05-14 19:47:43'),
(3, 'Dra. Ana López', 'alopez', '1234', NULL, 'doctor', '2025-05-08 17:23:11', '2025-05-08 17:23:11'),
(4, 'Recepcionista 1', 'recep1', '1234', NULL, 'recepcionista', '2025-05-08 17:23:11', '2025-05-08 17:23:11'),
(5, 'Recepcionista 2', 'recep2', '1234', NULL, 'recepcionista', '2025-05-08 17:23:11', '2025-05-08 17:23:11'),
(6, 'Dr. Carlos Ruiz', 'cruiz', '1234', NULL, 'doctor', '2025-05-08 17:23:11', '2025-05-08 17:23:11'),
(7, 'Dra. Marta Diaz', 'mdiaz', '1234', NULL, 'doctor', '2025-05-08 17:23:11', '2025-05-08 17:23:11'),
(8, 'Dr. Luis Gómez', 'lgomez', '1234', NULL, 'doctor', '2025-05-08 17:23:11', '2025-05-08 17:23:11'),
(9, 'Dra. Paula Torres', 'ptorres', '1234', NULL, 'doctor', '2025-05-08 17:23:11', '2025-05-08 17:23:11'),
(10, 'Dr. Sergio Ramírez', 'sramirez', '1234', NULL, 'doctor', '2025-05-08 17:23:11', '2025-05-08 17:23:11');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `doctores `
--

CREATE TABLE `doctores` (
  `id` int NOT NULL,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `departamento` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `telefono` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `estado` enum('Permanente','En Espera') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `creado_por` int DEFAULT NULL,
  `creado_en` datetime DEFAULT CURRENT_TIMESTAMP,
  `actualizado_en` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `doctores `
--

INSERT INTO doctores (`id`,`nombre`,`departamento`,`telefono`,`estado`,`creado_por`,`creado_en`,`actualizado_en`) VALUES
(1, 'Juan Pérez','Cardiología','3021111111','Permanente', 1,'2025-05-08 17:23:11','2025-05-08 17:23:11'),
(2, 'Ana López','Neurología','3002222224','En Espera', 1,'2025-05-08 17:23:11','2025-05-08 18:47:41'),
(3, 'Carlos Ruiz','Dermatología','3003333333','Permanente', 1,'2025-05-08 17:23:11','2025-05-08 17:23:11'),
(4, 'Marta Diaz','Neurología','3004444444','Permanente', 1,'2025-05-08 17:23:11','2025-05-08 17:23:11'),
(5, 'Luis Olmos','Ginecología','3005555555','En Espera', 1,'2025-05-08 17:23:11','2025-05-08 17:43:50'),
(6, 'Paula Torres','Oftalmología','3606666666','Permanente', 1,'2025-05-08 17:23:11','2025-05-08 17:23:11'),
(7, 'Sergio Ramirez','Traumatología','3007777777','Permanente', 1,'2025-05-08 17:23:11','2025-05-08 17:23:11'),
(8, 'Laura Méndez','Oncología','3008888888','En Espera', 1,'2025-05-08 17:23:11','2025-05-08 17:23:11'),
(9, 'Pedro Castillo','Urología','3020211234','Permanente', 1,'2025-05-08 17:23:11','2025-05-08 17:55:28'),
(10, 'Sofía Herrera','Psiquiatría','3101000000','Permanente', 1,'2025-05-08 17:23:11','2025-05-08 17:23:11'),
(11, 'Samuel Vega','Ginecología','3008990883','Permanente', 1,'2025-05-08 17:38:45','2025-05-08 17:38:45'),
(12, 'Valentina Vega','Pediatría','3005660877','Permanente', 1,'2025-05-08 17:49:56','2025-05-08 17:49:56'),
(13, 'Sara Zeya','Traumatología','3231329083','En Espera', 1,'2025-05-08 17:57:27','2025-05-08 17:57:27'),
(15, 'Andrea Fuentes','Ginecología','3157022187','Permanente', 1,'2025-05-14 19:24:11','2025-05-14 19:26:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pacientes`
--

CREATE TABLE `pacientes` (
  `id` int NOT NULL,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sintomas` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `telefono` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `direccion` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `estado` enum('Admitido','En Espera') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `creado_por` int DEFAULT NULL,
  `creado_en` datetime DEFAULT CURRENT_TIMESTAMP,
  `actualizado_en` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `pacientes`
--

INSERT INTO `pacientes`(`id`, `nombre`, `sintomas`, `telefono`, `direccion`, `estado`, `creado_por`, `creado_en`, `actualizado_en`) VALUES
(1, 'Maria García', 'dolor de cabeza', '3101111111', 'Calle 1 #10-20', 'Admitido', 1, '2025-05-08 17:23:11', '2025-05-08 17:23:11'),
(2, 'José Martínez', 'Dolor abdominal', '3102222222', 'Calle 2 #20-30', 'En Espera', 1, '2025-05-08 17:23:11', '2025-05-08 20:17:32'),
(3, 'Lucía Fernández', 'tos', '3103333333', 'Calle 3 #30-40', 'Admitido', 1, '2025-05-08 17:23:11', '2025-05-08 17:23:11'),
(4, 'Carlos Torres', 'mareo', '3104444444', 'Calle 4 #40-50', 'Admitido', 1, '2025-05-08 17:23:11', '2025-05-08 17:23:11'),
(5, 'Elena Ramírez', 'dolor abdominal', '3105555555', 'Calle 5 #50-60', 'En Espera', 1, '2025-05-08 17:23:11', '2025-05-08 17:23:11'),
(6, 'Miguel Castro', 'vómito', '3106666666', 'Calle 6 #60-70', 'Admitido', 1, '2025-05-08 17:23:11', '2025-05-08 17:23:11'),
(7, 'Patricia López', 'alergia', '3107777777', 'Calle 7 #70-80', 'En Espera', 1, '2025-05-08 17:23:11', '2025-05-08 17:23:11'),
(8, 'Andrés Gómez', 'fractura', '3108888888', 'Calle 8 #80-90', 'Admitido', 1, '2025-05-08 17:23:11', '2025-05-08 17:23:11'),
(9, 'Sandra Díaz', 'dolor muscular', '3109999999', 'Calle 9 #90-100', 'Admitido', 1, '2025-05-08 17:23:11', '2025-05-08 17:23:11'),
(10, 'Raúl Herrera', 'insomnio', '3110000000', 'Calle 10 #100-110', 'En Espera', 1, '2025-05-08 17:23:11', '2025-05-08 17:23:11'),
(11, 'Rigoberto Saldoval', 'Fractura', '6052890067', 'Calle 23 # 22-11', 'Admitido', 1, '2025-05-08 20:18:19', '2025-05-08 20:18:19'),
(12, 'Ancelmo Rodriguez', 'Dolor abdominal', '6052745680', 'Cra 11b #12-06', 'Admitido', 1, '2025-05-13 10:32:23', '2025-05-13 10:32:23');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `citas`
--

CREATE TABLE `citas` (
  `id` int NOT NULL,
  `doctor_id` int DEFAULT NULL,
  `id_paciente` int DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  `estado` enum('Programada','En Consulta','Finalizada','Cancelada','No Asistio','Aprobada','Pendiente') CHARACTER SET utf8mb4 COLLATE unicode_ci DEFAULT NULL,
  `creado_por` int DEFAULT NULL,
  `creado_en` datetime DEFAULT CURRENT_TIMESTAMP,
  `actualizado_en` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `citas`
--

INSERT INTO `citas`(`id`, `id_doctor`, `id_paciente`, `fecha`, `estado`, `creado_por`, `creado_en`, `actualizado_en`) VALUES
(1, 1, 1, '2024-05-10 09:00:00', 'Aprobada', 1, '2025-05-08 17:23:11', '2025-05-08 17:23:11'),
(2, 2, 2, '2024-05-11 10:00:00', 'Pendiente', 1, '2025-05-08 17:23:11', '2025-05-08 17:23:11'),
(3, 3, 3, '2024-05-12 11:00:00', 'Aprobada', 1, '2025-05-08 17:23:11', '2025-05-08 17:23:11'),
(4, 4, 4, '2024-05-13 12:00:00', 'Aprobada', 1, '2025-05-08 17:23:11', '2025-05-08 17:23:11'),
(5, 5, 5, '2024-05-14 13:00:00', 'Pendiente', 1, '2025-05-08 17:23:11', '2025-05-08 17:23:11'),
(6, 6, 6, '2024-05-15 15:00:00', 'Aprobada', 1, '2025-05-08 17:23:11', '2025-05-08 17:23:11'),
(7, 7, 7, '2024-05-16 15:00:00', 'Aprobada', 1, '2025-05-08 17:23:11', '2025-05-08 17:23:11'),
(8, 8, 8, '2024-05-17 16:00:00', 'Pendiente', 1, '2025-05-08 17:23:11', '2025-05-08 17:23:11'),
(9, 9, 9, '2024-05-18 17:00:00', 'Aprobada', 1, '2025-05-08 17:23:11', '2025-05-08 17:23:11'),
(10, 10, 10, '2024-05-20 10:00:00', 'Aprobada', 1, '2025-05-08 17:23:11', '2025-05-08 17:23:11'),
(11, 5, 6, '2025-05-08 08:15:00', 'Programada', 1, '2025-05-08 21:58:48', '2025-05-08 21:58:48'),
(12, 5, 2, '2025-05-08 08:15:00', 'Aprobada', 1, '2025-05-10 22:29:55', '2025-05-10 22:29:55'),
(13, 12, 12, '2025-05-13 11:00:00', 'En Consulta', 1, '2025-05-13 10:33:06', '2025-05-13 10:33:35'),
(14, 15, 9, '2024-05-15 07:00:00', 'Cancelada', 1, '2025-05-14 19:32:19', '2025-05-14 19:33:56');

--
-- Indices para tablas volcadas
--

--
-- Indices para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `usuario` (`usuario`);

--
-- Indices para la tabla `doctores `
--
ALTER TABLE `doctores `
  ADD PRIMARY KEY (`id`),
  ADD KEY `creado_por` (`creado_por`);

--
-- Indices de la tabla `pacientes`
--
ALTER TABLE `pacientes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `creado_por` (`creado_por`);

  --
  -- Indices de la tabla `citas`
  --
ALTER TABLE `citas`
    ADD PRIMARY KEY (`id`),
    ADD KEY `doctor_id` (`doctor_id`),
    ADD KEY `id_paciente` (`id_paciente`),
    ADD KEY `creado_por` (`creado_por`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `doctores `
--
ALTER TABLE `doctores `
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `pacientes`
--
ALTER TABLE `pacientes`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `citas`
--
ALTER TABLE `citas`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- Restricciones para las tablas volcadas
--

--
-- Filtros para la tabla `doctores `
--
ALTER TABLE `doctores `
  ADD CONSTRAINT `doctores_ibfk_1` FOREIGN KEY (`creado_por`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `pacientes`
--
ALTER TABLE `pacientes`
  ADD CONSTRAINT `pacientes_ibfk_1` FOREIGN KEY (`creado_por`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `citas`
--
ALTER TABLE `citas`
  ADD CONSTRAINT `citas_ibfk_1` FOREIGN KEY (`id_doctor`) REFERENCES `doctores` (`id`),
  ADD CONSTRAINT `citas_ibfk_2` FOREIGN KEY (`id_paciente`) REFERENCES `pacientes` (`id`),
  ADD CONSTRAINT `citas_ibfk_3` FOREIGN KEY (`creado_por`) REFERENCES `usuarios` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;