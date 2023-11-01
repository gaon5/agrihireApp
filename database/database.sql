CREATE DATABASE  IF NOT EXISTS `hire` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `hire`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: hire
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `admin_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `username` varchar(100) DEFAULT NULL,
  `title_id` int NOT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `phone_number` varchar(255) DEFAULT NULL,
  `state` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`admin_id`),
  KEY `user_id` (`user_id`),
  KEY `title_id` (`title_id`),
  CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_account` (`user_id`),
  CONSTRAINT `admin_ibfk_2` FOREIGN KEY (`title_id`) REFERENCES `title` (`title_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,1,'admin',2,'admin','admin','02000000',1);
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`category_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (4,'Building-and-Renovation'),(3,'Earthmoving'),(1,'Landscaping'),(5,'Tool-and-Equipment'),(2,'Trailers');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `city`
--

DROP TABLE IF EXISTS `city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `city` (
  `city_id` int NOT NULL AUTO_INCREMENT,
  `region_id` int NOT NULL,
  `city` varchar(255) NOT NULL,
  PRIMARY KEY (`city_id`),
  KEY `city_id` (`region_id`),
  CONSTRAINT `city_ibfk_1` FOREIGN KEY (`region_id`) REFERENCES `region` (`region_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=150 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `city`
--

LOCK TABLES `city` WRITE;
/*!40000 ALTER TABLE `city` DISABLE KEYS */;
INSERT INTO `city` VALUES (1,1,'Dargaville'),(2,1,'Kaikohe'),(3,1,'Kaitaia'),(4,1,'Kawakawa'),(5,1,'Kerikeri'),(6,1,'Mangawhai'),(7,1,'Maungaturoto'),(8,1,'Paihia'),(9,1,'Whangarei'),(10,2,'Albany'),(11,2,'Auckland City'),(12,2,'Botany Downs'),(13,2,'Clevedon'),(14,2,'Franklin'),(15,2,'Great Barrier Island'),(16,2,'Helensville'),(17,2,'Henderson'),(18,2,'Hibiscus Coast'),(19,2,'Kumeu'),(20,2,'Mangere'),(21,2,'Manukau'),(22,2,'New Lynn'),(23,2,'North Shore'),(24,2,'Onehunga'),(25,2,'Papakura'),(26,2,'Pukekohe'),(27,2,'Remuera'),(28,2,'Waiheke Island'),(29,2,'Waitakere'),(30,2,'Waiuku'),(31,2,'Warkworth'),(32,2,'Wellsford'),(33,3,'Cambridge'),(34,3,'Coromandel'),(35,3,'Hamilton'),(36,3,'Huntly'),(37,3,'Matamata'),(38,3,'Morrinsville'),(39,3,'Ngaruawahia'),(40,3,'Ngatea'),(41,3,'Otorohanga'),(42,3,'Paeroa'),(43,3,'Raglan'),(44,3,'Taumarunui'),(45,3,'Taupo'),(46,3,'Te Awamutu'),(47,3,'Te Kuiti'),(48,3,'Thames'),(49,3,'Tokoroa/Putaruru'),(50,3,'Turangi '),(51,3,'Waihi'),(52,3,'Whangamata'),(53,3,'Whitianga'),(54,4,'Katikati'),(55,4,'Kawerau'),(56,4,'Mt. Maunganui'),(57,4,'Opotiki'),(58,4,'Papamoa'),(59,4,'Rotorua'),(60,4,'Tauranga'),(61,4,'Te Puke'),(62,4,'Waihi Beach'),(63,4,'Whakatane'),(64,5,'Gisborne'),(65,5,'Ruatoria'),(66,6,'Hastings'),(67,6,'Napier'),(68,6,'Waipukurau'),(69,6,'Wairoa'),(70,7,'Hawera'),(71,7,'Mokau'),(72,7,'New Plymouth'),(73,7,'Opunake'),(74,7,'Stratford'),(75,8,'Ohakune'),(76,8,'Taihape'),(77,8,'Waiouru'),(78,8,'Whanganui'),(79,8,'Bulls'),(80,8,'Dannevirke'),(81,8,'Feilding'),(82,8,'Levin'),(83,8,'Manawatu'),(84,8,'Marton'),(85,8,'Pahiatua'),(86,8,'Palmerston North'),(87,8,'Woodville'),(88,9,'Kapiti'),(89,9,'Lower Hutt City'),(90,9,'Porirua'),(91,9,'Upper Hutt City'),(92,9,'Wellington City'),(93,10,'Golden Bay'),(94,10,'Motueka'),(95,10,'Murchison'),(96,10,'Nelson'),(97,11,'Blenheim'),(98,11,'Marlborough Sounds'),(99,11,'Picton'),(100,12,'Greymouth'),(101,12,'Hokitika'),(102,12,'Westport'),(103,13,'Akaroa'),(104,13,'Amberley'),(105,13,'Ashburton'),(106,13,'Belfast'),(107,13,'Cheviot'),(108,13,'Christchurch City'),(109,13,'Darfield'),(110,13,'Fairlie'),(111,13,'Ferrymead'),(112,13,'Geraldine'),(113,13,'Halswell'),(114,13,'Hanmer Springs'),(115,13,'Kaiapoi'),(116,13,'Kaikoura'),(117,13,'Lyttelton'),(118,13,'Mt Cook'),(119,13,'Rangiora'),(120,13,'Rolleston'),(121,13,'Selwyn'),(122,14,'Kurow'),(123,14,'Oamaru'),(124,14,'Timaru'),(125,14,'Twizel'),(126,14,'Waimate'),(127,15,'Alexandra'),(128,15,'Balclutha'),(129,15,'Cromwell'),(130,15,'Dunedin'),(131,15,'Lawrence'),(132,15,'Milton'),(133,15,'Palmerston'),(134,15,'Queenstown'),(135,15,'Ranfurly'),(136,15,'Roxburgh'),(137,15,'Tapanui'),(138,15,'Wanaka'),(139,16,'Bluff'),(140,16,'Edendale'),(141,16,'Gore'),(142,16,'Invercargill'),(143,16,'Lumsden'),(144,16,'Otautau'),(145,16,'Riverton'),(146,16,'Stewart Island'),(147,16,'Te Anau'),(148,16,'Tokanui'),(149,16,'Winton');
/*!40000 ALTER TABLE `city` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `classify`
--

DROP TABLE IF EXISTS `classify`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `classify` (
  `classify_id` int NOT NULL AUTO_INCREMENT,
  `sub_id` int NOT NULL,
  `equipment_id` int NOT NULL,
  PRIMARY KEY (`classify_id`),
  KEY `sub_id` (`sub_id`),
  KEY `equipment_id` (`equipment_id`),
  CONSTRAINT `classify_ibfk_1` FOREIGN KEY (`sub_id`) REFERENCES `sub_category` (`sub_id`),
  CONSTRAINT `classify_ibfk_2` FOREIGN KEY (`equipment_id`) REFERENCES `equipment` (`equipment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classify`
--

LOCK TABLES `classify` WRITE;
/*!40000 ALTER TABLE `classify` DISABLE KEYS */;
INSERT INTO `classify` VALUES (1,7,1),(2,8,2),(3,8,3),(4,2,4),(5,2,5),(6,3,6),(7,3,7),(8,5,8),(9,6,9),(10,6,10),(11,9,11),(12,9,12),(13,14,13),(14,14,14),(15,11,15),(16,11,16),(17,12,17),(18,12,18),(19,13,19),(20,13,20),(21,14,21);
/*!40000 ALTER TABLE `classify` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contact`
--

DROP TABLE IF EXISTS `contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contact` (
  `contact_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(11) NOT NULL,
  `last_name` varchar(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `location` varchar(255) NOT NULL,
  `enquiry_type` varchar(11) NOT NULL,
  `enquiry_details` varchar(255) NOT NULL,
  PRIMARY KEY (`contact_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact`
--

LOCK TABLES `contact` WRITE;
/*!40000 ALTER TABLE `contact` DISABLE KEYS */;
INSERT INTO `contact` VALUES (7,'Nicholas','Ting','nickyting222@gmail.com','021526533','Christchurch','general','Question');
/*!40000 ALTER TABLE `contact` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `customer_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `username` varchar(100) DEFAULT NULL,
  `title_id` int NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `phone_number` varchar(255) DEFAULT NULL,
  `city_id` int DEFAULT NULL,
  `region_id` int DEFAULT NULL,
  `street_name` varchar(255) NOT NULL,
  `birth_date` date DEFAULT NULL,
  `question_id` int NOT NULL,
  `answer` text NOT NULL,
  `state` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`customer_id`),
  KEY `user_id` (`user_id`),
  KEY `title_id` (`title_id`),
  KEY `city_id` (`city_id`),
  KEY `region_id` (`region_id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `customer_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_account` (`user_id`),
  CONSTRAINT `customer_ibfk_2` FOREIGN KEY (`title_id`) REFERENCES `title` (`title_id`),
  CONSTRAINT `customer_ibfk_3` FOREIGN KEY (`city_id`) REFERENCES `city` (`city_id`),
  CONSTRAINT `customer_ibfk_4` FOREIGN KEY (`region_id`) REFERENCES `region` (`region_id`),
  CONSTRAINT `customer_ibfk_5` FOREIGN KEY (`question_id`) REFERENCES `security_question` (`question_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (1,3,'customer1',1,'John','Ting','021526533',1,1,'211 Wainoni Road','2001-02-22',1,'Jenny',1),(4,6,NULL,1,'Ting','John','0210305678',108,13,'111 Kendal Avenue','1999-02-20',1,'1',1),(5,7,NULL,2,'Lim','Beatrice','0210876543',108,13,'48 Epsom Road','1998-03-14',1,'1',1),(6,8,NULL,2,'Ting','Emily','021526999',108,13,'211 Wainoni Road','2001-11-10',1,'1',1),(7,9,NULL,1,'Ngu','Adrian','0211234567',108,13,'339 Halswell Road','2001-10-29',1,'1',1);
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipment`
--

DROP TABLE IF EXISTS `equipment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipment` (
  `equipment_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `count` int DEFAULT '0',
  `priority` int DEFAULT NULL,
  `length` decimal(10,2) DEFAULT NULL,
  `width` decimal(10,2) DEFAULT NULL,
  `height` decimal(10,2) DEFAULT NULL,
  `requires_drive_license` tinyint(1) DEFAULT '0',
  `min_stock_threshold` int NOT NULL DEFAULT '1',
  `description` text,
  `detail` text,
  PRIMARY KEY (`equipment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipment`
--

LOCK TABLES `equipment` WRITE;
/*!40000 ALTER TABLE `equipment` DISABLE KEYS */;
INSERT INTO `equipment` VALUES (1,'2.8 Tonne Swivel Dumper',141.00,2,0,45.00,45.00,1.00,1,1,'Description- For transporting gravel and topsoil. Easy tipping into trenches.','Description- For transporting gravel and topsoil. Easy tipping into trenches.'),(2,'B3150 Tractor Grader',125.00,2,0,300.00,185.00,233.00,0,1,'Smallest Tractor Grader but packs a real punch. Ideal for delicate finishing tasks and working inside buildings. ','It is an open cab model with turf tyres to help protect surfaces. The folding ROPS frame allows entry through lower doorways and tighter spaces.'),(3,'M5111 ROP’s Tractor Grader',140.00,2,0,465.00,280.00,300.00,1,1,'Wide-open design to get an excellent view of the blade below for precise grade adjustment to ensure a flawless finish. It is an all-around top performer. Easy to use and simple to maintain.','This Grader is highly versatile and delivers peak performance, fully utilizing its 3,050mm blade on any construction site. The machine comes equipped with an intuitive control system, featuring a standard laser/2D/3D compatible interface allowing exceptional accuracy.'),(4,'Post Hole Borer Motorised One Person',92.00,2,0,38.00,51.00,34.00,0,1,'Makes digging post holes for fencing, building piles, loosening up hard soil and plant holes a breeze!','Fits auger diameter of 100 – 200mm'),(5,'Post Hole Borer Motorised Two Person',155.00,2,0,155.00,50.00,50.00,0,1,'Makes digging post holes for fencing, building piles, loosening up hard soil and plant holes a breeze!','Fits auger diameter of 100 – 350mm'),(6,'Leaf Blower Hand Held',42.00,2,0,95.00,17.00,25.00,0,1,'Handy tool to help speed up the process of tidying the garden. It can suck up lighter objects or leaves, clippings etc. into a pile.','Designed with a specialised stop switch and semi-automatic choke lever, the blower automatically resets itself to the run position while helping prevent accidental flooding for smooth starts.'),(7,'Leaf Blower Hand Held Battery Powered',40.00,2,0,120.00,20.00,35.00,0,1,'Lightweight, easy to use and quiet leaf blower.','Has a boost power mode to give extra power when needed. Comes with cruise control for ease when blowing leafs and debris away.'),(8,'Trailer High Side Single Axle up to 2.47m x 1.5m',68.00,2,0,350.00,201.00,430.00,0,1,'For moving furniture, rubbish or garden prunings etc. Highside with tail gate','Max load 1070kg. Unbraked.'),(9,'Chiller Trailer Small',54.00,2,0,340.00,170.00,210.00,0,1,'Transporting cold items','Cooling unit mounted on trailer'),(10,'Chiller Trailer Large',72.00,2,0,450.00,240.00,200.00,0,1,'Transporting cold items','Cooling unit mounted on trailer'),(11,'Excavator Mini - 1.8T',84.00,2,0,371.00,99.00,233.00,0,1,'User-friendly and well-suited for confined spaces, this equipment is perfect for small to medium-scale projects, such as drainage work, trenching, pool excavations, and building foundations. Its rubber tracks safeguard surfaces and guarantee noiseless mobility, while the inclusion of a backfill blade enhances user convenience.','Adjustable width tracks to allow passage through narrow spaces. Low noise diesel engine'),(12,'Excavator Mini – 1.7T Zero Swing',84.00,2,0,354.50,124.00,234.00,0,1,'Designed for small to medium projects in confined spaces like drainage, trenches, pool excavations, and building foundations, this mini excavator offers ease of use, rubber track protection, quiet travel, powerful digging force, and a wide working range.','Its zero tail swing design ensures it\'s perfect for congested job sites, making it a versatile choice for various construction scenarios.  Track can be adjusted to between 990mm - 1240mm to navigate narrow spaces'),(13,' Circular 190mm Cordless',40.00,2,0,30.70,39.30,23.30,0,1,'A cordless circular saw that\'s handheld, designed for cutting various materials up to 70mm in thickness, including wood, plastics, drywall panels, gypsum fiberboard, and composite materials.','It has a sturdy baseplate, rechargeable batteries, comes with spare battery and charger.'),(14,'Circular 225mm Cordless',40.00,2,0,35.00,39.30,27.80,0,1,'A robust professional saw suitable for framing, fencing, flooring, and general carpentry tasks.','2100 watt motor for maximum productivity'),(15,'Drill Electric 16 To 20Mm Chuck',45.00,2,0,35.00,31.20,20.70,0,1,'Suitable for drilling a variety of materials including wood and metal.','Maximum Drill capacity is 16mm steel & 45mm wood. 1100 watts motor for maximum productivity.'),(16,'Drill Cordless',45.00,2,0,23.10,10.00,30.50,0,1,'A light, easy to use, re-chargeable battery powered hand tool ideal for drilling timber and steel where 240V power is unavailable or inconvenient. Battery charger included for prolonged use.','High / low speed. Comfort grip'),(17,'Fencing Batten Stapler Stockade ST-315i',45.00,2,0,37.80,11.00,39.60,0,1,'Ideal tool for efficient fence construction and maintenance, driving 3.15mm diameter staples consistently without the need for compressors or airlines.','Adjustable depth of drive offers flexibility to achieve the desired staple depth, ensuring a superior finish while preventing damage to the wire.'),(18,'Gas Nailer to 90mm',45.00,2,0,35.00,23.00,29.00,0,1,'Perfect for timber framing applications such as wall framing, fencing, and pallet making, making it an ideal choice for larger framing projects in locations where compressed air is unavailable, eliminating the need for hoses or power cords.','Maximum nail length 90mm'),(19,'Survey Laser Infrared Beam 200m',34.00,2,0,17.50,24.80,19.70,0,1,'For taking fast and accurate levels on building or construction sites.','Accuracy is ± 2.6mm/30m. Self leveling range is ±5º'),(20,'Moisture Meter',56.00,2,0,11.90,4.60,2.50,0,1,'Meaures the moisture;content in wood, walls and other surfaces','Easy to use; backlit display for use in all lighting conditions.'),(21,'Wallboard Screw Gun Collated/Cartridge Type Battery',45.00,2,0,32.30,23.00,27.80,0,1,'Wallboard Screw Gun Collated/Cartridge Type Battery','Has a magazine of screws to reduce reloading time. No electric cord to get in the way.');
/*!40000 ALTER TABLE `equipment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipment_img`
--

DROP TABLE IF EXISTS `equipment_img`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipment_img` (
  `image_id` int NOT NULL AUTO_INCREMENT,
  `equipment_id` int NOT NULL,
  `image_url` varchar(255) NOT NULL,
  `priority` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`image_id`),
  KEY `product_id` (`equipment_id`),
  CONSTRAINT `equipment_img_ibfk_1` FOREIGN KEY (`equipment_id`) REFERENCES `equipment` (`equipment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipment_img`
--

LOCK TABLES `equipment_img` WRITE;
/*!40000 ALTER TABLE `equipment_img` DISABLE KEYS */;
INSERT INTO `equipment_img` VALUES (1,1,'image/upload_image/0001.jpg',1),(2,2,'image/upload_image/0002.jpg',1),(3,3,'image/upload_image/0003.jpg',1),(4,4,'image/upload_image/0004.jpg',1),(5,5,'image/upload_image/0005.jpg',1),(7,7,'image/upload_image/0007.jpg',1),(8,8,'image/upload_image/0008.jpg',1),(9,9,'image/upload_image/0009.jpg',1),(10,10,'image/upload_image/0010.jpg',1),(11,11,'image/upload_image/0011.jpg',1),(12,12,'image/upload_image/0012.jpg',1),(13,13,'image/upload_image/0013.jpg',1),(14,14,'image/upload_image/0014.jpg',1),(15,15,'image/upload_image/0015.jpg',1),(16,16,'image/upload_image/0016.jpg',1),(17,17,'image/upload_image/0017.jpg',1),(18,18,'image/upload_image/0018.jpg',1),(19,19,'image/upload_image/0019.jpg',1),(20,20,'image/upload_image/0020.jpg',1),(21,21,'image/upload_image/0021.jpg',1),(22,8,'image/upload_image/00082.jpg',0),(23,19,'image/upload_image/00192.jpg',0);
/*!40000 ALTER TABLE `equipment_img` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipment_instance`
--

DROP TABLE IF EXISTS `equipment_instance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipment_instance` (
  `instance_id` int NOT NULL AUTO_INCREMENT,
  `equipment_id` int NOT NULL,
  `instance_status` int DEFAULT NULL,
  PRIMARY KEY (`instance_id`),
  KEY `equipment_instance_equipment_equipment_id_fk` (`equipment_id`),
  KEY `equipment_instance_instance_status_instance_id_fk` (`instance_status`),
  CONSTRAINT `equipment_instance_ibfk_1` FOREIGN KEY (`equipment_id`) REFERENCES `equipment` (`equipment_id`),
  CONSTRAINT `equipment_instance_ibfk_2` FOREIGN KEY (`instance_status`) REFERENCES `instance_status` (`instance_id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipment_instance`
--

LOCK TABLES `equipment_instance` WRITE;
/*!40000 ALTER TABLE `equipment_instance` DISABLE KEYS */;
INSERT INTO `equipment_instance` VALUES (1,1,1),(2,1,1),(3,2,3),(4,2,2),(5,3,2),(6,3,2),(7,4,2),(8,4,2),(9,5,2),(10,5,2),(11,6,2),(12,6,2),(13,7,2),(14,7,2),(15,8,2),(16,8,2),(17,9,2),(18,9,2),(19,10,2),(20,10,1),(21,11,1),(22,11,2),(23,12,2),(24,12,1),(25,13,3),(26,13,2),(27,14,1),(28,14,1),(29,15,3),(30,15,3),(31,16,1),(32,16,1),(33,17,1),(34,17,1),(35,18,1),(36,18,1),(37,19,1),(38,19,1),(39,20,1),(40,20,1),(41,21,3),(42,21,3);
/*!40000 ALTER TABLE `equipment_instance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipment_maintenance`
--

DROP TABLE IF EXISTS `equipment_maintenance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipment_maintenance` (
  `maintenance_id` int NOT NULL AUTO_INCREMENT,
  `instance_id` int NOT NULL,
  `maintenance_start_date` date NOT NULL,
  `maintenance_end_date` date NOT NULL,
  `maintenance_type_id` int NOT NULL,
  `maintenance_status_id` int NOT NULL,
  `maintenance_cost` decimal(10,2) DEFAULT NULL,
  `notes` text,
  PRIMARY KEY (`maintenance_id`),
  KEY `maintenance_status_id` (`maintenance_status_id`),
  KEY `foreign_idx` (`instance_id`),
  KEY `foreign1_idx` (`maintenance_type_id`),
  CONSTRAINT `equipment_maintenance_ibfk_1` FOREIGN KEY (`maintenance_status_id`) REFERENCES `maintenance_status` (`maintenance_status_id`),
  CONSTRAINT `equipment_maintenance_ibfk_2` FOREIGN KEY (`maintenance_type_id`) REFERENCES `maintenance_type` (`maintenance_type_id`),
  CONSTRAINT `equipment_maintenance_ibfk_3` FOREIGN KEY (`instance_id`) REFERENCES `equipment_instance` (`instance_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipment_maintenance`
--

LOCK TABLES `equipment_maintenance` WRITE;
/*!40000 ALTER TABLE `equipment_maintenance` DISABLE KEYS */;
INSERT INTO `equipment_maintenance` VALUES (1,1,'2023-10-26','2023-11-02',2,1,300.00,'Haven\'t pay fee'),(2,2,'2023-10-27','2023-11-03',2,1,200.00,'$200, may cost more'),(3,16,'2023-09-30','2023-10-31',2,1,500.00,'$500 fee'),(4,41,'2023-11-01','2023-11-10',3,1,50.00,NULL),(5,42,'2023-11-01','2023-11-10',3,1,50.00,NULL),(7,29,'2023-11-02','2023-11-03',1,1,100.00,NULL),(8,30,'2023-11-02','2023-11-03',1,1,100.00,NULL);
/*!40000 ALTER TABLE `equipment_maintenance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipment_rental_status`
--

DROP TABLE IF EXISTS `equipment_rental_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipment_rental_status` (
  `equipment_rental_status_id` int NOT NULL AUTO_INCREMENT,
  `instance_id` int NOT NULL,
  `customer_id` int NOT NULL,
  `rental_start_datetime` datetime NOT NULL,
  `expected_return_datetime` datetime DEFAULT NULL,
  `actual_return_datetime` datetime DEFAULT NULL,
  `rental_status_id` int NOT NULL,
  `notes` text,
  PRIMARY KEY (`equipment_rental_status_id`),
  KEY `customer_id` (`customer_id`),
  KEY `instance_id` (`instance_id`),
  KEY `rental_status_id` (`rental_status_id`),
  CONSTRAINT `equipment_rental_status_ibfk_1` FOREIGN KEY (`instance_id`) REFERENCES `equipment_instance` (`instance_id`),
  CONSTRAINT `equipment_rental_status_ibfk_2` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`),
  CONSTRAINT `equipment_rental_status_ibfk_3` FOREIGN KEY (`rental_status_id`) REFERENCES `rental_status` (`rental_status_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipment_rental_status`
--

LOCK TABLES `equipment_rental_status` WRITE;
/*!40000 ALTER TABLE `equipment_rental_status` DISABLE KEYS */;
INSERT INTO `equipment_rental_status` VALUES (1,16,1,'2023-11-01 10:00:00','2023-11-01 19:00:00',NULL,1,'instance 16'),(2,21,1,'2023-11-01 12:00:00','2023-11-01 19:00:00',NULL,1,'instance 21'),(3,1,1,'2023-11-01 10:30:00','2023-11-01 19:00:00',NULL,1,'instance 1'),(4,16,1,'2023-11-02 10:00:00','2023-11-02 19:00:00',NULL,1,'instance 16'),(5,21,1,'2023-11-02 12:00:00','2023-11-02 19:00:00',NULL,1,'instance 21'),(6,1,1,'2023-11-02 10:30:00','2023-11-02 19:00:00',NULL,1,'instance 1'),(7,39,1,'2023-11-01 14:00:00','2023-11-02 10:00:00',NULL,1,NULL),(8,40,1,'2023-11-01 15:50:00','2023-11-02 10:00:00',NULL,1,NULL),(9,39,1,'2023-11-02 14:00:00','2023-11-03 10:00:00',NULL,1,NULL),(10,40,1,'2023-11-02 15:50:00','2023-11-03 10:00:00',NULL,1,NULL),(11,16,1,'2023-10-01 10:00:00','2023-10-01 19:00:00',NULL,1,NULL),(12,21,1,'2023-10-01 12:00:00','2023-10-01 19:00:00',NULL,1,NULL),(13,1,1,'2023-10-01 10:30:00','2023-10-01 19:00:00',NULL,1,NULL),(14,16,1,'2023-12-01 10:30:00','2023-12-01 19:00:00',NULL,1,NULL),(17,19,1,'2023-11-02 07:00:00','2023-11-07 07:00:00',NULL,2,NULL);
/*!40000 ALTER TABLE `equipment_rental_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipment_status`
--

DROP TABLE IF EXISTS `equipment_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipment_status` (
  `equipment_status_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`equipment_status_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipment_status`
--

LOCK TABLES `equipment_status` WRITE;
/*!40000 ALTER TABLE `equipment_status` DISABLE KEYS */;
INSERT INTO `equipment_status` VALUES (1,'Hired'),(2,'Returned'),(3,'Terminated');
/*!40000 ALTER TABLE `equipment_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hire_item`
--

DROP TABLE IF EXISTS `hire_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hire_item` (
  `hire_item_id` int NOT NULL AUTO_INCREMENT,
  `hire_id` int NOT NULL,
  `instance_id` int NOT NULL,
  `count` int DEFAULT '1',
  `price` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`hire_item_id`),
  KEY `foreign1_idx` (`hire_id`),
  KEY `foreign5_idx` (`instance_id`),
  CONSTRAINT `hire_item_ibfk_1` FOREIGN KEY (`instance_id`) REFERENCES `equipment_instance` (`instance_id`),
  CONSTRAINT `hire_item_ibfk_2` FOREIGN KEY (`hire_id`) REFERENCES `hire_list` (`hire_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hire_item`
--

LOCK TABLES `hire_item` WRITE;
/*!40000 ALTER TABLE `hire_item` DISABLE KEYS */;
INSERT INTO `hire_item` VALUES (4,4,16,1,50.00),(5,5,21,1,40.00),(6,6,1,1,30.00),(7,5,2,1,20.00),(9,9,19,1,432.00),(10,10,20,1,504.00),(14,15,19,1,360.00);
/*!40000 ALTER TABLE `hire_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hire_list`
--

DROP TABLE IF EXISTS `hire_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hire_list` (
  `hire_id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `status_id` int NOT NULL,
  `datetime` datetime NOT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`hire_id`),
  KEY `customer_id` (`customer_id`),
  KEY `status_id` (`status_id`),
  CONSTRAINT `hire_list_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`),
  CONSTRAINT `hire_list_ibfk_2` FOREIGN KEY (`status_id`) REFERENCES `hire_status` (`status_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hire_list`
--

LOCK TABLES `hire_list` WRITE;
/*!40000 ALTER TABLE `hire_list` DISABLE KEYS */;
INSERT INTO `hire_list` VALUES (4,1,3,'2023-10-06 06:00:00',100.00),(5,1,3,'2023-10-16 07:00:00',50.00),(6,1,3,'2023-10-16 07:00:00',200.00),(7,1,3,'2023-10-26 16:08:29',141.00),(8,1,3,'2023-10-26 22:05:50',0.00),(9,1,3,'2023-10-27 01:57:47',432.00),(10,1,3,'2023-10-27 01:58:51',504.00),(14,1,3,'2023-11-01 17:18:34',360.00),(15,1,3,'2023-11-01 17:18:59',360.00);
/*!40000 ALTER TABLE `hire_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hire_log`
--

DROP TABLE IF EXISTS `hire_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hire_log` (
  `log_id` int NOT NULL AUTO_INCREMENT,
  `staff_id` int NOT NULL,
  `datetime` datetime NOT NULL,
  `equipment_status_id` int NOT NULL,
  `message` text,
  `equipment_id` int NOT NULL,
  PRIMARY KEY (`log_id`),
  KEY `staff_id` (`staff_id`),
  KEY `event_type_id` (`equipment_status_id`),
  KEY `hire_log_ibfk_3` (`equipment_id`),
  CONSTRAINT `hire_log_ibfk_1` FOREIGN KEY (`staff_id`) REFERENCES `staff` (`staff_id`),
  CONSTRAINT `hire_log_ibfk_2` FOREIGN KEY (`equipment_status_id`) REFERENCES `equipment_status` (`equipment_status_id`),
  CONSTRAINT `hire_log_ibfk_3` FOREIGN KEY (`equipment_id`) REFERENCES `equipment` (`equipment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hire_log`
--

LOCK TABLES `hire_log` WRITE;
/*!40000 ALTER TABLE `hire_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `hire_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hire_status`
--

DROP TABLE IF EXISTS `hire_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hire_status` (
  `status_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`status_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hire_status`
--

LOCK TABLES `hire_status` WRITE;
/*!40000 ALTER TABLE `hire_status` DISABLE KEYS */;
INSERT INTO `hire_status` VALUES (1,'pending'),(2,'shipped'),(3,'completed'),(4,'cancelled');
/*!40000 ALTER TABLE `hire_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `instance_status`
--

DROP TABLE IF EXISTS `instance_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `instance_status` (
  `instance_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`instance_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `instance_status`
--

LOCK TABLES `instance_status` WRITE;
/*!40000 ALTER TABLE `instance_status` DISABLE KEYS */;
INSERT INTO `instance_status` VALUES (1,'Available'),(2,'Hired'),(3,'Maintenance'),(4,'Terminated');
/*!40000 ALTER TABLE `instance_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maintenance_status`
--

DROP TABLE IF EXISTS `maintenance_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maintenance_status` (
  `maintenance_status_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`maintenance_status_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maintenance_status`
--

LOCK TABLES `maintenance_status` WRITE;
/*!40000 ALTER TABLE `maintenance_status` DISABLE KEYS */;
INSERT INTO `maintenance_status` VALUES (1,'Pending'),(2,'Overdue'),(3,'Completed');
/*!40000 ALTER TABLE `maintenance_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maintenance_type`
--

DROP TABLE IF EXISTS `maintenance_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maintenance_type` (
  `maintenance_type_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`maintenance_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maintenance_type`
--

LOCK TABLES `maintenance_type` WRITE;
/*!40000 ALTER TABLE `maintenance_type` DISABLE KEYS */;
INSERT INTO `maintenance_type` VALUES (1,'Routine Check'),(2,'Repair'),(3,'Annual Inspection');
/*!40000 ALTER TABLE `maintenance_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `news`
--

DROP TABLE IF EXISTS `news`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `news` (
  `news_id` int NOT NULL AUTO_INCREMENT,
  `news` text,
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`news_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `news`
--

LOCK TABLES `news` WRITE;
/*!40000 ALTER TABLE `news` DISABLE KEYS */;
/*!40000 ALTER TABLE `news` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment` (
  `payment_id` int NOT NULL AUTO_INCREMENT,
  `hire_id` int NOT NULL,
  `status_id` int NOT NULL,
  `payment_type_id` int NOT NULL,
  `datetime` datetime NOT NULL,
  PRIMARY KEY (`payment_id`),
  KEY `status_id` (`status_id`),
  KEY `payment_type_id` (`payment_type_id`),
  KEY `hire_id` (`hire_id`),
  CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`hire_id`) REFERENCES `hire_list` (`hire_id`),
  CONSTRAINT `payment_ibfk_2` FOREIGN KEY (`status_id`) REFERENCES `payment_status` (`status_id`),
  CONSTRAINT `payment_ibfk_3` FOREIGN KEY (`payment_type_id`) REFERENCES `payment_type` (`payment_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` VALUES (1,4,1,1,'2023-10-18 07:00:00'),(2,5,1,2,'2023-10-01 07:00:00'),(3,6,1,3,'2023-09-30 07:00:00'),(4,7,1,3,'2023-10-26 16:08:30'),(5,8,1,2,'2023-10-26 22:05:52'),(6,9,1,1,'2023-10-27 01:57:48'),(7,10,1,1,'2023-10-27 01:58:53'),(8,5,1,3,'2023-10-27 11:17:59'),(9,5,1,1,'2023-10-27 11:23:05'),(10,5,1,1,'2023-10-27 12:10:42'),(11,6,1,1,'2023-10-27 12:13:46'),(12,6,1,2,'2023-10-27 15:20:59'),(17,15,1,1,'2023-11-01 17:18:59');
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_status`
--

DROP TABLE IF EXISTS `payment_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_status` (
  `status_id` int NOT NULL AUTO_INCREMENT,
  `status_name` varchar(255) NOT NULL,
  PRIMARY KEY (`status_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_status`
--

LOCK TABLES `payment_status` WRITE;
/*!40000 ALTER TABLE `payment_status` DISABLE KEYS */;
INSERT INTO `payment_status` VALUES (1,'Successful'),(2,'Pending'),(3,'Failed');
/*!40000 ALTER TABLE `payment_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_type`
--

DROP TABLE IF EXISTS `payment_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_type` (
  `payment_type_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`payment_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_type`
--

LOCK TABLES `payment_type` WRITE;
/*!40000 ALTER TABLE `payment_type` DISABLE KEYS */;
INSERT INTO `payment_type` VALUES (1,'Paypal'),(2,'Master Card'),(3,'Credit');
/*!40000 ALTER TABLE `payment_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `region`
--

DROP TABLE IF EXISTS `region`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `region` (
  `region_id` int NOT NULL AUTO_INCREMENT,
  `region` varchar(255) NOT NULL,
  PRIMARY KEY (`region_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `region`
--

LOCK TABLES `region` WRITE;
/*!40000 ALTER TABLE `region` DISABLE KEYS */;
INSERT INTO `region` VALUES (1,'Northland'),(2,'Auckland'),(3,'Waikato'),(4,'Bay Of Plenty'),(5,'Gisborne'),(6,'Hawke\'s Bay'),(7,'Taranaki'),(8,'Manawatu - Whanganui'),(9,'Wellington'),(10,'Nelson Bays'),(11,'Marlborough'),(12,'West Coast'),(13,'Canterbury'),(14,'Timaru - Oamaru'),(15,'Otago'),(16,'Southland');
/*!40000 ALTER TABLE `region` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rental_status`
--

DROP TABLE IF EXISTS `rental_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rental_status` (
  `rental_status_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`rental_status_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rental_status`
--

LOCK TABLES `rental_status` WRITE;
/*!40000 ALTER TABLE `rental_status` DISABLE KEYS */;
INSERT INTO `rental_status` VALUES (1,'Waiting For Pickup'),(2,'Rented Out'),(3,'Return On Time'),(4,'Overdue');
/*!40000 ALTER TABLE `rental_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `security_question`
--

DROP TABLE IF EXISTS `security_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `security_question` (
  `question_id` int NOT NULL AUTO_INCREMENT,
  `question` text NOT NULL,
  PRIMARY KEY (`question_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `security_question`
--

LOCK TABLES `security_question` WRITE;
/*!40000 ALTER TABLE `security_question` DISABLE KEYS */;
INSERT INTO `security_question` VALUES (1,'In which city were you born?'),(2,'What is your favorite book?'),(3,'What is the name of your best friend from childhood?'),(4,'What is the name of your favorite movie?'),(5,'What was the street you grew up on?');
/*!40000 ALTER TABLE `security_question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shopping_cart_item`
--

DROP TABLE IF EXISTS `shopping_cart_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shopping_cart_item` (
  `cart_item_id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `equipment_id` int NOT NULL,
  `count` int NOT NULL DEFAULT '1',
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  PRIMARY KEY (`cart_item_id`),
  KEY `product_id` (`equipment_id`),
  KEY `shopping_cart_item_customer_customer_id_fk` (`customer_id`),
  CONSTRAINT `shopping_cart_item_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`),
  CONSTRAINT `shopping_cart_item_ibfk_2` FOREIGN KEY (`equipment_id`) REFERENCES `equipment` (`equipment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shopping_cart_item`
--

LOCK TABLES `shopping_cart_item` WRITE;
/*!40000 ALTER TABLE `shopping_cart_item` DISABLE KEYS */;
INSERT INTO `shopping_cart_item` VALUES (1,1,4,1,'2023-10-28 00:00:00','2023-10-29 00:00:00');
/*!40000 ALTER TABLE `shopping_cart_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff` (
  `staff_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `username` varchar(100) DEFAULT NULL,
  `title_id` int NOT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `phone_number` varchar(255) DEFAULT NULL,
  `state` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`staff_id`),
  KEY `user_id` (`user_id`),
  KEY `title_id` (`title_id`),
  CONSTRAINT `staff_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_account` (`user_id`),
  CONSTRAINT `staff_ibfk_2` FOREIGN KEY (`title_id`) REFERENCES `title` (`title_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
INSERT INTO `staff` VALUES (1,2,'staff',1,'Leon','Kennedy','020001111',1),(2,10,NULL,2,'Alex','Ting','021526000',1),(3,11,NULL,2,'Jenny','Wong','021526888',1),(4,12,NULL,1,'Jeffery','Ngu','0211234567',1),(5,13,NULL,1,'Pauline','Tian','0219876543',1);
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sub_category`
--

DROP TABLE IF EXISTS `sub_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sub_category` (
  `sub_id` int NOT NULL AUTO_INCREMENT,
  `category_id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`sub_id`),
  UNIQUE KEY `name` (`name`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `sub_category_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sub_category`
--

LOCK TABLES `sub_category` WRITE;
/*!40000 ALTER TABLE `sub_category` DISABLE KEYS */;
INSERT INTO `sub_category` VALUES (1,1,'Lawn-Mowers'),(2,1,'Post-Hole-Borers'),(3,1,'Leaf-Blowers'),(4,2,'Furniture-Trailers'),(5,2,'Cage-High-Side-Trailers'),(6,2,'Chiller-Trailers'),(7,3,'Dumper'),(8,3,'Tractor-Graders'),(9,3,'Mini-Excavators-Diggers'),(10,4,'Saws'),(11,4,'Drills'),(12,4,'Staplers-&-Nailers'),(13,5,'Measuring-&-Survey'),(14,5,'Screw-Drivers');
/*!40000 ALTER TABLE `sub_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `title`
--

DROP TABLE IF EXISTS `title`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `title` (
  `title_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  PRIMARY KEY (`title_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `title`
--

LOCK TABLES `title` WRITE;
/*!40000 ALTER TABLE `title` DISABLE KEYS */;
INSERT INTO `title` VALUES (1,'Mr.'),(2,'Ms.'),(3,'Mrs.');
/*!40000 ALTER TABLE `title` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_account`
--

DROP TABLE IF EXISTS `user_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_account` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `is_customer` tinyint(1) NOT NULL DEFAULT '0',
  `is_staff` tinyint(1) NOT NULL DEFAULT '0',
  `is_admin` tinyint(1) NOT NULL DEFAULT '0',
  `register_date` date NOT NULL,
  `last_login_date` date NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_account`
--

LOCK TABLES `user_account` WRITE;
/*!40000 ALTER TABLE `user_account` DISABLE KEYS */;
INSERT INTO `user_account` VALUES (1,'admin@hire.com','$2b$12$OEYeiJb5Vz.BjAeGPDUcQe3YPESrG4/S./hoszazQuXEGsO4XurUG',0,0,1,'2023-09-25','2023-11-01'),(2,'staff@hire.com','$2b$12$OEYeiJb5Vz.BjAeGPDUcQe3YPESrG4/S./hoszazQuXEGsO4XurUG',0,1,0,'2023-09-25','2023-11-01'),(3,'customer@hire.com','$2b$12$OEYeiJb5Vz.BjAeGPDUcQe3YPESrG4/S./hoszazQuXEGsO4XurUG',1,0,0,'2023-09-27','2023-11-01'),(4,'nickyting222@gmail.com','$2b$12$sAqb65tDCsDn7ZjKAMNHgu5MbDLTAXyXCCFky1yQSyu7kV8iR5ZC2',1,0,0,'2023-11-01','2023-11-01'),(6,'johnting220@email.com','$2b$12$QN7o/Zgxzt4VhwXHTSes1.FjAp8LTMrfB5tEx45sd9rSiz0Bahl6S',1,0,0,'2023-11-01','2023-11-01'),(7,'beatricelim314@email.com','$2b$12$e0k.Uu7Ey0mN7.D3E4GdseNFdCJa.Ppv9nqr3c15TMfc7lNtZUd2a',1,0,0,'2023-11-01','2023-11-01'),(8,'emilyting1111@email.com','$2b$12$GkS73EXe6rN1VH3D95X6eeXRfGCxfMFbkTq9Sleub6LrnkyEARxrm',1,0,0,'2023-11-01','2023-11-01'),(9,'adrianngu1033@email.com','$2b$12$J3U/WpMYZTGGYVbBskyujO3aN5omb3NLR0Ze1xGxejNsJ3UrCZSEO',1,0,0,'2023-11-01','2023-11-01'),(10,'alexting614@email.com','$2b$12$fvWsXfuhtpBQmEDYNifxL.he8wWVZTFH5tcJDMxSJ1x8NfKpuBywu',0,1,0,'2023-11-01','2023-11-01'),(11,'jennywong555@email.com','$2b$12$2ReKAlYXlBQCe6S.s9zeKOfi10IjyLepiZy5qY8/xzr4yxt8hTYa2',0,1,0,'2023-11-01','2023-11-01'),(12,'jeffreyngu@email.com','$2b$12$e25cv7qNfkymXT5OZVD90.U9wPjCcJkP4/q.n6FKe7O4EqhQz7bTe',0,1,0,'2023-11-01','2023-11-01'),(13,'paulinetian@email.com','$2b$12$seLYaGmKoxthtATgVnzwPudwxNMQbt9UQGOu/2McTZfEuNRrdIklG',0,1,0,'2023-11-01','2023-11-01');
/*!40000 ALTER TABLE `user_account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wishlist`
--

DROP TABLE IF EXISTS `wishlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wishlist` (
  `wishlist_id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `equipment_id` int NOT NULL,
  PRIMARY KEY (`wishlist_id`),
  KEY `wishlist_customer_customer_id_fk` (`customer_id`),
  KEY `wishlist_equipment_equipment_id_fk` (`equipment_id`),
  CONSTRAINT `wishlist_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`),
  CONSTRAINT `wishlist_ibfk_2` FOREIGN KEY (`equipment_id`) REFERENCES `equipment` (`equipment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wishlist`
--

LOCK TABLES `wishlist` WRITE;
/*!40000 ALTER TABLE `wishlist` DISABLE KEYS */;
INSERT INTO `wishlist` VALUES (1,1,13),(2,1,14),(3,1,19);
/*!40000 ALTER TABLE `wishlist` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-01 17:41:10
