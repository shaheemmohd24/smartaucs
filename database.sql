-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: sql.freedb.tech
-- Generation Time: Dec 06, 2023 at 08:11 PM
-- Server version: 8.0.35-0ubuntu0.22.04.1
-- PHP Version: 8.2.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `freedb_AUCTION`
--

-- --------------------------------------------------------

--
-- Table structure for table `auction`
--

CREATE TABLE `auction` (
  `id` int NOT NULL,
  `product_id` int NOT NULL,
  `auction_start_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `auction_end_time` datetime DEFAULT NULL,
  `winner_id` int DEFAULT NULL,
  `final_bid_amount` decimal(10,2) DEFAULT NULL,
  `product_name` varchar(255) DEFAULT NULL,
  `base_price` decimal(10,2) DEFAULT NULL,
  `moneydistributed` enum('yes','no') NOT NULL DEFAULT 'no',
  `category_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `auction`
--

INSERT INTO `auction` (`id`, `product_id`, `auction_start_time`, `auction_end_time`, `winner_id`, `final_bid_amount`, `product_name`, `base_price`, `moneydistributed`, `category_id`) VALUES
(15, 11, '2023-12-06 17:26:35', '2023-12-15 00:00:00', 25, 140700.11, 'HONDA CIVIC', 140000.00, 'yes', 8),
(16, 12, '2023-12-06 17:29:34', '2023-12-07 00:00:00', NULL, NULL, 'MARUTI SWIFT', 86000.00, 'no', 8),
(17, 15, '2023-12-06 18:02:31', '2023-12-08 00:00:00', NULL, NULL, 'BRAKE PAD ', 450.00, 'no', 5);

-- --------------------------------------------------------

--
-- Table structure for table `bids`
--

CREATE TABLE `bids` (
  `id` int NOT NULL,
  `auction_id` int NOT NULL,
  `user_id` int NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `bid_amount` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `bids`
--

INSERT INTO `bids` (`id`, `auction_id`, `user_id`, `timestamp`, `bid_amount`) VALUES
(4, 15, 25, '2023-12-06 10:07:19', 140000.04),
(5, 15, 25, '2023-12-06 10:07:32', 140000.04),
(6, 15, 25, '2023-12-06 10:07:45', 140000.11),
(7, 15, 25, '2023-12-06 10:14:06', 140200.11),
(8, 15, 25, '2023-12-06 10:14:25', 140700.11);

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `category_id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`category_id`, `name`, `description`, `created_at`, `updated_at`) VALUES
(4, 'Antiques', 'Description for Antiques', '2023-12-06 16:53:47', '2023-12-06 16:53:47'),
(5, 'Mechanical parts', 'Description for Mechanical parts', '2023-12-06 16:54:04', '2023-12-06 16:54:04'),
(6, 'Books', 'Description for Books', '2023-12-06 16:54:21', '2023-12-06 16:54:21'),
(7, 'Electronics', 'Description for Electronics', '2023-12-06 16:54:33', '2023-12-06 16:54:33'),
(8, 'Vehicles', 'Description for Vehicles', '2023-12-06 16:54:45', '2023-12-06 16:54:45');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text,
  `supplier_id` int DEFAULT NULL,
  `path` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `description`, `supplier_id`, `path`) VALUES
(11, 'HONDA CIVIC', 'Mileage\r\n16.5 to 25.35 kmpl\r\n\r\n\r\nEngine\r\n1597 to 1799 cc\r\n\r\n\r\nFuel Type\r\nPetrol \r\n\r\n\r\nTransmission\r\nAutomatic \r\n\r\nSeating Capacity\r\n5 Seater', 23, 'civic.webp'),
(12, 'MARUTI SWIFT', 'Mileage\r\n22.38 to 30.9 kmpl\r\n\r\n\r\nEngine\r\n1197 cc\r\n\r\n\r\nSafety\r\n2 Star (Global NCAP)\r\n\r\n\r\nFuel Type\r\nPetrol \r\n\r\n\r\nTransmission\r\nManual \r\n\r\n\r\nSeating Capacity\r\n5 Seater', 23, 'swift.webp'),
(13, 'INNOVA CRYSTA', 'Engine\r\n2393 cc\r\n\r\n\r\nSafety\r\n5 Star (ASEAN NCAP)\r\n\r\n\r\nFuel Type\r\nDiesel\r\n\r\n\r\nTransmission\r\nManual\r\n\r\n\r\nSeating Capacity\r\n7 & 8 Seater', 23, 'innova-crysta-2.jpg'),
(14, 'DRILLING MACHINE', 'Brand	Sceptre\r\n\r\n\r\nPower Source	Corded Electric\r\n\r\nMaximum Rotational Speed 2600 RPM\r\n\r\nVoltage	220 Volts\r\n\r\nAmperage 16 Amps\r\n\r\nMaximum Chuck Size 10 Millimeters\r\nColour	Red\r\nIncluded Components SP-2310 Electric Drill Machine\r\n\r\nSpecial Feature	Powerful Motor', 23, 'drill.jpg'),
(15, 'BRAKE PAD ', 'Brand	NIKAVI\r\nMaterial Carbon Fibre\r\nAuto Part Position Rear, Front\r\nVehicle Service Type Bicycle\r\n\r\nColour: black\r\n\r\nPackage contents: 1 x brake disc pad', 23, 'brk.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `seller_documents`
--

CREATE TABLE `seller_documents` (
  `id` int NOT NULL,
  `user_id` varchar(512) DEFAULT NULL,
  `document_filename` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(512) DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `verification_document` varchar(255) DEFAULT NULL,
  `status` enum('pending','approved','rejected') NOT NULL,
  `wallet` decimal(10,2) DEFAULT '0.00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role`, `email`, `address`, `verification_document`, `status`, `wallet`) VALUES
(21, 'shanidsulthan', 'shanid', 'admin', 'shanid@gmail.com', 'shanid', NULL, 'approved', 28201.02),
(22, 'buyer1', 'buyer', 'buyer', 'buyer@gmail.com', 'buyer', NULL, 'approved', 10022.00),
(23, 'seller1', 'seller', 'seller', 'seller@gmail.com', 'seller home', NULL, 'approved', 98703.08),
(24, 'buyer2', 'buyer', 'buyer', 'buyer@buyer.com', 'hvh', NULL, 'approved', 8995.00),
(25, 'shamil', 'shamil', 'buyer', 'shamilmhd2003@gmail.com', 'sssshhhhs', NULL, 'approved', 909299.89);

-- --------------------------------------------------------

--
-- Table structure for table `wallet`
--

CREATE TABLE `wallet` (
  `user_id` int NOT NULL,
  `balance` decimal(10,2) DEFAULT NULL,
  `last_source_of_update` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `wallet`
--

INSERT INTO `wallet` (`user_id`, `balance`, `last_source_of_update`) VALUES
(21, 28201.02, '28000.02 ADDED AS ADMIN SHARE FOR AUCTION NO 15'),
(22, 10022.00, 'admin  ADDED AMOUNT 0'),
(23, 98703.08, '98000.08 ADDED AS SUPPLIER SHARE FOR AUCTION NO 15'),
(24, 8995.00, 'AMOUNT 1005.00 DEDUCTED FOR BID IN AUCTION 4'),
(25, 909299.89, 'AMOUNT 500.00 DEDUCTED FOR BID IN AUCTION 15');

--
-- Triggers `wallet`
--
DELIMITER $$
CREATE TRIGGER `update_wallet_in_users` AFTER UPDATE ON `wallet` FOR EACH ROW BEGIN
    UPDATE users
    SET wallet = NEW.balance
    WHERE id = NEW.user_id;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `wallet_trigger` AFTER UPDATE ON `wallet` FOR EACH ROW BEGIN
    DECLARE _user_id INT;
    DECLARE _amount_change DECIMAL(10, 2);
    DECLARE _credit_debit ENUM('CREDIT', 'DEBIT');
    DECLARE _before_balance DECIMAL(10, 2);
    DECLARE _after_balance DECIMAL(10, 2);
    DECLARE _remarks VARCHAR(255);

    -- Determine whether it's a credit or debit
    IF NEW.balance > OLD.balance THEN
        SET _credit_debit = 'CREDIT';
        SET _amount_change = NEW.balance - OLD.balance;
        SET _user_id = NEW.user_id;
        SET _before_balance = OLD.balance;
        SET _after_balance = NEW.balance;
        SET _remarks = NEW.last_source_of_update;

        -- Insert a record into the walletlog table
        INSERT INTO walletlog (user_id, amount_change, credit_debit, before_balance, after_balance, remarks)
        VALUES (_user_id, _amount_change, _credit_debit, _before_balance, _after_balance, _remarks);
    END IF;

    IF NEW.balance < OLD.balance THEN
        SET _credit_debit = 'DEBIT';
        SET _amount_change = OLD.balance - NEW.balance;
        SET _user_id = NEW.user_id;
        SET _before_balance = OLD.balance;
        SET _after_balance = NEW.balance;
        SET _remarks = NEW.last_source_of_update;

        -- Insert a record into the walletlog table
        INSERT INTO walletlog (user_id, amount_change, credit_debit, before_balance, after_balance, remarks)
        VALUES (_user_id, _amount_change, _credit_debit, _before_balance, _after_balance, _remarks);
    END IF;

END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `walletlog`
--

CREATE TABLE `walletlog` (
  `log_id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `amount_change` decimal(10,2) DEFAULT NULL,
  `credit_debit` enum('CREDIT','DEBIT') DEFAULT NULL,
  `before_balance` decimal(10,2) DEFAULT NULL,
  `after_balance` decimal(10,2) DEFAULT NULL,
  `remarks` varchar(255) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `walletlog`
--

INSERT INTO `walletlog` (`log_id`, `user_id`, `amount_change`, `credit_debit`, `before_balance`, `after_balance`, `remarks`, `timestamp`) VALUES
(1, 22, 22.00, 'CREDIT', 0.00, 22.00, 'admin  ADDED AMOUNT 22', '2023-11-11 10:08:19'),
(2, 22, 10000.00, 'CREDIT', 22.00, 10022.00, 'admin  ADDED AMOUNT 10000', '2023-11-11 10:20:00'),
(3, 22, 1001.00, 'DEBIT', 10022.00, 9021.00, 'AMOUNT 1001.00 DEDUCTED FOR BID IN AUCTION 4', '2023-11-11 10:24:36'),
(9, 22, 1.00, 'DEBIT', 9021.00, 9020.00, 'AMOUNT 1.00 DEDUCTED FOR BID IN AUCTION 4', '2023-11-11 10:38:23'),
(10, 24, 10000.00, 'CREDIT', 0.00, 10000.00, 'admin  ADDED AMOUNT 10000', '2023-11-11 10:40:33'),
(11, 24, 1005.00, 'DEBIT', 10000.00, 8995.00, 'AMOUNT 1005.00 DEDUCTED FOR BID IN AUCTION 4', '2023-11-11 10:41:14'),
(31, 23, 703.50, 'CREDIT', 0.00, 703.50, '703.50 ADDED AS SUPPLIER SHARE FOR AUCTION NO 4', '2023-11-11 11:04:25'),
(32, 21, 201.00, 'CREDIT', 0.00, 201.00, '201.00 ADDED AS ADMIN SHARE FOR AUCTION NO 4', '2023-11-11 11:04:25'),
(33, 22, 1002.00, 'CREDIT', 9020.00, 10022.00, 'REFUND FOR BIDS PLACED IN AUCTION 4 WHICH ENDED AND YOU DID NOT WIN', '2023-11-11 11:04:26'),
(34, 25, 1000000.00, 'CREDIT', 0.00, 1000000.00, 'admin  ADDED AMOUNT 1000000', '2023-11-25 13:01:33'),
(35, 25, 50000.00, 'CREDIT', 1000000.00, 1050000.00, 'admin  ADDED AMOUNT 50000', '2023-11-25 13:05:03'),
(36, 23, 0.50, 'DEBIT', 703.50, 703.00, 'admin  ADDED AMOUNT 0', '2023-11-26 10:13:47'),
(37, 25, 140000.04, 'DEBIT', 1050000.00, 909999.96, 'AMOUNT 140000.0400000000000000008327 DEDUCTED FOR BID IN AUCTION 15', '2023-12-06 18:07:18'),
(38, 25, 0.07, 'DEBIT', 909999.96, 909999.89, 'AMOUNT 0.0700000000000000066613 DEDUCTED FOR BID IN AUCTION 15', '2023-12-06 18:07:44'),
(39, 23, 98000.08, 'CREDIT', 703.00, 98703.08, '98000.08 ADDED AS SUPPLIER SHARE FOR AUCTION NO 15', '2023-12-06 18:11:25'),
(40, 21, 28000.02, 'CREDIT', 201.00, 28201.02, '28000.02 ADDED AS ADMIN SHARE FOR AUCTION NO 15', '2023-12-06 18:11:25'),
(41, 25, 200.00, 'DEBIT', 909999.89, 909799.89, 'AMOUNT 200.00 DEDUCTED FOR BID IN AUCTION 15', '2023-12-06 18:14:05'),
(42, 25, 500.00, 'DEBIT', 909799.89, 909299.89, 'AMOUNT 500.00 DEDUCTED FOR BID IN AUCTION 15', '2023-12-06 18:14:23');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auction`
--
ALTER TABLE `auction`
  ADD PRIMARY KEY (`id`),
  ADD KEY `product_id` (`product_id`),
  ADD KEY `winner_id` (`winner_id`),
  ADD KEY `fk_auction_category` (`category_id`);

--
-- Indexes for table `bids`
--
ALTER TABLE `bids`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `idx_auction_id` (`auction_id`);

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`category_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`),
  ADD KEY `supplier_id` (`supplier_id`);

--
-- Indexes for table `seller_documents`
--
ALTER TABLE `seller_documents`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `wallet`
--
ALTER TABLE `wallet`
  ADD PRIMARY KEY (`user_id`);

--
-- Indexes for table `walletlog`
--
ALTER TABLE `walletlog`
  ADD PRIMARY KEY (`log_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auction`
--
ALTER TABLE `auction`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `bids`
--
ALTER TABLE `bids`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `category`
--
ALTER TABLE `category`
  MODIFY `category_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `seller_documents`
--
ALTER TABLE `seller_documents`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `walletlog`
--
ALTER TABLE `walletlog`
  MODIFY `log_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auction`
--
ALTER TABLE `auction`
  ADD CONSTRAINT `auction_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  ADD CONSTRAINT `auction_ibfk_2` FOREIGN KEY (`winner_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `fk_auction_category` FOREIGN KEY (`category_id`) REFERENCES `category` (`category_id`) ON DELETE RESTRICT ON UPDATE CASCADE;

--
-- Constraints for table `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`supplier_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `wallet`
--
ALTER TABLE `wallet`
  ADD CONSTRAINT `wallet_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
