# eByMazon
Mini combine eBay and amazon system

## Create Database
Below is instruction to initalize the eByMazon Database

### Prerequisites
- [Python3](https://www.python.org/downloads/)
- [MariaDB](https://mariadb.org/)

### Steps
1.Clone and install modules
```
git clone https://github.com/jinchen1036/eByMazon.git
cd eByMazon
pip install mysql-connect 
```

2. Go to db_init.py in DB_Create folder, enter your username and password for your own mysql. 
3. run python file to start initialize eByMazon database
```
python3 DB_Create/db_init.py
```
