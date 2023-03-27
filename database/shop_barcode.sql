-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Máy chủ: localhost
-- Thời gian đã tạo: Th5 19, 2021 lúc 09:57 AM
-- Phiên bản máy phục vụ: 10.4.14-MariaDB
-- Phiên bản PHP: 7.4.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `shop_barcode`
--

-- --------------------------------------------------------

--
--
-- Cấu trúc bảng cho bảng `bill_product`
--

CREATE TABLE `bill_product` (
  `bill_id` varchar(100) NOT NULL,
  `product_id` varchar(50) NOT NULL,
  `quantity` int(11) NOT NULL,
  `discount` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
