from sqlalchemy import create_engine, text
import pandas as pd
import logging

engine = create_engine('sqlite:///globant.db')
logging.basicConfig(filename='LOGS/view1.log', level=logging.ERROR, format="%(asctime)s %(levelname)s %(message)s")
with engine.connect() as connection:
        try:
            query = '''CREATE VIEW view_req1 AS
                        SELECT d.name as Department, j.job as Job, 
                        COUNT(CASE 
                            WHEN substr(he.datetime,6,2) IN ('01', '02', '03') THEN he.id END) AS Q1, 
                        COUNT(CASE 
                            WHEN substr(he.datetime,6,2) IN ('04', '05', '06') THEN he.id END) AS Q2, 
                        COUNT(CASE 
                            WHEN substr(he.datetime,6,2) IN ('07', '08', '09') THEN he.id END) AS Q3, 
                        COUNT(CASE 
                            WHEN substr(he.datetime,6,2) IN ('10', '11', '12') THEN he.id END) AS Q4
                    FROM hired_employee he
                    JOIN jobs j ON he.jobs_id = j.id
                    JOIN departments d ON he.department_id = d.id
                    WHERE substring(he.datetime, 1, 4) = '2021'
                    GROUP BY d.name, j.job 
                    ORDER BY d.name, j.job DESC'''
            df = pd.read_sql_query(text(query), connection)
        except Exception as e:
              logging.error(str(e))
              raise Exception("The view exists in database, for more information please read the corresponding log in LOGS folder")
