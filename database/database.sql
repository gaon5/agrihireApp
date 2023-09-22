-- --------------------------------------------------------

--
-- table structure `admin`
--

DROP TABLE IF EXISTS `admin`;
CREATE TABLE IF NOT EXISTS `admin` (
  `admin_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `username` varchar(100) DEFAULT NULL,
  `title_id` int(11) NOT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `phone_number` varchar(255) DEFAULT NULL,
  `state` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`admin_id`),
  KEY `user_id` (`user_id`),
  KEY `title_id` (`title_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- table structure `category`
--

DROP TABLE IF EXISTS `category`;
CREATE TABLE IF NOT EXISTS `category` (
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `priority` int(11) DEFAULT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- table structure `city`
--

DROP TABLE IF EXISTS `city`;
CREATE TABLE IF NOT EXISTS `city` (
  `city_id` int(11) NOT NULL AUTO_INCREMENT,
  `region_id` int(11) NOT NULL,
  `city` varchar(255) NOT NULL,
  PRIMARY KEY (`city_id`),
  KEY `city_id` (`region_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=150 ;

--
-- Transfer data in table `city`
--

INSERT INTO `city` (`city_id`, `region_id`, `city`) VALUES
(1, 1, 'Dargaville'),
(2, 1, 'Kaikohe'),
(3, 1, 'Kaitaia'),
(4, 1, 'Kawakawa'),
(5, 1, 'Kerikeri'),
(6, 1, 'Mangawhai'),
(7, 1, 'Maungaturoto'),
(8, 1, 'Paihia'),
(9, 1, 'Whangarei'),
(10, 2, 'Albany'),
(11, 2, 'Auckland City'),
(12, 2, 'Botany Downs'),
(13, 2, 'Clevedon'),
(14, 2, 'Franklin'),
(15, 2, 'Great Barrier Island'),
(16, 2, 'Helensville'),
(17, 2, 'Henderson'),
(18, 2, 'Hibiscus Coast'),
(19, 2, 'Kumeu'),
(20, 2, 'Mangere'),
(21, 2, 'Manukau'),
(22, 2, 'New Lynn'),
(23, 2, 'North Shore'),
(24, 2, 'Onehunga'),
(25, 2, 'Papakura'),
(26, 2, 'Pukekohe'),
(27, 2, 'Remuera'),
(28, 2, 'Waiheke Island'),
(29, 2, 'Waitakere'),
(30, 2, 'Waiuku'),
(31, 2, 'Warkworth'),
(32, 2, 'Wellsford'),
(33, 3, 'Cambridge'),
(34, 3, 'Coromandel'),
(35, 3, 'Hamilton'),
(36, 3, 'Huntly'),
(37, 3, 'Matamata'),
(38, 3, 'Morrinsville'),
(39, 3, 'Ngaruawahia'),
(40, 3, 'Ngatea'),
(41, 3, 'Otorohanga'),
(42, 3, 'Paeroa'),
(43, 3, 'Raglan'),
(44, 3, 'Taumarunui'),
(45, 3, 'Taupo'),
(46, 3, 'Te Awamutu'),
(47, 3, 'Te Kuiti'),
(48, 3, 'Thames'),
(49, 3, 'Tokoroa/Putaruru'),
(50, 3, 'Turangi '),
(51, 3, 'Waihi'),
(52, 3, 'Whangamata'),
(53, 3, 'Whitianga'),
(54, 4, 'Katikati'),
(55, 4, 'Kawerau'),
(56, 4, 'Mt. Maunganui'),
(57, 4, 'Opotiki'),
(58, 4, 'Papamoa'),
(59, 4, 'Rotorua'),
(60, 4, 'Tauranga'),
(61, 4, 'Te Puke'),
(62, 4, 'Waihi Beach'),
(63, 4, 'Whakatane'),
(64, 5, 'Gisborne'),
(65, 5, 'Ruatoria'),
(66, 6, 'Hastings'),
(67, 6, 'Napier'),
(68, 6, 'Waipukurau'),
(69, 6, 'Wairoa'),
(70, 7, 'Hawera'),
(71, 7, 'Mokau'),
(72, 7, 'New Plymouth'),
(73, 7, 'Opunake'),
(74, 7, 'Stratford'),
(75, 8, 'Ohakune'),
(76, 8, 'Taihape'),
(77, 8, 'Waiouru'),
(78, 8, 'Whanganui'),
(79, 8, 'Bulls'),
(80, 8, 'Dannevirke'),
(81, 8, 'Feilding'),
(82, 8, 'Levin'),
(83, 8, 'Manawatu'),
(84, 8, 'Marton'),
(85, 8, 'Pahiatua'),
(86, 8, 'Palmerston North'),
(87, 8, 'Woodville'),
(88, 9, 'Kapiti'),
(89, 9, 'Lower Hutt City'),
(90, 9, 'Porirua'),
(91, 9, 'Upper Hutt City'),
(92, 9, 'Wellington City'),
(93, 10, 'Golden Bay'),
(94, 10, 'Motueka'),
(95, 10, 'Murchison'),
(96, 10, 'Nelson'),
(97, 11, 'Blenheim'),
(98, 11, 'Marlborough Sounds'),
(99, 11, 'Picton'),
(100, 12, 'Greymouth'),
(101, 12, 'Hokitika'),
(102, 12, 'Westport'),
(103, 13, 'Akaroa'),
(104, 13, 'Amberley'),
(105, 13, 'Ashburton'),
(106, 13, 'Belfast'),
(107, 13, 'Cheviot'),
(108, 13, 'Christchurch City'),
(109, 13, 'Darfield'),
(110, 13, 'Fairlie'),
(111, 13, 'Ferrymead'),
(112, 13, 'Geraldine'),
(113, 13, 'Halswell'),
(114, 13, 'Hanmer Springs'),
(115, 13, 'Kaiapoi'),
(116, 13, 'Kaikoura'),
(117, 13, 'Lyttelton'),
(118, 13, 'Mt Cook'),
(119, 13, 'Rangiora'),
(120, 13, 'Rolleston'),
(121, 13, 'Selwyn'),
(122, 14, 'Kurow'),
(123, 14, 'Oamaru'),
(124, 14, 'Timaru'),
(125, 14, 'Twizel'),
(126, 14, 'Waimate'),
(127, 15, 'Alexandra'),
(128, 15, 'Balclutha'),
(129, 15, 'Cromwell'),
(130, 15, 'Dunedin'),
(131, 15, 'Lawrence'),
(132, 15, 'Milton'),
(133, 15, 'Palmerston'),
(134, 15, 'Queenstown'),
(135, 15, 'Ranfurly'),
(136, 15, 'Roxburgh'),
(137, 15, 'Tapanui'),
(138, 15, 'Wanaka'),
(139, 16, 'Bluff'),
(140, 16, 'Edendale'),
(141, 16, 'Gore'),
(142, 16, 'Invercargill'),
(143, 16, 'Lumsden'),
(144, 16, 'Otautau'),
(145, 16, 'Riverton'),
(146, 16, 'Stewart Island'),
(147, 16, 'Te Anau'),
(148, 16, 'Tokanui'),
(149, 16, 'Winton');

-- --------------------------------------------------------

--
-- table structure `classify`
--

DROP TABLE IF EXISTS `classify`;
CREATE TABLE IF NOT EXISTS `classify` (
  `classify_id` int(11) NOT NULL AUTO_INCREMENT,
  `sub_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  PRIMARY KEY (`classify_id`),
  KEY `sub_id` (`sub_id`),
  KEY `product_id` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- table structure `customer`
--

DROP TABLE IF EXISTS `customer`;
CREATE TABLE IF NOT EXISTS `customer` (
  `customer_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `username` varchar(100) DEFAULT NULL,
  `title_id` int(11) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `phone_number` varchar(255) DEFAULT NULL,
  `city_id` int(11) DEFAULT NULL,
  `region_id` int(11) DEFAULT NULL,
  `street_name` varchar(255) NOT NULL,
  `birth_date` date DEFAULT NULL,
  `question_id` int(11) NOT NULL,
  `answer` text NOT NULL,
  `state` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`customer_id`),
  KEY `user_id` (`user_id`),
  KEY `title_id` (`title_id`),
  KEY `city_id` (`city_id`),
  KEY `region_id` (`region_id`),
  KEY `question_id` (`question_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- table structure `equipment_maintenance`
--

DROP TABLE IF EXISTS `equipment_maintenance`;
CREATE TABLE IF NOT EXISTS `equipment_maintenance` (
  `maintenance_id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `maintenance_date` date NOT NULL,
  `maintenance_type_id` int(11) NOT NULL,
  `maintenance_status_id` int(11) NOT NULL,
  `notes` text,
  PRIMARY KEY (`maintenance_id`),
  KEY `product_id` (`product_id`),
  KEY `maintenance_type_id` (`maintenance_type_id`),
  KEY `maintenance_status_id` (`maintenance_status_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- table structure `equipment_rental_status`
--

DROP TABLE IF EXISTS `equipment_rental_status`;
CREATE TABLE IF NOT EXISTS `equipment_rental_status` (
  `rental_status_id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `rental_start_date` date NOT NULL,
  `expected_return_date` date DEFAULT NULL,
  `actual_return_date` date DEFAULT NULL,
  `rental_status` int(11) NOT NULL,
  `notes` text,
  PRIMARY KEY (`rental_status_id`),
  KEY `product_id` (`product_id`),
  KEY `customer_id` (`customer_id`),
  KEY `rental_status` (`rental_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- table structure `event_type`
--

DROP TABLE IF EXISTS `event_type`;
CREATE TABLE IF NOT EXISTS `event_type` (
  `event_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`event_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- table structure `hire_log`
--

DROP TABLE IF EXISTS `hire_log`;
CREATE TABLE IF NOT EXISTS `hire_log` (
  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `staff_id` int(11) NOT NULL,
  `datetime` datetime NOT NULL,
  `event_type_id` int(11) NOT NULL,
  `message` text,
  `product_id` int(11) NOT NULL,
  PRIMARY KEY (`log_id`),
  KEY `staff_id` (`staff_id`),
  KEY `event_type_id` (`event_type_id`),
  KEY `hire_log_ibfk_3` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- table structure `maintenance_status`
--

DROP TABLE IF EXISTS `maintenance_status`;
CREATE TABLE IF NOT EXISTS `maintenance_status` (
  `maintenance_status_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`maintenance_status_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- table structure `maintenance_type`
--

DROP TABLE IF EXISTS `maintenance_type`;
CREATE TABLE IF NOT EXISTS `maintenance_type` (
  `maintenance_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`maintenance_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- table structure `order_item`
--

DROP TABLE IF EXISTS `order_item`;
CREATE TABLE IF NOT EXISTS `order_item` (
  `order_item_id` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `count` int(11) DEFAULT '1',
  `price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`order_item_id`),
  KEY `order_id` (`order_id`),
  KEY `product_id` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- table structure `order_list`
--

DROP TABLE IF EXISTS `order_list`;
CREATE TABLE IF NOT EXISTS `order_list` (
  `order_id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_id` int(11) NOT NULL,
  `status_id` int(11) NOT NULL,
  `datetime` datetime NOT NULL,
  `price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`order_id`),
  KEY `customer_id` (`customer_id`),
  KEY `status_id` (`status_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- table structure `order_status`
--

DROP TABLE IF EXISTS `order_status`;
CREATE TABLE IF NOT EXISTS `order_status` (
  `status_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`status_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- table structure `payment`
--

DROP TABLE IF EXISTS `payment`;
CREATE TABLE IF NOT EXISTS `payment` (
  `payment_id` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` int(11) NOT NULL,
  `status_id` int(11) NOT NULL,
  `payment_type_id` int(11) NOT NULL,
  `datetime` datetime NOT NULL,
  PRIMARY KEY (`payment_id`),
  KEY `order_id` (`order_id`),
  KEY `status_id` (`status_id`),
  KEY `payment_type_id` (`payment_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- table structure `payment_status`
--

DROP TABLE IF EXISTS `payment_status`;
CREATE TABLE IF NOT EXISTS `payment_status` (
  `status_id` int(11) NOT NULL AUTO_INCREMENT,
  `status_name` varchar(255) NOT NULL,
  PRIMARY KEY (`status_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- table structure `payment_type`
--

DROP TABLE IF EXISTS `payment_type`;
CREATE TABLE IF NOT EXISTS `payment_type` (
  `payment_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`payment_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- table structure `product`
--

DROP TABLE IF EXISTS `product`;
CREATE TABLE IF NOT EXISTS `product` (
  `product_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `count` int(11) DEFAULT '0',
  `priority` int(11) DEFAULT NULL,
  `length` decimal(10,2) DEFAULT NULL,
  `width` decimal(10,2) DEFAULT NULL,
  `height` decimal(10,2) DEFAULT NULL,
  `requires_drive_license` tinyint(1) DEFAULT '0',
  `min_stock_threshold` int(11) NOT NULL DEFAULT '1',
  `description` text,
  `detail` text,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- table structure `product_img`
--

DROP TABLE IF EXISTS `product_img`;
CREATE TABLE IF NOT EXISTS `product_img` (
  `image_id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `image_url` varchar(255) NOT NULL,
  PRIMARY KEY (`image_id`),
  KEY `product_id` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- table structure `region`
--

DROP TABLE IF EXISTS `region`;
CREATE TABLE IF NOT EXISTS `region` (
  `region_id` int(11) NOT NULL AUTO_INCREMENT,
  `region` varchar(255) NOT NULL,
  PRIMARY KEY (`region_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=17 ;

--
-- Transfer data in table `region`
--

INSERT INTO `region` (`region_id`, `region`) VALUES
(1, 'Northland'),
(2, 'Auckland'),
(3, 'Waikato'),
(4, 'Bay Of Plenty'),
(5, 'Gisborne'),
(6, 'Hawke''s Bay'),
(7, 'Taranaki'),
(8, 'Manawatu - Whanganui'),
(9, 'Wellington'),
(10, 'Nelson Bays'),
(11, 'Marlborough'),
(12, 'West Coast'),
(13, 'Canterbury'),
(14, 'Timaru - Oamaru'),
(15, 'Otago'),
(16, 'Southland');

-- --------------------------------------------------------

--
-- table structure `rental_status`
--

DROP TABLE IF EXISTS `rental_status`;
CREATE TABLE IF NOT EXISTS `rental_status` (
  `rental_status_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`rental_status_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- table structure `security_question`
--

DROP TABLE IF EXISTS `security_question`;
CREATE TABLE IF NOT EXISTS `security_question` (
  `question_id` int(11) NOT NULL AUTO_INCREMENT,
  `question` text NOT NULL,
  PRIMARY KEY (`question_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=11 ;

--
-- Transfer data in table `security_question`
--

INSERT INTO `security_question` (`question_id`, `question`) VALUES
(1, 'What is your mother''s name?'),
(2, 'What was the name of your first pet?'),
(3, 'In which city were you born?'),
(4, 'What is the name of your favorite teacher?'),
(5, 'What is your favorite book?'),
(6, 'What is the make and model of your first car?'),
(7, 'What is the name of your best friend from childhood?'),
(8, 'What is the name of your favorite movie?'),
(9, 'What was the street you grew up on?'),
(10, 'What is your favorite color?');

-- --------------------------------------------------------

--
-- table structure `shopping_cart`
--

DROP TABLE IF EXISTS `shopping_cart`;
CREATE TABLE IF NOT EXISTS `shopping_cart` (
  `shopping_id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_id` int(11) NOT NULL,
  PRIMARY KEY (`shopping_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- table structure `shopping_cart_item`
--

DROP TABLE IF EXISTS `shopping_cart_item`;
CREATE TABLE IF NOT EXISTS `shopping_cart_item` (
  `cart_item_id` int(11) NOT NULL AUTO_INCREMENT,
  `shopping_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `count` int(11) DEFAULT '1',
  PRIMARY KEY (`cart_item_id`),
  KEY `shopping_id` (`shopping_id`),
  KEY `product_id` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- table structure `staff`
--

DROP TABLE IF EXISTS `staff`;
CREATE TABLE IF NOT EXISTS `staff` (
  `staff_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `username` varchar(100) DEFAULT NULL,
  `title_id` int(11) NOT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `phone_number` varchar(255) DEFAULT NULL,
  `state` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`staff_id`),
  KEY `user_id` (`user_id`),
  KEY `title_id` (`title_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- table structure `sub_category`
--

DROP TABLE IF EXISTS `sub_category`;
CREATE TABLE IF NOT EXISTS `sub_category` (
  `sub_id` int(11) NOT NULL AUTO_INCREMENT,
  `category_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`sub_id`),
  KEY `category_id` (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- table structure `title`
--

DROP TABLE IF EXISTS `title`;
CREATE TABLE IF NOT EXISTS `title` (
  `title_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  PRIMARY KEY (`title_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=4 ;

--
-- Transfer data in table `title`
--

INSERT INTO `title` (`title_id`, `title`) VALUES
(1, 'Mr.'),
(2, 'Ms.'),
(3, 'Miss.');

-- --------------------------------------------------------

--
-- table structure `user_account`
--

DROP TABLE IF EXISTS `user_account`;
CREATE TABLE IF NOT EXISTS `user_account` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `is_customer` tinyint(1) NOT NULL DEFAULT '0',
  `is_staff` tinyint(1) NOT NULL DEFAULT '0',
  `is_admin` tinyint(1) NOT NULL DEFAULT '0',
  `register_date` date NOT NULL,
  `last_login_date` date NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1 ;

--
-- Limit exported tables
--

--
-- Limit table `admin`
--
ALTER TABLE `admin`
  ADD CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_account` (`user_id`),
  ADD CONSTRAINT `admin_ibfk_2` FOREIGN KEY (`title_id`) REFERENCES `title` (`title_id`);

--
-- Limit table `city`
--
ALTER TABLE `city`
  ADD CONSTRAINT `city_ibfk_1` FOREIGN KEY (`region_id`) REFERENCES `region` (`region_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limit table `classify`
--
ALTER TABLE `classify`
  ADD CONSTRAINT `classify_ibfk_1` FOREIGN KEY (`sub_id`) REFERENCES `sub_category` (`sub_id`),
  ADD CONSTRAINT `classify_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`);

--
-- Limit table `customer`
--
ALTER TABLE `customer`
  ADD CONSTRAINT `customer_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_account` (`user_id`),
  ADD CONSTRAINT `customer_ibfk_2` FOREIGN KEY (`title_id`) REFERENCES `title` (`title_id`),
  ADD CONSTRAINT `customer_ibfk_3` FOREIGN KEY (`city_id`) REFERENCES `city` (`city_id`),
  ADD CONSTRAINT `customer_ibfk_4` FOREIGN KEY (`region_id`) REFERENCES `region` (`region_id`),
  ADD CONSTRAINT `customer_ibfk_5` FOREIGN KEY (`question_id`) REFERENCES `security_question` (`question_id`);

--
-- Limit table `equipment_maintenance`
--
ALTER TABLE `equipment_maintenance`
  ADD CONSTRAINT `equipment_maintenance_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`),
  ADD CONSTRAINT `equipment_maintenance_ibfk_2` FOREIGN KEY (`maintenance_type_id`) REFERENCES `maintenance_type` (`maintenance_type_id`),
  ADD CONSTRAINT `equipment_maintenance_ibfk_3` FOREIGN KEY (`maintenance_status_id`) REFERENCES `maintenance_status` (`maintenance_status_id`);

--
-- Limit table `equipment_rental_status`
--
ALTER TABLE `equipment_rental_status`
  ADD CONSTRAINT `equipment_rental_status_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`),
  ADD CONSTRAINT `equipment_rental_status_ibfk_2` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`),
  ADD CONSTRAINT `equipment_rental_status_ibfk_3` FOREIGN KEY (`rental_status`) REFERENCES `rental_status` (`rental_status_id`);

--
-- Limit table `hire_log`
--
ALTER TABLE `hire_log`
  ADD CONSTRAINT `hire_log_ibfk_1` FOREIGN KEY (`staff_id`) REFERENCES `staff` (`staff_id`),
  ADD CONSTRAINT `hire_log_ibfk_2` FOREIGN KEY (`event_type_id`) REFERENCES `event_type` (`event_type_id`),
  ADD CONSTRAINT `hire_log_ibfk_3` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`);

--
-- Limit table `order_item`
--
ALTER TABLE `order_item`
  ADD CONSTRAINT `order_item_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `order_list` (`order_id`),
  ADD CONSTRAINT `order_item_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`);

--
-- Limit table `order_list`
--
ALTER TABLE `order_list`
  ADD CONSTRAINT `order_list_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`),
  ADD CONSTRAINT `order_list_ibfk_2` FOREIGN KEY (`status_id`) REFERENCES `order_status` (`status_id`);

--
-- Limit table `payment`
--
ALTER TABLE `payment`
  ADD CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `order_list` (`order_id`),
  ADD CONSTRAINT `payment_ibfk_2` FOREIGN KEY (`status_id`) REFERENCES `payment_status` (`status_id`),
  ADD CONSTRAINT `payment_ibfk_3` FOREIGN KEY (`payment_type_id`) REFERENCES `payment_type` (`payment_type_id`);

--
-- Limit table `product_img`
--
ALTER TABLE `product_img`
  ADD CONSTRAINT `product_img_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`);

--
-- Limit table `shopping_cart_item`
--
ALTER TABLE `shopping_cart_item`
  ADD CONSTRAINT `shopping_cart_item_ibfk_1` FOREIGN KEY (`shopping_id`) REFERENCES `shopping_cart` (`shopping_id`),
  ADD CONSTRAINT `shopping_cart_item_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`);

--
-- Limit table `staff`
--
ALTER TABLE `staff`
  ADD CONSTRAINT `staff_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_account` (`user_id`),
  ADD CONSTRAINT `staff_ibfk_2` FOREIGN KEY (`title_id`) REFERENCES `title` (`title_id`);

--
-- Limit table `sub_category`
--
ALTER TABLE `sub_category`
  ADD CONSTRAINT `sub_category_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`category_id`);
