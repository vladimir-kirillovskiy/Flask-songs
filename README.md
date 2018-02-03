# Rest Api with Python, Flask and Mongodb

Simple Api with single page frontend. Frontend located here: https://github.com/vladimir-kirillovskiy/Flask-songs-frontend

# Installation Instructions:

  - Create an api folder
    ```sh
    $ mkdir api && cd api
    ```
  - Create virtualenv
    ```sh
    $ virtualenv env
    ```
  - Activate virtualenv
    ```sh
    $ source env/bin/activate
    ```
  - Clone git repo and go to the new directory
    ```sh
    $ git clone https://github.com/vladimir-kirillovskiy/Flask-songs.git api
    $ cd api
    ```
  - Install required packages
    ```sh
    $ pip install -r requirements.txt
    ```
  - Import songs collection, this will create new db as well
    ```sh
    $ mongoimport --db rest_api --collection songs --drop --file songs.json
    ```
  - Create rating table
    ```sh
    $ mongo
    > db.createCollection('ratings')
    > exit
    ```
  - Run app, this should create dev server on 127.0.0.1:5000 
    ```sh
    $ python main.py
    ```
  - In the second terminal window clone frontend repository on the same level as api folder
    ```sh
    $ git clone https://github.com/vladimir-kirillovskiy/Flask-songs-frontend frontend
    $ cd frontend
    ```
  - Open index.html file in browser
  - Or you can use Postman program to send requests to 127.0.0.1:5000