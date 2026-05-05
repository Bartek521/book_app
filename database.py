import sqlite3

class database:
        def __init__(self,db_name = 'datebase.db'):
                self.db_name = db_name
        def GetConnectionDb(self):
                connect_db = sqlite3.connect(self.db_name)
                cursor = connect_db.cursor()
                cursor.execute("PRAGMA FOREIGN_KEYS = ON")
                return connect_db
        def InitDb(self):
                with self.GetConnectionDb() as database:
                        cursor = database.cursor()
                        cursor.execute(''' CREATE TABLE IF NOT EXISTS USERS
                                           (ID_USER INTEGER PRIMARY KEY AUTOINCREMENT,
                                            NAME TEXT NOT NULL,
                                            LASTNAME TEXT NOT NULL,
                                            EMAIL TEXT UNIQUE NOT NULL CHECK (EMAIL LIKE '%@%'),
                                            PASSWORD TEXT NOT NULL CHECK (LENGTH(PASSWORD)>7),
                                            ROLA TEXT DEFAULT "USER" );''');
                        cursor.execute('''CREATE TABLE IF NOT EXISTS BOOKS
                                          (ID_BOOK INTEGER PRIMARY KEY AUTOINCREMENT,
                                           BARCODE TEXT UNIQUE NOT NULL,
                                           TITLE TEXT NOT NULL,
                                           AUTHOR TEXT NOT NULL,
                                           PUBLISHING_HOUSE TEXT NOT NULL,
                                           YEAR VARCHAR(4) NOT NULL,
                                           KIND TEXT NOT NULL);
                                           ''')
                        cursor.execute('''CREATE TABLE IF NOT EXISTS MAGAZINE
                                          (ID_OPERATION INTEGER PRIMARY KEY AUTOINCREMENT,
                                           ID_USER INTEGER NOT NULL,
                                           ID_BOOK INTEGER NOT NULL,
                                           STATUS TEXT NOT NULL CHECK (STATUS IN ("DO KUPIENIA","DO PRZECZYTANIA","W TRAKCIE CZYTANIA", "PRZECZYTANE")),
                                           RATE REAL,
                                           NOTES TEXT,
                                           FOREIGN KEY(ID_USER) REFERENCES USERS(ID_USER),
                                           FOREIGN KEY(ID_BOOK) REFERENCES BOOKS(ID_BOOK));
                                           ''')
                        database.commit()
        def DbClose(self):
                self.cursor.close()
                self.datebase.close()