from connector.DatabaseConnector import connector


class Models:
    def __init__(self, id = None, name = None, brand_id = None, url = None, created_at = None, status = None):
        self.id = id
        self.name = name
        self.brand_id = brand_id
        self.url = url
        self.created_at = created_at
        self.status = status

    @classmethod
    def create_conn(cls):
        return connector.connect()

    @classmethod
    def getAll(cls):
        connection = cls.create_conn()
        cursor = connection.cursor()

        query = f"SELECT m.id, m.name, b.url as brand_id, m.url, m.created_at, m.status " \
                f"FROM models AS m " \
                f"INNER JOIN brands AS b ON b.id = m.brand_id"

        cursor.execute(query)
        results = cursor.fetchall()

        models = []
        for result in results:
            id, name, brand_id, url, created_at, status = result
            model = Models(id, name, brand_id, url, created_at, status)
            models.append(model)

        return models

    @classmethod
    def selectById(cls, id):
        connection = cls.create_conn()
        cursor = connection.cursor()

        query = f"SELECT * FROM models WHERE id = {id}"
        cursor.execute(query)

        result = cursor.fetchone()

        id, name, brand_id, url, created_at, status = result
        model = Models(id, name, brand_id, url, created_at, status)

        cursor.close()
        connection.close()

        return model

    @classmethod
    def get_by_name(cls, name, brand_id):
        connection = cls.create_conn()
        cursor = connection.cursor()

        query = f"""
            SELECT 
                * 
            FROM 
                models 
            WHERE 
                name LIKE '{name}'
            AND 
                brand_id = '{brand_id}'
            LIMIT 1
        """
        cursor.execute(query)

        result = cursor.fetchone()

        if result is not None:
            id, name, brand_id, url, created_at, status = result
            model = Models(id, name, brand_id, url, created_at, status)
        else:
            model = None

        cursor.close()
        connection.close()

        return model

    @classmethod
    def get_by_name_like(cls, name, brand_id):
        connection = cls.create_conn()
        cursor = connection.cursor()

        query = f"""
               SELECT 
                   * 
               FROM 
                   models 
               WHERE 
                   name LIKE '%{name}%'
               AND 
                   brand_id = '{brand_id}'
               LIMIT 1
           """
        cursor.execute(query)

        result = cursor.fetchone()

        if result is not None:
            id, name, brand_id, url, created_at, status = result
            model = Models(id, name, brand_id, url, created_at, status)
        else:
            model = None

        cursor.close()
        connection.close()

        return model

    @classmethod
    def getByUrl(cls, brand_id):
        connection = cls.create_conn()
        cursor = connection.cursor()

        query = f"SELECT * FROM brands WHERE brand_id = '{brand_id}' LIMIT 1"
        cursor.execute(query)

        result = cursor.fetchone()

        if result:
            id, name, brand_id, url, created_at, status = result
            model = Models(id, name, brand_id, url, created_at, status)
        else:
            model = None

        cursor.close()
        connection.close()

        return model

    @classmethod
    def getAllByBrandId(cls, brand_id):
        connection = cls.create_conn()
        cursor = connection.cursor()

        query = f"SELECT * FROM models WHERE brand_id = {brand_id} AND status = 1"
        cursor.execute(query)
        results = cursor.fetchall()

        models = []
        for result in results:
            id, name, brand_id, url, created_at, status = result
            model = Models(id, name, brand_id, url, created_at, status)
            models.append(model)
        return models
    @classmethod
    def delete(cls, id):
        connection = cls.create_conn()
        cursor = connection.cursor()

        query = f"DELETE FROM models WHERE id = {id}"
        cursor.execute(query)

        connection.commit()

        cursor.close()
        connection.close()

    def insert(self):
        connection = self.create_conn()
        try:
            cursor = connection.cursor()

            query = f"INSERT INTO models (name, brand_id, url, created_at, status) " \
                    f"VALUES ({repr(self.name)}, '{self.brand_id}', {repr(self.url)}, '{self.created_at}', {self.status})"
            cursor.execute(query)

            connection.commit()
        except Exception as e:
            print(f"An error occurred while inserting data: {e}")
        finally:
            cursor.close()
            connection.close()


    def updateStatus(self,id,status):
        connection = self.create_conn()
        cursor = connection.cursor()

        query = f"UPDATE models SET status = {status} WHERE id = {id}"
        print(query)
        cursor.execute(query)

        connection.commit()

        cursor.close()
        connection.close()
    def update(self):
        connection = self.create_conn()
        cursor = connection.cursor()

        query = f"UPDATE models SET name = '{self.name}', brand_id = '{self.brand_id}', url = '{self.url}', status = {self.status} WHERE id = {self.id}"
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

    def getBrandId(self):
        return self.brand_id

    def setBrandId(self, brand_id):
        self.brand_id = brand_id

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

