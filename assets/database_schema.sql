CREATE TABLE `amadvertisements` (
  `ID` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'Unique ID',
  `User` bigint(20) unsigned NOT NULL COMMENT 'User that sent the link',
  `Link` varchar(60) NOT NULL COMMENT 'The invite link',
  `Time` int(10) unsigned NOT NULL COMMENT 'The time it was sent',
  `Message` bigint(20) unsigned NOT NULL COMMENT 'The message ID that contained the invite',
  `Channel` bigint(20) unsigned NOT NULL COMMENT 'The channel the invite was sent in',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID` (`ID`),
  UNIQUE KEY `ID_2` (`ID`),
  KEY `fkIdx_838` (`User`),
  CONSTRAINT `FK_837` FOREIGN KEY (`User`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Stores records of users advertising other servers';


CREATE TABLE `amnsfw` (
  `ID` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'Unique ID of the instance',
  `User` bigint(20) unsigned NOT NULL COMMENT 'User that sent the image',
  `Confidence` float NOT NULL COMMENT 'The confidence in the NSFW-ness',
  `Time` int(10) unsigned NOT NULL COMMENT 'The time it was sent',
  `Message` bigint(20) unsigned NOT NULL COMMENT 'The ID of the message containing the image',
  `Channel` bigint(20) unsigned NOT NULL COMMENT 'The channel the image was sent in',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID` (`ID`),
  UNIQUE KEY `ID_2` (`ID`),
  KEY `fkIdx_859` (`User`),
  CONSTRAINT `FK_858` FOREIGN KEY (`User`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Stores records of users sending NSFW images';


CREATE TABLE `amsluruses` (
  `ID` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'The Unique ID of the instance',
  `User` bigint(20) unsigned NOT NULL COMMENT 'The user that used the slur',
  `Slur` varchar(20) NOT NULL COMMENT 'The Slur used',
  `Severity` int(10) unsigned DEFAULT NULL COMMENT 'The severity of the slur (TBD)',
  `Time` int(10) unsigned NOT NULL COMMENT 'The Time it was used',
  `Message` bigint(20) unsigned NOT NULL COMMENT 'The ID of the message containing the slur',
  `Channel` bigint(20) unsigned NOT NULL COMMENT 'The channel the slur was sent in',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID` (`ID`),
  UNIQUE KEY `ID_2` (`ID`),
  KEY `fkIdx_848` (`User`),
  CONSTRAINT `FK_847` FOREIGN KEY (`User`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Stores records of slur usage';


CREATE TABLE `bans` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'The unique ban ID',
  `User` bigint(20) unsigned NOT NULL COMMENT 'The user that was banned',
  `BannedBy` bigint(20) unsigned NOT NULL COMMENT 'The user that banned them',
  `Reason` varchar(255) DEFAULT NULL COMMENT 'The reason they were banned (if specified)',
  `BannedTime` int(10) unsigned NOT NULL COMMENT 'The date and time they were banned',
  `Active` tinyint(1) NOT NULL COMMENT 'Whether or not the user is currently banned\r\nAllows staff to see previous Bans',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID` (`ID`),
  KEY `fkUserB` (`User`) COMMENT 'References Users to identify who was banned',
  KEY `fkUserBBy` (`BannedBy`) COMMENT 'References Users to identify who banned this user',
  CONSTRAINT `BansUsers_BannedBy` FOREIGN KEY (`BannedBy`) REFERENCES `users` (`ID`),
  CONSTRAINT `BansUsers_BannedUser` FOREIGN KEY (`User`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Storage for bans';


CREATE TABLE `credits` (
  `Credits` int(11) unsigned NOT NULL DEFAULT 2000 COMMENT 'How many credit they have',
  `User` bigint(20) unsigned NOT NULL COMMENT 'The user',
  PRIMARY KEY (`User`),
  KEY `fkUserC` (`User`) COMMENT 'References Users to identify the user whose credits are being stored',
  CONSTRAINT `CreditsUsers_User` FOREIGN KEY (`User`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Stores the amount of credits the user has';


CREATE TABLE `dailies` (
  `User` bigint(20) unsigned NOT NULL COMMENT 'The User',
  `LastDaily` int(10) unsigned NOT NULL DEFAULT 0 COMMENT 'The date and time of their last daily',
  `DailyUses` int(10) unsigned NOT NULL DEFAULT 0 COMMENT 'The amount of times they''ve used the daily command',
  PRIMARY KEY (`User`),
  KEY `fkUserD` (`User`) COMMENT 'References Users to identify the user whose dailies are being stored',
  CONSTRAINT `DailiesUsers_User` FOREIGN KEY (`User`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Keeps track of a users use of the daily command';


CREATE TABLE `fmdata` (
  `ID` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'The unique ID of the scrobbling',
  `Track` bigint(20) unsigned NOT NULL COMMENT 'The track associated',
  `User` bigint(20) unsigned NOT NULL COMMENT 'The user who listened to that track',
  `Scrobbles` int(10) unsigned NOT NULL COMMENT 'The number of listens (referred to as Scrobbles by Last.FM)',
  PRIMARY KEY (`ID`),
  KEY `fkFMTrack` (`Track`) COMMENT 'References FMTracks to identify the track and associated artist and album',
  KEY `fkUserFD` (`User`) COMMENT 'References Users to store the Last.FM scrobbles associated with the Discord User',
  CONSTRAINT `FMDataFMTracks_Track` FOREIGN KEY (`Track`) REFERENCES `fmtracks` (`ID`),
  CONSTRAINT `FMDataUsers_User` FOREIGN KEY (`User`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Caches scrobbles the bot has seen';


CREATE TABLE `fmtracks` (
  `ID` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'The unique Track ID',
  `Artist` varchar(100) NOT NULL COMMENT 'The artist who created the track',
  `Album` varchar(100) DEFAULT NULL COMMENT 'The track album (if applicable)',
  `Track` varchar(100) NOT NULL COMMENT 'The name of the track',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Storage for tracks seen by the bot';


CREATE TABLE `fmusers` (
  `User` bigint(20) unsigned NOT NULL COMMENT 'The user',
  `Username` varchar(50) NOT NULL COMMENT 'Their Last.FM Username',
  `LastUpdated` int(10) unsigned NOT NULL COMMENT 'The date and time this was last set',
  PRIMARY KEY (`User`),
  KEY `fkUserF` (`User`) COMMENT 'References Users to store the Last.FM username associated with the Discord User',
  CONSTRAINT `FMUsersUsers_User` FOREIGN KEY (`User`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Stores the Last.FM username for each user';


CREATE TABLE `golds` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'The unique gold ID',
  `User` bigint(20) unsigned NOT NULL COMMENT 'The user given gold',
  `TimeGiven` int(10) unsigned NOT NULL COMMENT 'The time they were given gold',
  `GivenBy` bigint(20) unsigned NOT NULL COMMENT 'The user they were given gold by',
  `Message` varchar(2000) DEFAULT NULL COMMENT 'The message they were given gold for',
  PRIMARY KEY (`ID`),
  KEY `fkUserG` (`User`) COMMENT 'References Users to identify the user who received gold',
  KEY `fkUserGBy` (`GivenBy`) COMMENT 'References Users to identify the user who gave gold',
  CONSTRAINT `GoldsUsers_User` FOREIGN KEY (`User`) REFERENCES `users` (`ID`),
  CONSTRAINT `GoldsUsers_UserGivenBy` FOREIGN KEY (`GivenBy`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Stores the server''s "Golds" (similar to reddit gold?)';


CREATE TABLE `joins` (
  `ID` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'The Unique join ID',
  `User` bigint(20) unsigned NOT NULL COMMENT 'The user that joined',
  `Time` int(10) unsigned NOT NULL COMMENT 'The time that they joined',
  PRIMARY KEY (`ID`),
  KEY `fkIdx_869` (`User`),
  CONSTRAINT `FK_868` FOREIGN KEY (`User`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Stores records of users joining the server';


CREATE TABLE `leaves` (
  `ID` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'The unique ID of the leave',
  `User` bigint(20) unsigned NOT NULL COMMENT 'The user that left',
  `Time` int(11) NOT NULL COMMENT 'The time that they left',
  PRIMARY KEY (`ID`),
  KEY `fkIdx_876` (`User`),
  CONSTRAINT `FK_875` FOREIGN KEY (`User`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Stores records of users leaving the server';


CREATE TABLE `levels` (
  `User` bigint(20) unsigned NOT NULL COMMENT 'The user',
  `Points` int(10) unsigned NOT NULL DEFAULT 0 COMMENT 'Their total points',
  `Level` int(10) unsigned NOT NULL DEFAULT 0 COMMENT 'Their all-time level',
  `MonthPoints` int(10) unsigned NOT NULL DEFAULT 0 COMMENT 'Their points earned this month',
  `MonthLevel` int(10) unsigned NOT NULL DEFAULT 0 COMMENT 'Their level reached this month',
  `NextPoint` int(10) unsigned NOT NULL DEFAULT 0 COMMENT 'The date and time that they will next receive a point',
  PRIMARY KEY (`User`),
  KEY `fkUserL` (`User`) COMMENT 'References Users to identify the user whose Levels and points are being stored',
  CONSTRAINT `LevelsUsers_User` FOREIGN KEY (`User`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Keeps track of the leveling system';


CREATE TABLE `mutes` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'The mute ID',
  `User` bigint(20) unsigned NOT NULL COMMENT 'The user muted',
  `MutedBy` bigint(20) unsigned NOT NULL COMMENT 'The user that muted them',
  `Duration` int(10) unsigned NOT NULL COMMENT 'How long they were muted for',
  `UnmuteTime` int(10) unsigned NOT NULL COMMENT 'The date and time they will be unmuted',
  `Reason` varchar(300) DEFAULT NULL COMMENT 'The reason for the mute (if specified)',
  `Active` tinyint(1) unsigned NOT NULL COMMENT 'Whether or not the user is still currently muted\r\nLogically Equivalent to UnmuteTime > Current Time\r\n\r\nAllows staff to see previous mute recordings',
  PRIMARY KEY (`ID`),
  KEY `fkUserM` (`User`) COMMENT 'References Users to identify who was muted',
  KEY `fkUserMBy` (`MutedBy`) COMMENT 'References Users to identify who muted this user',
  CONSTRAINT `MutesUsers_MutedBy` FOREIGN KEY (`MutedBy`) REFERENCES `users` (`ID`),
  CONSTRAINT `MutesUsers_User` FOREIGN KEY (`User`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Keeps track of all mutes that have occured';


CREATE TABLE `nicknamechanges` (
  `ID` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'The Unique ID of the change',
  `User` bigint(20) unsigned NOT NULL COMMENT 'The user that changed their nickname',
  `Old` varchar(38) DEFAULT NULL COMMENT 'Their old nickname',
  `New` varchar(38) DEFAULT NULL COMMENT 'Their new nickname',
  `Time` int(10) unsigned NOT NULL COMMENT 'The time the nickname was changed',
  PRIMARY KEY (`ID`),
  KEY `fkIdx_883` (`User`),
  CONSTRAINT `FK_882` FOREIGN KEY (`User`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Stores nickname changes';


CREATE TABLE `purchasedroles` (
  `ID` int(10) unsigned NOT NULL COMMENT 'The transaction associated with the role purchase',
  `User` bigint(20) unsigned NOT NULL COMMENT 'The user who owns the role',
  `Role` bigint(20) unsigned NOT NULL COMMENT 'The role that is owned',
  `Active` tinyint(1) unsigned NOT NULL COMMENT 'Whether or not the user has the role applied',
  PRIMARY KEY (`ID`),
  KEY `fkRole` (`Role`) COMMENT 'References Roles to identify the role that was purchased',
  KEY `fkTransactionR` (`ID`) COMMENT 'References transaction to mark the transaction associated with this purchasedRole',
  KEY `fkUserR` (`User`) COMMENT 'References Users to identify who purchased the role',
  CONSTRAINT `PurchasedRolesRoles_Role` FOREIGN KEY (`Role`) REFERENCES `roles` (`ID`),
  CONSTRAINT `PurchasedRolesTransaction_Transaction` FOREIGN KEY (`ID`) REFERENCES `transactions` (`ID`),
  CONSTRAINT `PurchasedRolesUsers_User` FOREIGN KEY (`User`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Storage for Roles purchased by users';


CREATE TABLE `reminders` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'The unique remind ID',
  `User` bigint(20) unsigned NOT NULL COMMENT 'The user to be reminded',
  `RemindTime` int(10) unsigned NOT NULL COMMENT 'The date and time to be reminded',
  `RemindText` varchar(500) NOT NULL COMMENT 'The reason for the reminder/what they are to be reminded of',
  `Active` tinyint(1) unsigned NOT NULL COMMENT 'Whether or not this reminder has been sent\r\nEquivalent to RemindTime > CurrentTime\r\n\r\nAllows a user to see their past reminders',
  PRIMARY KEY (`ID`),
  KEY `fkUserRem` (`User`) COMMENT 'References users to Identify the user who is being reminded',
  CONSTRAINT `RemindersUser_User` FOREIGN KEY (`User`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Storage for reminders (users can be reminded)';


CREATE TABLE `roles` (
  `ID` bigint(20) unsigned NOT NULL COMMENT 'The role ID (based on Discord Snowflake)',
  `Name` varchar(100) NOT NULL COMMENT 'The name of the role',
  `Price` int(10) unsigned NOT NULL COMMENT 'The price of the role (0 if free)',
  `Color` varchar(15) DEFAULT NULL COMMENT 'The color of the role (if it''s a color role)',
  `Type` int(10) unsigned NOT NULL COMMENT 'The role type',
  `Reaction` varchar(5) DEFAULT NULL COMMENT 'The reaction to use for a shop menu',
  PRIMARY KEY (`ID`),
  KEY `fkRType` (`Type`) COMMENT 'References RoleTypes to define the type of this role',
  CONSTRAINT `RolesRoleTypes_RoleType` FOREIGN KEY (`Type`) REFERENCES `roletypes` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Stores roles that can be purchased or added  by users';


CREATE TABLE `roletypes` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'The type ID',
  `Name` varchar(50) NOT NULL COMMENT 'The type name',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Stores the types of roles (ex: ping roles, pronoun roles, color roles, other)';


CREATE TABLE `tags` (
  `TagName` varchar(50) NOT NULL COMMENT 'The name of the tag (unique)',
  `CreatedBy` bigint(20) unsigned NOT NULL COMMENT 'The user that created the tag',
  `Content` varchar(2000) NOT NULL COMMENT 'The content of the tag',
  `LastUpdated` int(10) unsigned NOT NULL COMMENT 'The last time the tag was updated',
  `Uses` int(10) unsigned NOT NULL DEFAULT 0 COMMENT 'The amount of time the tag has been used',
  PRIMARY KEY (`TagName`),
  KEY `fkUserTag` (`CreatedBy`) COMMENT 'References Users to identify the user that created the tag',
  CONSTRAINT `TagsUsers_Creator` FOREIGN KEY (`CreatedBy`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Storage for user tags';


CREATE TABLE `tempbans` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'The unique temporary ban ID',
  `User` bigint(20) unsigned NOT NULL COMMENT 'The user who is banned',
  `BannedBy` bigint(20) unsigned NOT NULL COMMENT 'The user who banned the banned user',
  `Reason` varchar(500) DEFAULT NULL COMMENT 'The reason for the ban (if specified)',
  `UnbanTime` int(10) unsigned NOT NULL COMMENT 'The date and time the user should be unbanned',
  `BannedTime` int(10) unsigned NOT NULL COMMENT 'The date and time they were banned',
  `Active` tinyint(1) unsigned NOT NULL COMMENT 'Whether or not the user is currently banned\r\nLogically Equivalent to UnbanTime> Current Time\r\n\r\nAllows staff to see previous TempBans',
  PRIMARY KEY (`ID`),
  KEY `fkUserTB` (`User`) COMMENT 'References Users to identify who was temporarily banned',
  KEY `fkUserTBy` (`BannedBy`) COMMENT 'References Users to identify who temporarily banned this user',
  CONSTRAINT `TempBansUsers_BannedBy` FOREIGN KEY (`BannedBy`) REFERENCES `users` (`ID`),
  CONSTRAINT `TempBansUsers_BannedUser` FOREIGN KEY (`User`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Storage for temporary bans';


CREATE TABLE `transactions` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'The unique transaction ID',
  `User` bigint(20) unsigned NOT NULL COMMENT 'The user affected by the transaction',
  `Type` int(10) unsigned NOT NULL COMMENT 'The type of transaction (see TransactionsType table)',
  `Time` int(10) unsigned NOT NULL COMMENT 'The date and time the transaction occured',
  `Amount` int(11) NOT NULL COMMENT 'The amount associated with the transaction\r\n+ for increase in credits\r\n- for decrease (purchases)',
  `PreviousBalance` int(10) unsigned NOT NULL COMMENT 'The balance before the transaction',
  `NewBalance` int(10) unsigned NOT NULL COMMENT 'The balance after the transaction',
  PRIMARY KEY (`ID`),
  KEY `fkTType` (`Type`) COMMENT 'References TransactionTypes to define the type of transaction that occured',
  KEY `fkUserT` (`User`) COMMENT 'References Users to identify the user who the transaction is associated with',
  CONSTRAINT `TransactionsTransactionType_Type` FOREIGN KEY (`Type`) REFERENCES `transactiontypes` (`ID`),
  CONSTRAINT `TransactionsUsers_User` FOREIGN KEY (`User`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Storage for any change in credits';


CREATE TABLE `transactiontypes` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'The type ID',
  `Name` varchar(50) NOT NULL COMMENT 'The type name',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Stores the types of transactions (ex, daily use, level up, role purchase, etc)';


CREATE TABLE `usernamechanges` (
  `ID` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'The unique ID of the username change',
  `User` bigint(20) unsigned NOT NULL COMMENT 'The user that changed their username',
  `Old` varchar(38) NOT NULL COMMENT 'Their old username',
  `New` varchar(38) NOT NULL COMMENT 'Their new username',
  `Time` int(10) unsigned NOT NULL COMMENT 'The time it was changed',
  PRIMARY KEY (`ID`),
  KEY `fkIdx_883_clone` (`User`),
  CONSTRAINT `FK_882_clone` FOREIGN KEY (`User`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Stores username changes';


CREATE TABLE `users` (
  `ID` bigint(20) unsigned NOT NULL COMMENT 'The Users'' Discord Snowflake ID',
  `Username` varchar(38) NOT NULL COMMENT 'Their current Discord Username',
  `Nickname` varchar(38) DEFAULT NULL COMMENT 'Their current server nickname',
  `CreationDate` int(10) unsigned NOT NULL COMMENT 'The date and time their account was created',
  `ActiveUser` tinyint(1) unsigned NOT NULL DEFAULT 1 COMMENT 'If they still are in the server',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Stores all the Users that are in and have been in the server';


CREATE TABLE `warnings` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'The unique warning ID',
  `User` bigint(20) unsigned NOT NULL COMMENT 'The User warned',
  `WarnedBy` bigint(20) unsigned NOT NULL COMMENT 'Who warned the user',
  `Reason` varchar(500) NOT NULL COMMENT 'The reason for the warning',
  `Date` int(10) unsigned NOT NULL COMMENT 'The date and time the warning occured',
  `Severity` int(10) unsigned NOT NULL COMMENT 'The Severity of the warning (1-10)',
  PRIMARY KEY (`ID`),
  KEY `fkUserW` (`User`) COMMENT 'References Users to identify who was warned',
  KEY `fkUserWBy` (`WarnedBy`) COMMENT 'References Users to identify who warned this user',
  CONSTRAINT `WarningsUsers_WarnedBy` FOREIGN KEY (`WarnedBy`) REFERENCES `users` (`ID`),
  CONSTRAINT `WarningsUsers_WarnedUser` FOREIGN KEY (`User`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Stores warnings for users';


DELIMITER $$
CREATE OR REPLACE PROCEDURE `zeus`.`daily`(IN u_id bigint, IN d_reward INT, IN u_dailyt int)
BEGIN
	UPDATE Dailies SET DailyUses = DailyUses+1, LastDaily = u_dailyt WHERE User = u_id;
	SELECT Credits INTO @prev FROM Credits WHERE User = u_id LIMIT 1;
	UPDATE Credits SET Credits = Credits+d_reward WHERE User = u_id;
	INSERT INTO transactions(User, Type, Time, Amount, PreviousBalance, NewBalance)
		VALUES(u_id, 1, u_dailyt, d_reward, @prev, (@prev + d_reward) );
END $$
DELIMITER ;;


DELIMITER $$
CREATE OR REPLACE PROCEDURE `zeus`.`ScoreCard`(IN userid BIGINT)
BEGIN
	SELECT LvlCard.Points, LvlCard.Rank, Credits.Credits, COUNT(Golds.ID) as Golds, Dailies.DailyUses
	FROM (
		SELECT User, Points, FIND_IN_SET( Points, (
		SELECT GROUP_CONCAT( DISTINCT Points
		ORDER BY Points DESC ) FROM Levels)
		) AS rank
		FROM Levels
		ORDER BY Points DESC
		) as LvlCard
	INNER JOIN Credits on Credits.User = LvlCard.User
	LEFT JOIN Golds on Golds.User = LvlCard.User
	LEFT JOIN Dailies on Dailies.User = LvlCard.User
	WHERE LvlCard.User = userid;
END $$
DELIMITER ;;

DELIMITER $$
CREATE OR REPLACE PROCEDURE `zeus`.`update_nickname`(IN u_id bigint, IN u_name VARCHAR(38), IN u_changet int)
BEGIN
	SELECT Nickname INTO @old FROM Users WHERE Users.ID = u_id LIMIT 1;
	INSERT INTO nicknamechanges(User, Old, New, Time) VALUES(u_id, @old, u_name, u_changet);
	UPDATE Users SET Nickname = u_name WHERE ID = u_id;
END $$
DELIMITER ;;

DELIMITER $$
CREATE OR REPLACE PROCEDURE `zeus`.`update_username`(IN u_id bigint, IN u_uname VARCHAR(38), IN u_changet int)
BEGIN
	SELECT Username INTO @old FROM Users WHERE Users.ID = u_id LIMIT 1;
	INSERT INTO usernamechanges(User, Old, New, Time) VALUES(u_id, @old, u_uname, u_changet);
	UPDATE Users SET Username = u_name WHERE ID = u_id;
END $$
DELIMITER ;;

DELIMITER $$
CREATE OR REPLACE PROCEDURE `zeus`.`user_join`(IN u_id bigint, IN u_name VARCHAR(38), IN u_create int, IN u_joint int)
BEGIN
	IF NOT EXISTS ( SELECT 1 FROM Users WHERE ID = u_id) THEN	
		INSERT INTO Users (ID, Username, CreationDate) VALUES (u_id, u_name, u_create);
		INSERT INTO Credits (User) VALUES (u_id);
		INSERT INTO Dailies (User) VALUES (u_id);
		INSERT INTO Levels (User) VALUES (u_id);
	ELSE
		UPDATE Users SET ActiveUser=1 WHERE ID=u_id;
		IF (SELECT Username FROM Users WHERE ID=u_id) != u_name THEN
			CALL update_username(u_id, u_name, u_joint);
		END IF;
		CALL update_nickname(u_id, NULL , u_joint);
	END IF;
	INSERT INTO Joins (User, Time) VALUES (u_id, u_joint);
END $$
DELIMITER ;;

DELIMITER $$
CREATE OR REPLACE PROCEDURE `zeus`.`user_leave`(IN u_id bigint, IN u_leavet int)
BEGIN
	UPDATE Users SET ActiveUser=0 WHERE ID=u_id;
	INSERT INTO Leaves (User, Time) VALUES (u_id, u_leavet);
END $$
DELIMITER ;;
