-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 30, 2022 at 08:09 PM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `forecast`
--

-- --------------------------------------------------------

--
-- Table structure for table `tb_admin`
--

CREATE TABLE `tb_admin` (
  `admin_id` int(5) NOT NULL,
  `username` varchar(10) NOT NULL,
  `password` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tb_admin`
--

INSERT INTO `tb_admin` (`admin_id`, `username`, `password`) VALUES
(1, 'admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `tb_arima`
--

CREATE TABLE `tb_arima` (
  `arima_id` int(5) NOT NULL,
  `emt_id` int(5) NOT NULL,
  `uploads_id` int(5) NOT NULL,
  `p` int(2) NOT NULL,
  `d` int(2) NOT NULL,
  `q` int(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tb_arima`
--

INSERT INTO `tb_arima` (`arima_id`, `emt_id`, `uploads_id`, `p`, `d`, `q`) VALUES
(1, 1, 1, 0, 1, 0),
(2, 2, 4, 1, 0, 0),
(3, 4, 7, 0, 1, 0),
(4, 3, 5, 0, 1, 1),
(5, 5, 6, 0, 1, 0);

-- --------------------------------------------------------

--
-- Table structure for table `tb_emiten`
--

CREATE TABLE `tb_emiten` (
  `emt_id` int(5) NOT NULL,
  `emt_code` varchar(4) NOT NULL,
  `emt_name` varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tb_emiten`
--

INSERT INTO `tb_emiten` (`emt_id`, `emt_code`, `emt_name`) VALUES
(1, 'ADRO', 'Adaro Energy Indonesia Tbk'),
(2, 'ANTM', 'Aneka Tambang Tbk'),
(3, 'BBCA', 'Bank Central Asia Tbk'),
(4, 'ASII', 'Astra International Tbk'),
(5, 'BBNI', 'Bank Negara Indonesia Tbk');

-- --------------------------------------------------------

--
-- Table structure for table `tb_uploads`
--

CREATE TABLE `tb_uploads` (
  `uploads_id` int(5) NOT NULL,
  `emt_id` int(5) NOT NULL,
  `filename` varchar(20) NOT NULL,
  `path` varchar(100) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tb_uploads`
--

INSERT INTO `tb_uploads` (`uploads_id`, `emt_id`, `filename`, `path`, `timestamp`) VALUES
(1, 1, 'ADRO.csv', '/home/forestock/mysite/uploads/ADRO.csv', '2022-08-16 19:11:32'),
(4, 2, 'ANTM.csv', '/home/forestock/mysite/uploads/ANTM.csv', '2022-08-19 13:54:34'),
(5, 3, 'BBCA.csv', '/home/forestock/mysite/uploads/BBCA.csv', '2022-08-19 13:54:43'),
(6, 5, 'BBNI.csv', '/home/forestock/mysite/uploads/BBNI.csv', '2022-08-19 13:54:51'),
(7, 4, 'ASII.csv', '/home/forestock/mysite/uploads/ASII.csv', '2022-08-19 13:56:12');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tb_admin`
--
ALTER TABLE `tb_admin`
  ADD PRIMARY KEY (`admin_id`);

--
-- Indexes for table `tb_arima`
--
ALTER TABLE `tb_arima`
  ADD PRIMARY KEY (`arima_id`);

--
-- Indexes for table `tb_emiten`
--
ALTER TABLE `tb_emiten`
  ADD PRIMARY KEY (`emt_id`);

--
-- Indexes for table `tb_uploads`
--
ALTER TABLE `tb_uploads`
  ADD PRIMARY KEY (`uploads_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tb_admin`
--
ALTER TABLE `tb_admin`
  MODIFY `admin_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `tb_arima`
--
ALTER TABLE `tb_arima`
  MODIFY `arima_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `tb_emiten`
--
ALTER TABLE `tb_emiten`
  MODIFY `emt_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `tb_uploads`
--
ALTER TABLE `tb_uploads`
  MODIFY `uploads_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
