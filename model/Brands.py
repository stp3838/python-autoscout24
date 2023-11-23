from connector.DatabaseConnector import connector


class Brands:
    def __init__(self, id = None, name = None, website = None, url = None, created_at = None, status = None):
        self.id = id
        self.name = name
        self.website = website
        self.url = url
        self.created_at = created_at
        self.status = status

    @classmethod
    def create_conn(cls):
        return connector.connect()

    @classmethod
    def selectAll(cls):
        connection = cls.create_conn()
        cursor = connection.cursor()

        query = "SELECT * FROM brands"
        cursor.execute(query)
        results = cursor.fetchall()

        brands = []
        for result in results:
            id, name, website, url, created_at, status = result
            brand = Brands(id, name, website, url, created_at, status)
            brands.append(brand)
        return brands

    @classmethod
    def getAllWebsite(cls, website):
        connection = cls.create_conn()
        cursor = connection.cursor()

        query = f"SELECT * FROM brands WHERE website = '{website}'"
        cursor.execute(query)
        results = cursor.fetchall()

        brands = []
        for result in results:
            id, name, website, url, created_at, status = result
            brand = Brands(id, name, website, url, created_at, status)
            brands.append(brand)
        return brands

    @classmethod
    def selectById(cls, id):
        connection = cls.create_conn()
        cursor = connection.cursor()

        query = f"SELECT * FROM brands WHERE id = {id}"
        cursor.execute(query)

        result = cursor.fetchone()

        id, name, website, url, created_at, status = result
        brand = Brands(id, name, website, url, created_at, status)

        cursor.close()
        connection.close()

        return brand

    @classmethod
    def get_by_name(cls, name, web_site):
        connection = None
        cursor = None
        try:
            connection = cls.create_conn()
            cursor = connection.cursor()

            query = f"""
                SELECT 
                    * 
                FROM 
                    brands 
                WHERE 
                    name = '{name}' 
                AND
                    website = '{web_site}'
                LIMIT 1
            """

            cursor.execute(query)
            result = cursor.fetchone()

            if result is not None:
                id, name, website, url, created_at, status = result
                brand = Brands(id, name, website, url, created_at, status)
            else:
                brand = None

        except Exception as e:
            print(f"Bir hata oluştu: {e}")
            brand = None
        finally:
            if cursor is not None:
                try:
                    cursor.close()

                except Exception as e:
                    print(f"Bir hata oluştu: {e}")
            if connection is not None:
                connection.close()

        return brand

    @classmethod
    def get_by_name_like(cls, name, web_site):
        connection = cls.create_conn()
        cursor = connection.cursor()

        query = f"""
                SELECT 
                    * 
                FROM 
                    brands 
                WHERE 
                    name like '%{name}%' 
                AND
                    website = '{web_site}'
                """
        cursor.execute(query)

        result = cursor.fetchone()

        id, name, website, url, created_at, status = result
        brand = Brands(id, name, website, url, created_at, status)

        cursor.close()
        connection.close()

        return brand

    @classmethod
    def getByUrl(cls, url):
        connection = cls.create_conn()
        cursor = connection.cursor()

        query = f"SELECT * FROM brands WHERE url = '{url}' LIMIT 1"
        cursor.execute(query)

        result = cursor.fetchone()

        if result:
            id, name, website, url, created_at, status = result
            brand = Brands(id, name, website, url, created_at, status)
        else:
            brand = None

        cursor.close()
        connection.close()

        return brand
    @classmethod
    def getWebsite(cls, website):
        connection = cls.create_conn()
        cursor = connection.cursor()

        query = f"SELECT * FROM brands WHERE website = {website}"
        cursor.execute(query)

        result = cursor.fetchone()

        if result:
            id, name, website, url, created_at, status = result
            brand = Brands(id, name, website, url, created_at, status)
        else:
            brand = None

        cursor.close()
        connection.close()

        return brand

    @classmethod
    def delete(cls, id):
        connection = cls.create_conn()
        cursor = connection.cursor()

        query = f"DELETE FROM brands WHERE id = {id}"
        cursor.execute(query)

        connection.commit()

        cursor.close()
        connection.close()

    def insert(self):
        connection = self.create_conn()
        cursor = connection.cursor()

        query = f"INSERT INTO brands (name, website, url,created_at, status) " \
                f"VALUES ({repr(self.name)}, {repr(self.website)}, {repr(self.url)}, '{self.created_at}', {self.status})"
        cursor.execute(query)

        connection.commit()

        cursor.close()
        connection.close()

    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getWebsie(self):
        return self.website

    def setWebsite(self, website):
        self.website = website

    def getUrl(self):
        return self.url

    def setUrl(self, url):
        self.url = url

    def getCreatedAt(self):
        return self.created_at

    def setCreatedAt(self, created_at):
        self.created_at = created_at

    def getStatus(self):
        return self.status

    def setStatus(self, status):
        self.status = status

    def updateStatus(self,id,status):
        connection = self.create_conn()
        cursor = connection.cursor()

        query = f"UPDATE brands SET status = {status} WHERE id = {id}"
        print(query)
        cursor.execute(query)

        connection.commit()

        cursor.close()
        connection.close()

