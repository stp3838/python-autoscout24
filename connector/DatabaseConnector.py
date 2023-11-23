import mysql.connector

class DatabaseConnector:
    _instance = None

    def __new__(cls, user, password, host, database):
        if cls._instance is None:
            cls._instance = super(DatabaseConnector, cls).__new__(cls)
            cls.user = user
            cls.password = password
            cls.host = host
            cls.database = database
        return cls._instance

    def connect(self):
        try:
            connection = mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.database,  charset="utf8")
            return connection
        except mysql.connector.Error as error:
            print("Veritabanı sunucusuna bağlanılamadı: {}".format(error))

#connector = DatabaseConnector("admin_api", "kUzk2T0Ehn", "ns.wiveda.de", "admin_api")
connector = DatabaseConnector("wiveda_system", "UYgCXGa49P4y9Jiy", " 88.198.220.233", "wiveda_system")