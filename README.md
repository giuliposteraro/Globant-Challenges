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

First, you need to regist in the api, use this endpoint:

`POST http://127.0.0.1:5000/register`

and in the body, you have to pass a JSON with your username and password like this:

{
    "username": "invited"
    "password": "1234"
}

When you login using `POST http://127.0.0.1:5000/login` and send the same body, you will obtain an access token, 
if you check this token in the page https://jwt.io/ you can see that the decoded is this: 

{
  "typ": "JWT",
  "alg": "HS256"
}


