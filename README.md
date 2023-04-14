# Challenge 1
At first, you need to install all of the requirements to run the project. So, run:

`pip install -r requirements.txt`

## Historic Data
If you want to load historic data from a csv file to an existing table in database, you have to run:

`python historic_data.py departments | jobs | hired_employee`

## Backup

If you want to do a backup for an existing table in database, you have to run:

`python backup.py departments | jobs | hired_employee`

## Restore

If you want to restore data for an existing table in database, you have to run:

`python restore.py departments | jobs | hired_employee`

## Run API in Docker

First, create the image running:

`docker build -t globant .`

This is the command to run the API in docker:

`docker run -p 8080:5000 globant`

## Endpoints

First, you need to regist in the api, use this endpoint:

`POST http://localhost:8080/register`

and in the body, you have to pass a JSON with your username and password like this:

{
    "username": "invited"
    "password": "1234"
}

When you login using `POST http://localhost:8080/login` and send the same body, you will obtain an access token, 
if you check this token in the page https://jwt.io/ you can see that the decoded is this: 

{
  "typ": "JWT",
  "alg": "HS256"
}

Then, in the file "Globant.postman_collection.json" you can find examples of endpoints that you can run.

# Challenge 2

Run `GET http://localhost:8080/requirement1` to obtain the first requirement result. In addition, when you run this command, it generates a csv file with the result with the name "result_req1.csv" in this repository

Run `GET http://localhost:8080/requirement2` to obtain the second requirement result. As the same of the requirement 1, it generates a csv file with the result with the name "result_req2.csv"
