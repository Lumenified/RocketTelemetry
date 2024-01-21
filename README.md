# Realtime rocket telemetry with socket. Built with flask and react.

## How to run:
### Backend
Change directory to backend by typing:
```bash
cd ./backend
```
Create the virtualenv in python:
```bash
python -m virtualenv venv
```
Then activate it.
For windows: 
```bash
./venv/Scripts/activate
```
For linux: 
```bash
source ./venv/bin/activate
```
Then install the necessary libraries in virtualenv by typing:
```bash
pip install -r ./requirements.txt
```
Finally:
```bash
python ./app.py
``` 
The project will run on localhost:8080.

### Frontend
Change directory to frontend. You'll install the necessary dependencies by typing:
```bash
npm install
```
To start the react app, type:
```bash
npm start
``` 
The react app will run on localhost:3000.