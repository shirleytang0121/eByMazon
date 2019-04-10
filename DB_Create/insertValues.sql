USE eByMazon;

INSERT INTO User(username, password,userType)
VALUES ('admin','password',TRUE),('selina81','1031',FALSE),('hebe83','0330',FALSE),
      ('ella84','0618',FALSE),('lu7','0420',FALSE);

INSERT INTO OU(ouID, name, cardNumber,address,state,phone) VALUES
(2,'Selina Ren','1234567890123456','Taibei 101', 'NY', 9171201031),
(3,'Hebe Tian','0987654321098765','Xinzhu 102','NJ',9174050330),
(4,'Ella Chen','1357924680123456','PingDong 103', 'CA', 9177700618),
(5, 'Han Lu', '1234560987610293', 'BeiJing 104','WI', 9177770420);

INSERT INTO OUstatus(ouID, moneySpend, status) VALUES
(2,10.31, TRUE),(3,0,FALSE),(4,0,FALSE),(5, 777, TRUE);
# INSERT INTO ItemInfo(itemID, image, title, priceType, saleStatus)

INSERT INTO FriendList(ownerID, friendID, discount) VALUES
(2,3,0.05),(3,2,0.10),(4,2,0.03);

INSERT INTO MessageSent(senderID, receiverID, message) VALUES
(2,3,'Good Morning'),(4,2,'Come to my home page');

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

# Electronic, Home, Grocery, Clothes,Furniture,Education,Music
INSERT INTO Category(category, itemID) VALUES
('Music',1),('Music',2),('Education',3),('Education',4),('Electronic',5),('Electronic',6);

INSERT INTO Taboo(word) VALUES ('subway'),('CSC'),('TG'),('super'),('winner')