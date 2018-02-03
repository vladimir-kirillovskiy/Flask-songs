# Rest Api with Python, Flask and Mongodb

Simple Api with single page frontend located here: https://github.com/vladimir-kirillovskiy/Flask-songs-frontend

# Installation Instructions:
- Clone frontend git repo
```sh
git clone https://github.com/vladimir-kirillovskiy/Flask-songs-frontend frontend
```
- Create an api folder
```sh
mkdir api && cd api
```
- Create virtualenv
```sh
virtualenv env
```
- Activate virtualenv
```sh
source env/bin/activate
```
- Clone git repo and go to the new directory
```sh
git clone https://github.com/vladimir-kirillovskiy/Flask-songs.git api
```
- Install required packages
```sh
pip install -r requirements.txt
```
- Import songs collection, this will create new db as well
```sh
mongoimport --db rest_api --collection songs --drop --file songs.json
```
- Create rating table
```sh
mongo
>db.createCollection('ratings')
```
- Run app
```sh
python main.py
```