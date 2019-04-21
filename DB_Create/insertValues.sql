USE eByMazon;

INSERT INTO User(username, password,userType)
VALUES ('admin','password',TRUE),('selina81','1031',FALSE),('hebe83','0330',FALSE),
      ('ella84','0618',FALSE),('lu7','0420',FALSE),('ran90','1203',FALSE),
      ('feng33','0325',FALSE),('ying96','0999',FALSE),('du11','0214',FALSE),
       ('dele22','1111',FALSE);

INSERT INTO OU(ouID, name, cardNumber,email,address,state,phone) VALUES
(2,'Selina Ren','1234567890123456','sren@gmail.com','Taipei 101', 'NY', 9171201031),
(3,'Hebe Tian','0987654321098765','htian@gmail.com','Xinzhu 102','NJ',9174050330),
(4,'Ella Chen','1357924680123456','schen@aol.com','PingDong 103', 'CA', 9177700618),
(5, 'Han Lu', '1234560987610293', 'hlu777@yahoo.com','BeiJing 104','WI', 9177770420),
(6,'Ran Peng','1234987650123456','rpeng@gmail.com','Beijing 101', 'TX', 9171990123),
(7,'Feng Xiao','1232467832498432','fxiao@aol.com','Xichuan 886','PA',9170325330),
(8,'Ying Li','1223342341254525','yli@aol.com','Shangjing 113', 'MI', 9170214334),
(9, 'Du Aa', '2011092334905', 'aadu@yahoo.com','Dangchi 704','TN', 9177110701),
(10,'Xu Chen', '201121334905', 'xuC@yahoo.com','DongGong 555','TN', 9177353701);

INSERT INTO GUapplications(username,email,name,cardNumber,address,state,phone) VALUES
('bon18','bonbon@tian.com','Bon Tian','2001938436634','TaoYuan 1023','NJ',9175550330);

INSERT INTO OUstatus(ouID, moneySpend, status) VALUES
(2,10.31, 1),(3,0,0),(4,0,0),(5, 777, 1),(6,90, 0),(7,540,1),(8,44,3),(9, 59, 2),(10,45,3);
-- INSERT INTO ItemInfo(itemID, image, title, priceType, saleStatus)

INSERT INTO FriendList(ownerID, friendID, discount) VALUES
(2,3,0.05),(3,2,0.10),(4,2,0.03),(6,7,0.05),(7,6,0.05),(6,9,0.05),(8,7,0.15),(6,3,0.05);

INSERT INTO MessageSent(senderID, receiverID, message) VALUES
(2,3,'Good Morning'),(4,2,'Come to my home page'),(6,7,'How are you?');

INSERT INTO ItemOwner(itemID, ownerID) VALUES
(1,2),(2,2),(3,4),(4,4),(5,3),(6,5);

INSERT INTO KeywordRecord(keyword, itemID) VALUES
('CD',1),('SHE',1),('DVD',2),('SHE',2),
('BOOK',3),('HARRY POTTER',3),('J. K. ROWLING',3),
('BOOK',4),('THE HUNGER GAMES',4),('SUZANNE COLLINS',4),
('LAPTOP',5),('SAMSUNG',5),('17 INCH',5),
('APPLE',6),('MAC BOOK',6),('13 INCH',6);

INSERT INTO FixedPrice(itemID, price, availableNum) VALUES
(1,15.99,10),(2,17.79,20),(3,7.99,5),(4,12.50,20);

INSERT INTO ItemBid(itemID, startPrice) VALUES (5,300),(6,800);

INSERT INTO Transaction(itemID, buyerID, singlePrice, priceTotal, numDeal, shippingStatus)
VALUES (1,7,15.99,16.40,1,TRUE),(1,6,15.99,17.30,1,TRUE);

INSERT INTO Complaint(itemID, complainerID, description, justified) VALUES
(1,7,'Arrive Too Late',TRUE);
# Electronic, Home, Grocery, Clothes,Furniture,Education,Music
INSERT INTO Category(category, itemID) VALUES
('Music',1),('Music',2),('Education',3),('Education',4),('Electronic',5),('Electronic',6);

INSERT INTO Taboo(word) VALUES ('subway'),('CSC'),('TG'),('super'),('winner');

INSERT INTO ouBlacklist VALUES ('block123'),('test123');