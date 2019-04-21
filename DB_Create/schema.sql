-- DROP DATABASE IF EXISTS eByMazon;
CREATE DATABASE IF NOT EXISTS eByMazon;
USE eByMazon;

-- Drop all tables if exists
DROP TABLE IF EXISTS Taboo,ouBlacklist,itemBlackList,Notification,Tax;
DROP TABLE IF EXISTS Complaint,Warning,OUlike,ItemView;
DROP TABLE IF EXISTS BidRecord,Category,searchKeyword,ItemRate;
DROP TABLE IF EXISTS FixedPrice,ItemBid;
DROP TABLE IF EXISTS Transaction,KeywordRecord;
DROP TABLE IF EXISTS MessageSent,Appeal,ItemInfo;
DROP TABLE IF EXISTS GUapplications,OUstatus,ItemOwner,FriendList;
DROP TABLE IF EXISTS OU;
DROP TABLE IF EXISTS User;

-- Create Table
CREATE TABLE User(
  ID INTEGER PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(64) UNIQUE NOT NULL,
  password VARCHAR(64) NOT NULL,
  userType BOOLEAN    -- True for SU, False for OU
);


CREATE TABLE GUapplications(
--   applicationID INTEGER PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(64) UNIQUE NOT NULL,
  email VARCHAR(64),
  name VARCHAR(32) NOT NULL,
  cardNumber VARCHAR(32) NOT NULL,
  address VARCHAR(64) NOT NULL,
  state VARCHAR(32),    -- calculate tax during check out
  phone VARCHAR(32)
);

CREATE TABLE OU(
  ouID INTEGER PRIMARY KEY,
  name VARCHAR(32) NOT NULL,
  cardNumber VARCHAR(32) NOT NULL,
  email VARCHAR (64),
  address VARCHAR(64) NOT NULL,
  state VARCHAR(32),    -- calculate tax during check out
  phone VARCHAR(32),
  FOREIGN KEY (ouID) REFERENCES User(ID) ON DELETE CASCADE
);

CREATE TABLE OUstatus(
  ouID INTEGER PRIMARY KEY,
  moneySpend FLOAT,
  aveRate FLOAT,
  status INTEGER ,    -- 0 for OU, 1 for VIP, 2 for Suspended, 3 for remove
  statusTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- ON UPDATE CURRENT_TIMESTAMP, -- check for changing status
  FOREIGN KEY (ouID) REFERENCES OU(ouID) ON DELETE CASCADE
);

CREATE TABLE Appeal(
  ouID INTEGER,
  message VARCHAR(256),
  appealTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (ouID) REFERENCES OU(ouID) ON DELETE CASCADE
);
CREATE TABLE FriendList(
  ownerID INTEGER,
  friendID INTEGER,
  discount FLOAT,
  PRIMARY KEY (ownerID, friendID),
  FOREIGN KEY (ownerID) REFERENCES User(ID) ON DELETE CASCADE,
  FOREIGN KEY (friendID) REFERENCES User(ID) ON DELETE CASCADE
);
CREATE TABLE MessageSent(
  senderID INTEGER,
  receiverID INTEGER,
  message VARCHAR(128),
  sendTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (senderID,receiverID) REFERENCES FriendList(ownerID, friendID) ON DELETE CASCADE
);

-- Item
CREATE TABLE ItemOwner(
  itemID INTEGER PRIMARY KEY AUTO_INCREMENT,
  ownerID INTEGER,
  FOREIGN KEY (ownerID) REFERENCES OU(ouID) ON DELETE CASCADE
);


CREATE TABLE ItemInfo(
  itemID INTEGER PRIMARY KEY,
  image BLOB,               -- Only allow store file/image up to 64KB
  title VARCHAR(64),
  description VARCHAR(256),
  priceType BOOLEAN,        -- False for fixed price, true for bidding
  usedStatus BOOLEAN,
  saleStatus BOOLEAN DEFAULT FALSE,
  approvalStatus BOOLEAN DEFAULT FALSE,   -- approval by SU
  likeness INTEGER DEFAULT 0,
  dislike INTEGER DEFAULT 0,
  postTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (itemID) REFERENCES ItemOwner(itemID) ON DELETE CASCADE
);
-- CREATE TABLE KeywordRecord(
--   keyword VARCHAR(64),
--   itemID  INTEGER,
--   PRIMARY KEY (keyword,itemID),
--   FOREIGN KEY (itemID) REFERENCES ItemOwner(itemID) ON DELETE CASCADE
-- );

CREATE TABLE FixedPrice(
  itemID INTEGER PRIMARY KEY,
  price FLOAT,
  availableNum INTEGER,
  FOREIGN KEY (itemID) REFERENCES ItemOwner(itemID) ON DELETE CASCADE
);
CREATE TABLE ItemBid(
  itemID INTEGER PRIMARY KEY,
  startPrice FLOAT,
--  bid_high FLOAT,
  endDay TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (itemID) REFERENCES ItemOwner(itemID) ON DELETE CASCADE
);

CREATE TABLE BidRecord(
  itemID INTEGER,
  bidderID INTEGER,
  bidPrice FLOAT,
  bidTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (itemID, bidderID),
  FOREIGN KEY (itemID) REFERENCES ItemOwner(itemID) ON DELETE CASCADE,
  FOREIGN KEY (bidderID) REFERENCES OU(ouID) ON DELETE CASCADE
);



CREATE TABLE Category(  -- ?
--   categoryID INTEGER AUTO_INCREMENT,
  category VARCHAR(64),
  itemID INTEGER,
  PRIMARY KEY (category,itemID),
  FOREIGN KEY (itemID) REFERENCES ItemOwner(itemID) ON DELETE CASCADE
);


CREATE TABLE Transaction(
  itemID  INTEGER,
  buyerID INTEGER REFERENCES OU(ouID) ON DELETE SET NULL,
  singlePrice FLOAT,    --  If multi available, price will be single price
  priceTotal FLOAT,
  numDeal INTEGER,    --  Need for multi-available
  shippingStatus BOOLEAN,  -- False for not ship, True for shipped
  dealTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (itemID,buyerID),
  FOREIGN KEY (itemID) REFERENCES ItemOwner(itemID) ON DELETE CASCADE
);


CREATE TABLE ItemRate(
  itemID  INTEGER,
  raterID  INTEGER REFERENCES Transaction(buyerID) ON DELETE SET NULL,
  rating INTEGER,     -- From 0 to 5
  description VARCHAR(128),
  likes INTEGER,      --  Not need for second hand
  postTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(itemID, raterID),
  FOREIGN KEY (itemID) REFERENCES Transaction(itemID) ON DELETE CASCADE
);

CREATE TABLE Complaint(
  itemID  INTEGER,
  complainerID  INTEGER REFERENCES Transaction(buyerID) ON DELETE SET NULL,
  description VARCHAR(128),
  compliantTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  justified BOOLEAN,
  PRIMARY KEY (itemID, complainerID),
  FOREIGN KEY (itemID) REFERENCES Transaction(itemID) ON DELETE CASCADE
);

--  CREATE TABLE WarningCategory(
--    warningID INTEGER PRIMARY KEY,
--    description VARCHAR(128)
--  );
CREATE TABLE Warning(
  itemID INTEGER,
  warningID INTEGER, -- 0 for low rating, 1 for 2 complaints, 2 for decline deal, 3 for removed item, 4 for taboo word
  warnTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (itemID,warningID),
  FOREIGN KEY (itemID) REFERENCES Transaction(itemID) ON DELETE CASCADE
);

-- Search
CREATE TABLE searchKeyword(
  keyword VARCHAR(64) PRIMARY KEY ,
  frequency INTEGER
--   FOREIGN KEY (keyword) REFERENCES KeywordRecord(keyword)
);

CREATE TABLE OUlike(
  ouID INTEGER,
  keyword VARCHAR(64),
  frequency INTEGER,
  PRIMARY KEY (ouID, keyword),
  FOREIGN KEY (ouID) REFERENCES OU(ouID) ON DELETE CASCADE,
  FOREIGN KEY (keyword) REFERENCES searchKeyword(keyword)
);

CREATE TABLE ItemView(
  itemID INTEGER PRIMARY KEY,
  frequency INTEGER,
  FOREIGN KEY (itemID) REFERENCES itemOwner(itemID) ON DELETE CASCADE
);

CREATE TABLE Notification(
  keyword VARCHAR(64)
);

-- Others
CREATE TABLE Tax (
  state VARCHAR(32) PRIMARY KEY,
  taxRate FLOAT
);

CREATE TABLE Taboo (word VARCHAR(64));
CREATE TABLE ouBlacklist (ouName VARCHAR(64));    -- for blockOU, sold item will not be remove
-- ouName is the username

CREATE TABLE itemBlackList(itemID INTEGER);