# Challenge 1
At first, you need to install all of the requirements to run the project. So, run:

`pip install -r requirements.txt`

If you want to load historic data from a csv file to an existing table in database, you have to run:

`python historic_data.py departments | jobs | hired_employee`

If you want to do a backup for an existing table in database, you have to run:

`python backup.py departments | jobs | hired_employee`

If you want to restore data for an existing table in database, you have to run:

`python restore.py departments | jobs | hired_employee`

This is the command to run the API in docker:

`docker run -p 5000 globant`
