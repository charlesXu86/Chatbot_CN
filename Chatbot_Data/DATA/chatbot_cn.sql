/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1
Source Server Version : 50717
Source Host           : localhost:3306
Source Database       : chatbot_cn

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2019-05-29 08:50:31
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
INSERT INTO `authdata_user` VALUES ('0', 'admin', 'pbkdf2_sha256$120000$5AJjaLNVNYeu$9mewBJOFA8B0GV794GhjH/ezpW3cARU4y10NB1c8ujQ=', '2019-05-18 09:26:45', '0', '', '', '0', '1', '2019-05-18 17:26:44', '', 'charlesxu86@163.com');

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES ('1', 'Can add log entry', '1', 'add_logentry');
INSERT INTO `auth_permission` VALUES ('2', 'Can change log entry', '1', 'change_logentry');
INSERT INTO `auth_permission` VALUES ('3', 'Can delete log entry', '1', 'delete_logentry');
INSERT INTO `auth_permission` VALUES ('4', 'Can view log entry', '1', 'view_logentry');
INSERT INTO `auth_permission` VALUES ('5', 'Can add permission', '2', 'add_permission');
INSERT INTO `auth_permission` VALUES ('6', 'Can change permission', '2', 'change_permission');
INSERT INTO `auth_permission` VALUES ('7', 'Can delete permission', '2', 'delete_permission');
INSERT INTO `auth_permission` VALUES ('8', 'Can view permission', '2', 'view_permission');
INSERT INTO `auth_permission` VALUES ('9', 'Can add group', '3', 'add_group');
INSERT INTO `auth_permission` VALUES ('10', 'Can change group', '3', 'change_group');
INSERT INTO `auth_permission` VALUES ('11', 'Can delete group', '3', 'delete_group');
INSERT INTO `auth_permission` VALUES ('12', 'Can view group', '3', 'view_group');
INSERT INTO `auth_permission` VALUES ('13', 'Can add user', '4', 'add_user');
INSERT INTO `auth_permission` VALUES ('14', 'Can change user', '4', 'change_user');
INSERT INTO `auth_permission` VALUES ('15', 'Can delete user', '4', 'delete_user');
INSERT INTO `auth_permission` VALUES ('16', 'Can view user', '4', 'view_user');
INSERT INTO `auth_permission` VALUES ('17', 'Can add content type', '5', 'add_contenttype');
INSERT INTO `auth_permission` VALUES ('18', 'Can change content type', '5', 'change_contenttype');
INSERT INTO `auth_permission` VALUES ('19', 'Can delete content type', '5', 'delete_contenttype');
INSERT INTO `auth_permission` VALUES ('20', 'Can view content type', '5', 'view_contenttype');
INSERT INTO `auth_permission` VALUES ('21', 'Can add session', '6', 'add_session');
INSERT INTO `auth_permission` VALUES ('22', 'Can change session', '6', 'change_session');
INSERT INTO `auth_permission` VALUES ('23', 'Can delete session', '6', 'delete_session');
INSERT INTO `auth_permission` VALUES ('24', 'Can view session', '6', 'view_session');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_user
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
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

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
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

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES ('1', 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES ('3', 'auth', 'group');
INSERT INTO `django_content_type` VALUES ('2', 'auth', 'permission');
INSERT INTO `django_content_type` VALUES ('4', 'auth', 'user');
INSERT INTO `django_content_type` VALUES ('5', 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES ('6', 'sessions', 'session');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES ('1', 'contenttypes', '0001_initial', '2018-08-04 02:44:12.886722');
INSERT INTO `django_migrations` VALUES ('2', 'auth', '0001_initial', '2018-08-04 02:44:30.682033');
INSERT INTO `django_migrations` VALUES ('3', 'admin', '0001_initial', '2018-08-04 02:44:34.018594');
INSERT INTO `django_migrations` VALUES ('4', 'admin', '0002_logentry_remove_auto_add', '2018-08-04 02:44:34.065474');
INSERT INTO `django_migrations` VALUES ('5', 'admin', '0003_logentry_add_action_flag_choices', '2018-08-04 02:44:34.237369');
INSERT INTO `django_migrations` VALUES ('6', 'contenttypes', '0002_remove_content_type_name', '2018-08-04 02:44:36.931336');
INSERT INTO `django_migrations` VALUES ('7', 'auth', '0002_alter_permission_name_max_length', '2018-08-04 02:44:37.900190');
INSERT INTO `django_migrations` VALUES ('8', 'auth', '0003_alter_user_email_max_length', '2018-08-04 02:44:39.371889');
INSERT INTO `django_migrations` VALUES ('9', 'auth', '0004_alter_user_username_opts', '2018-08-04 02:44:39.418738');
INSERT INTO `django_migrations` VALUES ('10', 'auth', '0005_alter_user_last_login_null', '2018-08-04 02:44:40.692908');
INSERT INTO `django_migrations` VALUES ('11', 'auth', '0006_require_contenttypes_0002', '2018-08-04 02:44:40.786806');
INSERT INTO `django_migrations` VALUES ('12', 'auth', '0007_alter_validators_add_error_messages', '2018-08-04 02:44:40.922836');
INSERT INTO `django_migrations` VALUES ('13', 'auth', '0008_alter_user_username_max_length', '2018-08-04 02:44:41.906310');
INSERT INTO `django_migrations` VALUES ('14', 'auth', '0009_alter_user_last_name_max_length', '2018-08-04 02:44:42.772986');
INSERT INTO `django_migrations` VALUES ('15', 'sessions', '0001_initial', '2018-08-04 02:44:43.387466');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO `django_session` VALUES ('3gqzmzged573vob82u6xebxmkhhvhy5n', 'Yzg2Y2E2ZDBlZjY0ZTk2NjFlMjNkZmUzZWNlZmJkNTI0YWFhYjRmMzp7Il9hdXRoX3VzZXJfaWQiOiIwIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3OWM4ZTI1NzA4MzZjZGMwOWU5OWI5YzIzMzFiY2E5YjVmZDExNDkzIn0=', '2019-02-09 11:53:56.034790');
INSERT INTO `django_session` VALUES ('3yd1t311jbmw9ptowapuck5pnkawa98z', 'Yzg2Y2E2ZDBlZjY0ZTk2NjFlMjNkZmUzZWNlZmJkNTI0YWFhYjRmMzp7Il9hdXRoX3VzZXJfaWQiOiIwIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3OWM4ZTI1NzA4MzZjZGMwOWU5OWI5YzIzMzFiY2E5YjVmZDExNDkzIn0=', '2019-02-08 09:48:41.143799');
INSERT INTO `django_session` VALUES ('64i0xg5tr7m9bji42rkwnhpya1d29sk6', 'Y2FmZTFjZGM2ZTYwYjQ5NWM2YmI5MjhmNWRjYzllMjFlNmMwZGI2Mjp7Il9hdXRoX3VzZXJfaGFzaCI6Ijc5YzhlMjU3MDgzNmNkYzA5ZTk5YjljMjMzMWJjYTliNWZkMTE0OTMiLCJfYXV0aF91c2VyX2lkIjoiMCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-02-11 02:44:26.762417');
INSERT INTO `django_session` VALUES ('6qdehlw9wl7ht22zpzytc5vet48o79jg', 'N2Y5MDg0OWFhZmRkYzJhNDVhZmVmYTk3OGQ5YWJiNTZjOTY4MDdjZTp7Il9hdXRoX3VzZXJfaWQiOiIwIiwiX2F1dGhfdXNlcl9oYXNoIjoiNzljOGUyNTcwODM2Y2RjMDllOTliOWMyMzMxYmNhOWI1ZmQxMTQ5MyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-05-22 09:01:00.041969');
INSERT INTO `django_session` VALUES ('945eex1hmntgwxik1gsk0szaxwccxx84', 'ODcwZjgzMTBjNDQxOGNjYTU5YWQ2N2FkYjBlODc3ZDBhMDE5YTI3Mjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNzljOGUyNTcwODM2Y2RjMDllOTliOWMyMzMxYmNhOWI1ZmQxMTQ5MyIsIl9hdXRoX3VzZXJfaWQiOiIwIn0=', '2019-02-10 01:34:25.317500');
INSERT INTO `django_session` VALUES ('9b7c6kudgw82s1s7nqpd6kp25c4m4uuy', 'ZDhhY2NlYjY0MDZmNDgzZDJjMjYyMWRkNjBkMWEzMWY2NjYzZTgwZjp7Il9hdXRoX3VzZXJfaGFzaCI6Ijc5YzhlMjU3MDgzNmNkYzA5ZTk5YjljMjMzMWJjYTliNWZkMTE0OTMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIwIn0=', '2019-02-12 00:34:33.465683');
INSERT INTO `django_session` VALUES ('bye4kt3lul87hs7pv8df1zhxl5vecx2f', 'ODcwZjgzMTBjNDQxOGNjYTU5YWQ2N2FkYjBlODc3ZDBhMDE5YTI3Mjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNzljOGUyNTcwODM2Y2RjMDllOTliOWMyMzMxYmNhOWI1ZmQxMTQ5MyIsIl9hdXRoX3VzZXJfaWQiOiIwIn0=', '2019-02-09 02:10:13.375929');
INSERT INTO `django_session` VALUES ('cnxefkk6dcd3y84l1qy6magstzw8r7bo', 'ZDhhY2NlYjY0MDZmNDgzZDJjMjYyMWRkNjBkMWEzMWY2NjYzZTgwZjp7Il9hdXRoX3VzZXJfaGFzaCI6Ijc5YzhlMjU3MDgzNmNkYzA5ZTk5YjljMjMzMWJjYTliNWZkMTE0OTMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIwIn0=', '2019-05-30 02:21:47.909664');
INSERT INTO `django_session` VALUES ('d6v1ogs7ts5b8v2nw86q47gjk5otwadt', 'Y2FmZTFjZGM2ZTYwYjQ5NWM2YmI5MjhmNWRjYzllMjFlNmMwZGI2Mjp7Il9hdXRoX3VzZXJfaGFzaCI6Ijc5YzhlMjU3MDgzNmNkYzA5ZTk5YjljMjMzMWJjYTliNWZkMTE0OTMiLCJfYXV0aF91c2VyX2lkIjoiMCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-05-24 01:59:24.217454');
INSERT INTO `django_session` VALUES ('dv7p3hkp0jci65itrh7qjx2928cteuc0', 'Mjg1NzI0ZTkxYzQwZTIzZTE2NmM0N2NiYjU1N2UwZjY0MGY3NGI3Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjAiLCJfYXV0aF91c2VyX2hhc2giOiI3OWM4ZTI1NzA4MzZjZGMwOWU5OWI5YzIzMzFiY2E5YjVmZDExNDkzIn0=', '2019-05-27 06:21:05.555832');
INSERT INTO `django_session` VALUES ('eln2t51ab5xt773xgg8ru8ts32103dey', 'N2Y5MDg0OWFhZmRkYzJhNDVhZmVmYTk3OGQ5YWJiNTZjOTY4MDdjZTp7Il9hdXRoX3VzZXJfaWQiOiIwIiwiX2F1dGhfdXNlcl9oYXNoIjoiNzljOGUyNTcwODM2Y2RjMDllOTliOWMyMzMxYmNhOWI1ZmQxMTQ5MyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-03-30 03:15:47.527128');
INSERT INTO `django_session` VALUES ('f790afmpmqefe5xxjshekj09voxgm6e7', 'ODcwZjgzMTBjNDQxOGNjYTU5YWQ2N2FkYjBlODc3ZDBhMDE5YTI3Mjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNzljOGUyNTcwODM2Y2RjMDllOTliOWMyMzMxYmNhOWI1ZmQxMTQ5MyIsIl9hdXRoX3VzZXJfaWQiOiIwIn0=', '2019-03-30 09:36:08.937921');
INSERT INTO `django_session` VALUES ('fzv3jtpcoig0l7f843sbtpix4yvib4ao', 'N2Y5MDg0OWFhZmRkYzJhNDVhZmVmYTk3OGQ5YWJiNTZjOTY4MDdjZTp7Il9hdXRoX3VzZXJfaWQiOiIwIiwiX2F1dGhfdXNlcl9oYXNoIjoiNzljOGUyNTcwODM2Y2RjMDllOTliOWMyMzMxYmNhOWI1ZmQxMTQ5MyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-02-11 02:28:28.513989');
INSERT INTO `django_session` VALUES ('gmtnbgj68j660ei9gciiimbmq51ah607', 'N2Y5MDg0OWFhZmRkYzJhNDVhZmVmYTk3OGQ5YWJiNTZjOTY4MDdjZTp7Il9hdXRoX3VzZXJfaWQiOiIwIiwiX2F1dGhfdXNlcl9oYXNoIjoiNzljOGUyNTcwODM2Y2RjMDllOTliOWMyMzMxYmNhOWI1ZmQxMTQ5MyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-05-21 01:22:25.072082');
INSERT INTO `django_session` VALUES ('izegvcxbio3usyt4q015cux9hn3nns44', 'ZDhhY2NlYjY0MDZmNDgzZDJjMjYyMWRkNjBkMWEzMWY2NjYzZTgwZjp7Il9hdXRoX3VzZXJfaGFzaCI6Ijc5YzhlMjU3MDgzNmNkYzA5ZTk5YjljMjMzMWJjYTliNWZkMTE0OTMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIwIn0=', '2019-05-29 03:04:23.893311');
INSERT INTO `django_session` VALUES ('laxrmo6joo4j5yat10db17c6d7plolmj', 'Mjg1NzI0ZTkxYzQwZTIzZTE2NmM0N2NiYjU1N2UwZjY0MGY3NGI3Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjAiLCJfYXV0aF91c2VyX2hhc2giOiI3OWM4ZTI1NzA4MzZjZGMwOWU5OWI5YzIzMzFiY2E5YjVmZDExNDkzIn0=', '2019-05-24 09:14:52.305842');
INSERT INTO `django_session` VALUES ('m3y24lc1tm9ccfqep3e2s64jz015as72', 'N2Y5MDg0OWFhZmRkYzJhNDVhZmVmYTk3OGQ5YWJiNTZjOTY4MDdjZTp7Il9hdXRoX3VzZXJfaWQiOiIwIiwiX2F1dGhfdXNlcl9oYXNoIjoiNzljOGUyNTcwODM2Y2RjMDllOTliOWMyMzMxYmNhOWI1ZmQxMTQ5MyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-02-12 06:51:59.520398');
INSERT INTO `django_session` VALUES ('obqs3u2bs402or9rlrsafj5uii2xtx3b', 'Y2FmZTFjZGM2ZTYwYjQ5NWM2YmI5MjhmNWRjYzllMjFlNmMwZGI2Mjp7Il9hdXRoX3VzZXJfaGFzaCI6Ijc5YzhlMjU3MDgzNmNkYzA5ZTk5YjljMjMzMWJjYTliNWZkMTE0OTMiLCJfYXV0aF91c2VyX2lkIjoiMCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-03-30 07:51:17.608433');
INSERT INTO `django_session` VALUES ('pjg086fljlugq5cwmxlzsifmjtl6y081', 'Mjg1NzI0ZTkxYzQwZTIzZTE2NmM0N2NiYjU1N2UwZjY0MGY3NGI3Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjAiLCJfYXV0aF91c2VyX2hhc2giOiI3OWM4ZTI1NzA4MzZjZGMwOWU5OWI5YzIzMzFiY2E5YjVmZDExNDkzIn0=', '2019-03-30 04:06:41.742184');
INSERT INTO `django_session` VALUES ('ptp91f9lstjwism51farr0mhcr79dlsf', 'Yzg2Y2E2ZDBlZjY0ZTk2NjFlMjNkZmUzZWNlZmJkNTI0YWFhYjRmMzp7Il9hdXRoX3VzZXJfaWQiOiIwIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3OWM4ZTI1NzA4MzZjZGMwOWU5OWI5YzIzMzFiY2E5YjVmZDExNDkzIn0=', '2019-03-07 11:36:47.528210');
INSERT INTO `django_session` VALUES ('ql0mge30g94rqvtea9xprn2iywwqvah8', 'N2Y5MDg0OWFhZmRkYzJhNDVhZmVmYTk3OGQ5YWJiNTZjOTY4MDdjZTp7Il9hdXRoX3VzZXJfaWQiOiIwIiwiX2F1dGhfdXNlcl9oYXNoIjoiNzljOGUyNTcwODM2Y2RjMDllOTliOWMyMzMxYmNhOWI1ZmQxMTQ5MyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-02-08 09:39:54.895164');
INSERT INTO `django_session` VALUES ('qufw91ir5isanrgj3riq2yodrub1qhv7', 'Y2FmZTFjZGM2ZTYwYjQ5NWM2YmI5MjhmNWRjYzllMjFlNmMwZGI2Mjp7Il9hdXRoX3VzZXJfaGFzaCI6Ijc5YzhlMjU3MDgzNmNkYzA5ZTk5YjljMjMzMWJjYTliNWZkMTE0OTMiLCJfYXV0aF91c2VyX2lkIjoiMCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-05-29 01:59:53.519712');
INSERT INTO `django_session` VALUES ('r3qp2gr2p9vnrvqeya64yqfxsnn4blis', 'Y2FmZTFjZGM2ZTYwYjQ5NWM2YmI5MjhmNWRjYzllMjFlNmMwZGI2Mjp7Il9hdXRoX3VzZXJfaGFzaCI6Ijc5YzhlMjU3MDgzNmNkYzA5ZTk5YjljMjMzMWJjYTliNWZkMTE0OTMiLCJfYXV0aF91c2VyX2lkIjoiMCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-05-29 03:06:38.888836');
INSERT INTO `django_session` VALUES ('sn0ngidf7qenwnvrc75izg1s0aia0xyx', 'Y2FmZTFjZGM2ZTYwYjQ5NWM2YmI5MjhmNWRjYzllMjFlNmMwZGI2Mjp7Il9hdXRoX3VzZXJfaGFzaCI6Ijc5YzhlMjU3MDgzNmNkYzA5ZTk5YjljMjMzMWJjYTliNWZkMTE0OTMiLCJfYXV0aF91c2VyX2lkIjoiMCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-06-01 06:38:42.185062');
INSERT INTO `django_session` VALUES ('t5e10vj5ljld4uybpbbvfim2thbjpry6', 'Y2FmZTFjZGM2ZTYwYjQ5NWM2YmI5MjhmNWRjYzllMjFlNmMwZGI2Mjp7Il9hdXRoX3VzZXJfaGFzaCI6Ijc5YzhlMjU3MDgzNmNkYzA5ZTk5YjljMjMzMWJjYTliNWZkMTE0OTMiLCJfYXV0aF91c2VyX2lkIjoiMCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-03-30 07:59:13.682405');
INSERT INTO `django_session` VALUES ('v3p53qgrsh2car2f29lbuynayy745awe', 'ODcwZjgzMTBjNDQxOGNjYTU5YWQ2N2FkYjBlODc3ZDBhMDE5YTI3Mjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNzljOGUyNTcwODM2Y2RjMDllOTliOWMyMzMxYmNhOWI1ZmQxMTQ5MyIsIl9hdXRoX3VzZXJfaWQiOiIwIn0=', '2019-03-28 03:45:49.240731');
INSERT INTO `django_session` VALUES ('wtfi60qqormqftbojdn0j4qa45hianq6', 'Mjg1NzI0ZTkxYzQwZTIzZTE2NmM0N2NiYjU1N2UwZjY0MGY3NGI3Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjAiLCJfYXV0aF91c2VyX2hhc2giOiI3OWM4ZTI1NzA4MzZjZGMwOWU5OWI5YzIzMzFiY2E5YjVmZDExNDkzIn0=', '2019-03-30 08:44:04.244337');
INSERT INTO `django_session` VALUES ('ymzkaih3wzhj2oyxcbwx96xubm86oakq', 'ODcwZjgzMTBjNDQxOGNjYTU5YWQ2N2FkYjBlODc3ZDBhMDE5YTI3Mjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNzljOGUyNTcwODM2Y2RjMDllOTliOWMyMzMxYmNhOWI1ZmQxMTQ5MyIsIl9hdXRoX3VzZXJfaWQiOiIwIn0=', '2019-05-22 06:09:06.251313');
INSERT INTO `django_session` VALUES ('ypw8h8zcnvsovlgxgybaud5i4xjwmmbi', 'ZDhhY2NlYjY0MDZmNDgzZDJjMjYyMWRkNjBkMWEzMWY2NjYzZTgwZjp7Il9hdXRoX3VzZXJfaGFzaCI6Ijc5YzhlMjU3MDgzNmNkYzA5ZTk5YjljMjMzMWJjYTliNWZkMTE0OTMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIwIn0=', '2019-03-30 06:31:00.158246');
INSERT INTO `django_session` VALUES ('z2qnjve6i5bocq5emi7dygoxcmbtb160', 'N2Y5MDg0OWFhZmRkYzJhNDVhZmVmYTk3OGQ5YWJiNTZjOTY4MDdjZTp7Il9hdXRoX3VzZXJfaWQiOiIwIiwiX2F1dGhfdXNlcl9oYXNoIjoiNzljOGUyNTcwODM2Y2RjMDllOTliOWMyMzMxYmNhOWI1ZmQxMTQ5MyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-06-01 09:26:44.899053');
INSERT INTO `django_session` VALUES ('z5j0mfv1gjsklogyud377v9olk8w0vh7', 'Y2FmZTFjZGM2ZTYwYjQ5NWM2YmI5MjhmNWRjYzllMjFlNmMwZGI2Mjp7Il9hdXRoX3VzZXJfaGFzaCI6Ijc5YzhlMjU3MDgzNmNkYzA5ZTk5YjljMjMzMWJjYTliNWZkMTE0OTMiLCJfYXV0aF91c2VyX2lkIjoiMCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-05-24 02:34:36.036515');
INSERT INTO `django_session` VALUES ('zclvha25f51hzg1rv70huj116wcfh861', 'Y2FmZTFjZGM2ZTYwYjQ5NWM2YmI5MjhmNWRjYzllMjFlNmMwZGI2Mjp7Il9hdXRoX3VzZXJfaGFzaCI6Ijc5YzhlMjU3MDgzNmNkYzA5ZTk5YjljMjMzMWJjYTliNWZkMTE0OTMiLCJfYXV0aF91c2VyX2lkIjoiMCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-05-28 06:52:41.324683');
INSERT INTO `django_session` VALUES ('zs6pf2pidz27p64mme81fpbjygvlmr0n', 'Mjg1NzI0ZTkxYzQwZTIzZTE2NmM0N2NiYjU1N2UwZjY0MGY3NGI3Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjAiLCJfYXV0aF91c2VyX2hhc2giOiI3OWM4ZTI1NzA4MzZjZGMwOWU5OWI5YzIzMzFiY2E5YjVmZDExNDkzIn0=', '2019-02-09 12:10:23.887311');
INSERT INTO `django_session` VALUES ('ztgv4mgs569in26rbmtmg3suz3v89km2', 'ODcwZjgzMTBjNDQxOGNjYTU5YWQ2N2FkYjBlODc3ZDBhMDE5YTI3Mjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNzljOGUyNTcwODM2Y2RjMDllOTliOWMyMzMxYmNhOWI1ZmQxMTQ5MyIsIl9hdXRoX3VzZXJfaWQiOiIwIn0=', '2019-03-28 03:45:49.216666');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(255) NOT NULL COMMENT 'id',
  `name` varchar(20) DEFAULT NULL,
  `pwd` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('1', '111', '111');
