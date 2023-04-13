from sqlalchemy import create_engine, text
import pandas as pd
import logging

engine = create_engine('sqlite:///globant.db')
logging.basicConfig(filename='LOGS/view2.log', level=logging.ERROR, format="%(asctime)s %(levelname)s %(message)s")
with engine.connect() as connection:
        try: 
            query = '''CREATE VIEW view_req2 AS
            WITH avg_monthly_hires AS (
                            SELECT 
                                department_id, 
                                COUNT(*)/12 AS AvgMonthlyHires
                            FROM 
                                hired_employee
                            WHERE 
                                substr(datetime,1,4) = '2021' 
                            GROUP BY 
                                department_id
                            ), 
                            DepartmentHires AS (
                                SELECT 
                                    d.id, 
                                    d.name, 
                                    COUNT(*) AS num_employees_hired
                                FROM 
                                    hired_employee e
                                JOIN 
                                    departments d ON e.department_id = d.id
                                WHERE 
                                    substr(datetime,1,4) = '2021' 
                                GROUP BY 
                                    d.id, d.name
                            )
                            SELECT 
                            dh.id, 
                            dh.name, 
                            dh.num_employees_hired
                            FROM 
                            DepartmentHires dh
                            JOIN 
                            avg_monthly_hires ah ON dh.id = ah.department_id
                            WHERE 
                            dh.num_employees_hired > ah.AvgMonthlyHires
                            ORDER BY 
                            dh.num_employees_hired DESC;'''
            df = pd.read_sql_query(text(query), connection)
        except Exception as e:
              logging.error(str(e))
              raise Exception("The view exists in database, for more information please read the corresponding log in LOGS folder")


