/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1
Source Server Version : 50717
Source Host           : localhost:3306
Source Database       : chatbot_cn

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2019-05-14 14:50:54
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for authdata_user
-- ----------------------------
DROP TABLE IF EXISTS `authdata_user`;
CREATE TABLE `authdata_user` (
  `id` int(11) NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `last_login` timestamp NULL DEFAULT NULL,
  `is_superuser` int(11) DEFAULT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `is_staff` int(11) DEFAULT NULL,
  `is_active` int(11) DEFAULT NULL,
  `date_joined` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `usernames` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of authdata_user
-- ----------------------------
INSERT INTO `authdata_user` VALUES ('0', 'admin', 'pbkdf2_sha256$120000$5AJjaLNVNYeu$9mewBJOFA8B0GV794GhjH/ezpW3cARU4y10NB1c8ujQ=', '2019-05-13 06:21:05', '0', '', '', '0', '1', '2019-05-13 14:21:05', '', 'charlesxu86@163.com');
