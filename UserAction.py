import sqlite3

class UserAction :
    def __init__(self,database):
        self.database = database
    def CheckUsers(self,email):
        with self.database.GetConnectionDb() as connect:
            cursor = connect.cursor()
            cursor.execute("SELECT ID_USER FROM USERS WHERE EMAIL = ?",(email,))
            if cursor.fetchone():
                return True
            else:
                return False
    def AddUser(self, name,secondname,email,password,rola):
        try:
            with self.database.GetConnectionDb() as connect:
                if self.CheckUsers(email):
                    return False,"Email jest już przypisany do innego użytkownika"
                else:
                    cursor = connect.cursor()
                    cursor.execute("INSERT INTO USERS(NAME,SECONDNAME,EMAIL,PASSWORD,ROLA),VALUES(?,?,?,?,?)",(name,secondname,email,password,rola))
                    return True,"Zarejestrowano"
        except sqlite3.Error as e:
            return False,f"Błąd bazy danych :{e}"
    def Login(self,email, password):
        try:
            with self.database.GetConnectionDb() as connect:
                cursor = connect.cursor()
                cursor.execute("SELECT ID_USER FROM USERS WHERE (UPPER(EMAIL)=UPPER(?) AND PASSWORD = ?",(email,password,))
                user = cursor.fetchone()
                if user:
                    return user,"Użytkownik zalogowany",
                else:
                    return False,"Użytkownik nie posiada konta, najpierw zarejestruj się."
        except sqlite3.Error as e:
            return False,f"Błąd bazy danych : {e}"
    def CheckBook(self,barcode):
        with self.database.GetConnectionDb() as connect:
            cursor = connect.cursor()
            cursor.execute("SELECT ID_BOOK FORM BOOKS WHERE BARCODE=?",(barcode,))
            book = cursor.fetchone()
            if book:
                return True
            else:
                return False
    def AddBook(self,barcode,title,author,publishing_house,year,kind):
        try:
            with self.database.GetConnectionDb() as connect:
                cursor = connect.cursor()
                book = self.CheckBook(barcode)
                if book:
                    return False,"Książka o takim kodzie kreskowym już istnieje"
                else:
                    cursor.execute("INSERT INTO BOOKS(BARCODE,TITLE,AUTHOR,PUBLISHING_HOUSE,YEAR,KIND) VALUES (?,?,?,?,?,?)",
                                   (barcode, title, author, publishing_house, year, kind))
                    return True,"Dodano książkę do bazy"
        except sqlite3.Error as e:
            return False,f"Błąd bazy danych: {e}"