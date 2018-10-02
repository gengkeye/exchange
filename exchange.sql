-- MySQL dump 10.14  Distrib 5.5.56-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: exchange
-- ------------------------------------------------------
-- Server version	5.5.56-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `exchange`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `exchange` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `exchange`;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add bid',7,'add_bid'),(20,'Can change bid',7,'change_bid'),(21,'Can delete bid',7,'delete_bid'),(22,'Can add tele balance history',8,'add_telebalancehistory'),(23,'Can change tele balance history',8,'change_telebalancehistory'),(24,'Can delete tele balance history',8,'delete_telebalancehistory'),(25,'Can add tele group',9,'add_telegroup'),(26,'Can change tele group',9,'change_telegroup'),(27,'Can delete tele group',9,'delete_telegroup'),(28,'Can add tele image',10,'add_teleimage'),(29,'Can change tele image',10,'change_teleimage'),(30,'Can delete tele image',10,'delete_teleimage'),(31,'Can add tele membership',11,'add_telemembership'),(32,'Can change tele membership',11,'change_telemembership'),(33,'Can delete tele membership',11,'delete_telemembership'),(34,'Can add tele order',12,'add_teleorder'),(35,'Can change tele order',12,'change_teleorder'),(36,'Can delete tele order',12,'delete_teleorder'),(37,'Can add tele order item',13,'add_teleorderitem'),(38,'Can change tele order item',13,'change_teleorderitem'),(39,'Can delete tele order item',13,'delete_teleorderitem'),(40,'Can add tele price policy',14,'add_telepricepolicy'),(41,'Can change tele price policy',14,'change_telepricepolicy'),(42,'Can delete tele price policy',14,'delete_telepricepolicy'),(43,'Can add tele product',15,'add_teleproduct'),(44,'Can change tele product',15,'change_teleproduct'),(45,'Can delete tele product',15,'delete_teleproduct'),(46,'Can add tele store',16,'add_telestore'),(47,'Can change tele store',16,'change_telestore'),(48,'Can delete tele store',16,'delete_telestore'),(49,'Can add tele user',17,'add_teleuser'),(50,'Can change tele user',17,'change_teleuser'),(51,'Can delete tele user',17,'delete_teleuser');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(7,'exchange','bid'),(8,'exchange','telebalancehistory'),(9,'exchange','telegroup'),(10,'exchange','teleimage'),(11,'exchange','telemembership'),(12,'exchange','teleorder'),(13,'exchange','teleorderitem'),(14,'exchange','telepricepolicy'),(15,'exchange','teleproduct'),(16,'exchange','telestore'),(17,'exchange','teleuser'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2018-09-20 14:56:22'),(2,'auth','0001_initial','2018-09-20 14:56:24'),(3,'admin','0001_initial','2018-09-20 14:56:24'),(4,'admin','0002_logentry_remove_auto_add','2018-09-20 14:56:24'),(5,'contenttypes','0002_remove_content_type_name','2018-09-20 14:56:24'),(6,'auth','0002_alter_permission_name_max_length','2018-09-20 14:56:24'),(7,'auth','0003_alter_user_email_max_length','2018-09-20 14:56:24'),(8,'auth','0004_alter_user_username_opts','2018-09-20 14:56:24'),(9,'auth','0005_alter_user_last_login_null','2018-09-20 14:56:25'),(10,'auth','0006_require_contenttypes_0002','2018-09-20 14:56:25'),(11,'auth','0007_alter_validators_add_error_messages','2018-09-20 14:56:25'),(12,'auth','0008_alter_user_username_max_length','2018-09-20 14:56:25'),(13,'exchange','0001_initial','2018-09-20 14:56:29'),(14,'sessions','0001_initial','2018-09-20 14:56:29'),(15,'exchange','0002_auto_20180920_1524','2018-09-20 15:24:22'),(16,'exchange','0003_auto_20180923_1804','2018-09-23 18:04:30'),(17,'exchange','0004_teleuser_short_name','2018-09-25 17:56:30'),(18,'exchange','0005_auto_20180925_1908','2018-09-25 19:08:42');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exchange_bid`
--

DROP TABLE IF EXISTS `exchange_bid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exchange_bid` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sell_currency` varchar(30) NOT NULL,
  `buy_currency` varchar(30) NOT NULL,
  `max_amount` int(10) unsigned NOT NULL,
  `min_amount` int(10) unsigned NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `date_created` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `exchange_bid_user_id_a25a3551_fk_exchange_teleuser_id` (`user_id`),
  CONSTRAINT `exchange_bid_user_id_a25a3551_fk_exchange_teleuser_id` FOREIGN KEY (`user_id`) REFERENCES `exchange_teleuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exchange_bid`
--

LOCK TABLES `exchange_bid` WRITE;
/*!40000 ALTER TABLE `exchange_bid` DISABLE KEYS */;
INSERT INTO `exchange_bid` VALUES (1,'USD','CNY',1000000,10000,6.90,'2018-09-22 19:24:04',1),(2,'USD','PHP',10000,10000,54.00,'2018-09-22 19:24:04',4),(3,'PHP','CNY',500000,50000,7.70,'2018-09-22 19:24:04',3),(4,'CNY','PHP',100000,10000,7.65,'2018-09-22 19:24:04',1),(5,'PHP','CNY',500000,50000,7.83,'2018-09-22 19:24:04',4),(6,'CNY','PHP',1000,0,9.90,'2018-09-23 16:52:35',3),(7,'CNY','USD',22222,0,6.89,'2018-09-23 16:54:42',4),(8,'USD','PHP',777,0,54.00,'2018-09-23 17:21:31',1),(9,'CNY','PHP',1999,0,1.00,'2018-09-23 17:26:04',5);
/*!40000 ALTER TABLE `exchange_bid` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exchange_telegroup`
--

DROP TABLE IF EXISTS `exchange_telegroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exchange_telegroup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(20) DEFAULT NULL,
  `chat_id` varchar(20) DEFAULT NULL,
  `address` varchar(100) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `remarks` varchar(100) NOT NULL,
  `driver_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  UNIQUE KEY `chat_id` (`chat_id`),
  KEY `exchange_telegroup_driver_id_220e6158_fk_exchange_teleuser_id` (`driver_id`),
  CONSTRAINT `exchange_telegroup_driver_id_220e6158_fk_exchange_teleuser_id` FOREIGN KEY (`driver_id`) REFERENCES `exchange_teleuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exchange_telegroup`
--

LOCK TABLES `exchange_telegroup` WRITE;
/*!40000 ALTER TABLE `exchange_telegroup` DISABLE KEYS */;
/*!40000 ALTER TABLE `exchange_telegroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exchange_telegroup_images`
--

DROP TABLE IF EXISTS `exchange_telegroup_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exchange_telegroup_images` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `telegroup_id` int(11) NOT NULL,
  `teleimage_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `exchange_telegroup_image_telegroup_id_teleimage_i_853095e5_uniq` (`telegroup_id`,`teleimage_id`),
  KEY `exchange_telegroup_i_teleimage_id_a9ba6653_fk_exchange_` (`teleimage_id`),
  CONSTRAINT `exchange_telegroup_i_telegroup_id_fac444a4_fk_exchange_` FOREIGN KEY (`telegroup_id`) REFERENCES `exchange_telegroup` (`id`),
  CONSTRAINT `exchange_telegroup_i_teleimage_id_a9ba6653_fk_exchange_` FOREIGN KEY (`teleimage_id`) REFERENCES `exchange_teleimage` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exchange_telegroup_images`
--

LOCK TABLES `exchange_telegroup_images` WRITE;
/*!40000 ALTER TABLE `exchange_telegroup_images` DISABLE KEYS */;
/*!40000 ALTER TABLE `exchange_telegroup_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exchange_telegroup_managers`
--

DROP TABLE IF EXISTS `exchange_telegroup_managers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exchange_telegroup_managers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `telegroup_id` int(11) NOT NULL,
  `teleuser_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `exchange_telegroup_manag_telegroup_id_teleuser_id_d44f36fa_uniq` (`telegroup_id`,`teleuser_id`),
  KEY `exchange_telegroup_m_teleuser_id_931be4a3_fk_exchange_` (`teleuser_id`),
  CONSTRAINT `exchange_telegroup_m_telegroup_id_70f707cf_fk_exchange_` FOREIGN KEY (`telegroup_id`) REFERENCES `exchange_telegroup` (`id`),
  CONSTRAINT `exchange_telegroup_m_teleuser_id_931be4a3_fk_exchange_` FOREIGN KEY (`teleuser_id`) REFERENCES `exchange_teleuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exchange_telegroup_managers`
--

LOCK TABLES `exchange_telegroup_managers` WRITE;
/*!40000 ALTER TABLE `exchange_telegroup_managers` DISABLE KEYS */;
/*!40000 ALTER TABLE `exchange_telegroup_managers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exchange_teleimage`
--

DROP TABLE IF EXISTS `exchange_teleimage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exchange_teleimage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `image_id` varchar(100) NOT NULL,
  `purpose` varchar(20) NOT NULL,
  `from_user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `image_id` (`image_id`),
  KEY `exchange_teleimage_from_user_id_dda969be_fk_exchange_teleuser_id` (`from_user_id`),
  CONSTRAINT `exchange_teleimage_from_user_id_dda969be_fk_exchange_teleuser_id` FOREIGN KEY (`from_user_id`) REFERENCES `exchange_teleuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exchange_teleimage`
--

LOCK TABLES `exchange_teleimage` WRITE;
/*!40000 ALTER TABLE `exchange_teleimage` DISABLE KEYS */;
/*!40000 ALTER TABLE `exchange_teleimage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exchange_telemembership`
--

DROP TABLE IF EXISTS `exchange_telemembership`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exchange_telemembership` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `balance` decimal(12,2) NOT NULL,
  `subscribed` tinyint(1) NOT NULL,
  `group_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `exchange_telemembers_group_id_f3abd435_fk_exchange_` (`group_id`),
  KEY `exchange_telemembership_user_id_e107bd05_fk_exchange_teleuser_id` (`user_id`),
  CONSTRAINT `exchange_telemembership_user_id_e107bd05_fk_exchange_teleuser_id` FOREIGN KEY (`user_id`) REFERENCES `exchange_teleuser` (`id`),
  CONSTRAINT `exchange_telemembers_group_id_f3abd435_fk_exchange_` FOREIGN KEY (`group_id`) REFERENCES `exchange_telegroup` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exchange_telemembership`
--

LOCK TABLES `exchange_telemembership` WRITE;
/*!40000 ALTER TABLE `exchange_telemembership` DISABLE KEYS */;
/*!40000 ALTER TABLE `exchange_telemembership` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exchange_teleuser`
--

DROP TABLE IF EXISTS `exchange_teleuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exchange_teleuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `chat_id` varchar(20) DEFAULT NULL,
  `name` varchar(20) DEFAULT NULL,
  `username` varchar(20) DEFAULT NULL,
  `role` varchar(20) NOT NULL,
  `credit_level` varchar(20) NOT NULL,
  `date_created` datetime NOT NULL,
  `short_name` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `chat_id` (`chat_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `short_name` (`short_name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exchange_teleuser`
--

LOCK TABLES `exchange_teleuser` WRITE;
/*!40000 ALTER TABLE `exchange_teleuser` DISABLE KEYS */;
INSERT INTO `exchange_teleuser` VALUES (1,'357468958','oldseven','seven_old','User','A','2018-09-23 18:04:30','oldseven'),(3,'357468959','安安','annwith','User','AAA','2018-09-25 18:43:04','安安'),(4,'357468952','马云','Jackma','User','AA','2018-09-25 18:44:10','马云'),(5,'357468953','刘强东','QiangdongLiu','User','AAA','2018-09-25 18:44:41','刘强东'),(7,'357468954','王健林','JianlinWang','User','AA','2018-09-25 18:45:31','王健林');
/*!40000 ALTER TABLE `exchange_teleuser` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-09-26 17:32:43
