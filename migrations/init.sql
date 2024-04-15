-- ACTIVITIES определение

CREATE TABLE IF NOT EXISTS ACTIVITY (
	ID INTEGER NOT NULL,
	NAME TEXT(100) NOT NULL,
	USER_ID INTEGER NOT NULL,
	TYPE_ID INTEGER NOT NULL,
	Duration TEXT(50) NOT NULL,
	START_TIME TEXT(50) NOT NULL,
	END_TIME TEXT(50) NOT NULL,
	DESCRIPTION TEXT(2000),
	CONSTRAINT Activitys_PK PRIMARY KEY (ID)
	FOREIGN KEY (Type_ID) REFERENCES ACTIVITY_TYPES(ID)
	FOREIGN KEY (USER_ID) REFERENCES USERS(ID)
);

-- Users определение

CREATE TABLE IF NOT EXISTS  Users (
	ID INTEGER NOT NULL,
	EMAIL TEXT(50) NOT NULL,
	PASSWORD TEXT(100) NOT NULL,
	USERNAME TEXT(100) NOT NULL,
	CONSTRAINT Users_PK PRIMARY KEY (ID)
);

-- ACTIVITY_TYPES определение

CREATE TABLE IF NOT EXISTS  "ACTIVITY_TYPES" (
	ID INTEGER NOT NULL,
	NAME TEXT(50) NOT NULL,
	ICON_NAME TEXT(200) NOT NULL,
	CONSTRAINT ACTIVITY_TYPE_PK PRIMARY KEY (ID)
);