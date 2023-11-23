from datetime import datetime, timedelta
from connector.DatabaseConnector import connector

class Deals:

    @classmethod
    def create_conn(cls):
        return connector.connect()

    @classmethod
    def get_not_bought_cars(cls, days_between, type = 'autoscout', unique = False):
        current_time = datetime.now()
        start_timestamp = int(current_time.timestamp() * 1000)  # Şu anki zamanın timestamp'ini milisaniye cinsinden
        end_timestamp = int((current_time - timedelta(
            days=days_between)).timestamp() * 1000)  # Belirtilen gün kadar önceki zamanın timestamp'i

        if type == 'mobile':
            found = " AND (JSON_EXTRACT(deal_json, '$.found_mobile') IS NULL OR CAST(JSON_UNQUOTE(JSON_EXTRACT(deal_json, '$.found_mobile')) AS UNSIGNED) = 'false') "
        else:
            found = " AND (JSON_EXTRACT(deal_json, '$.found_autoscout') IS NULL OR CAST(JSON_UNQUOTE(JSON_EXTRACT(deal_json, '$.found_autoscout')) AS UNSIGNED) = 'false') "

        group_column, group_by = ("", "")
        if unique:
            group_column = ", CONCAT(deal_car_id, '-', deal_company_id) as duplicat "
            group_by = "GROUP BY duplicat "

        sql = f"""
            SELECT 
                JSON_UNQUOTE(JSON_EXTRACT(car_json,     '$.brand')) as brand,  
                JSON_UNQUOTE(JSON_EXTRACT(car_json,     '$.model')) as model,  
                JSON_UNQUOTE(JSON_EXTRACT(car_json,     '$.km'))    as km,  
                JSON_UNQUOTE(JSON_EXTRACT(car_json,     '$.registration_date'))    as reg_date,  
                JSON_UNQUOTE(JSON_EXTRACT(company_json, '$.autoscoutlink')) as autoscoutLink,  
                JSON_UNQUOTE(JSON_EXTRACT(company_json, '$.mobilelink'))    as mobileLink,
                deal_company_id, deal_car_id, deal_record_id
                {group_column}
            FROM 
                hp_deals as deal
                INNER JOIN hp_company as com ON deal_company_id = company_record_id
                INNER JOIN hp_car     as car ON deal_car_id     = car_record_id
            WHERE 
                CAST(JSON_UNQUOTE(JSON_EXTRACT(deal_json,  "$.carexpress_appointment_date")) AS UNSIGNED) <= '{start_timestamp}'
                AND (
                    CAST(JSON_UNQUOTE(JSON_EXTRACT(deal_json,  "$.dealer_feedback_date")) AS UNSIGNED) >= '{end_timestamp}' OR
                    CAST(JSON_UNQUOTE(JSON_EXTRACT(deal_json,  "$.carexpress_appointment_date")) AS UNSIGNED) >= '{end_timestamp}'
                )
                AND JSON_UNQUOTE(JSON_EXTRACT(deal_json,  "$.dealstage")) IN ("266631100", "266631102")
                {found}
            {group_by}
            ORDER BY company_record_id
        """

        conn = cls.create_conn()
        if conn is not None:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            return cursor.fetchall()
        else:
            return None

    @classmethod
    def get_not_bought_cars_system(cls, days_between, car_type='autoscout', unique=False):
        # Initialize start and end dates
        start_date = datetime.now()
        end_date = datetime.now() - timedelta(days=days_between)

        # Determine the 'found' condition based on car type
        found_condition = "AND found_mobile = 0" if car_type == 'mobile' else "AND found_autoscout = 0"

        # Handle the grouping logic
        group_column = ", CONCAT(da.client_id, '-', da.dealer_id) as duplicat" if unique else ""
        group_by = "GROUP BY duplicat" if unique else ""

        # SQL query construction
        sql = f"""
            SELECT 
                *, da.id as appointmentId {group_column}
            FROM 
                dealer_appointment as da
                INNER JOIN dealer as d ON d.id = da.dealer_id
                INNER JOIN car as car ON car.id = da.client_id
            WHERE 
                da.a_date <= '{start_date.strftime('%Y-%m-%d')}'
                AND (
                    da.f_date >= '{end_date.strftime('%Y-%m-%d')}' OR
                    da.a_date >= '{end_date.strftime('%Y-%m-%d')}'
                )
                AND state IN ('Nicht Angekauft', 'Ausgefallen')
                {found_condition}
            {group_by}
            ORDER BY da.dealer_id
        """

        # Assuming a method to create a database connection
        conn = cls.create_conn()
        if conn is not None:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            return cursor.fetchall()
        else:
            return None