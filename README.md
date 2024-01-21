# Realtime rocket telemetry with socket. Built with flask and react.

## How to run:
### Backend
Change directory to backend by typing **"cd ./backend"**. Create the virtualenv in python **"python -m virtualenv venv"** then activate it (for windows: **"./venv/Scripts/activate"** for linux: **"source ./venv/bin/activate"**) then install the necessary libraries in virtualenv by typing **"pip install -r ./requirements.txt."**. Finally **"python ./app.py"**. The project will run on localhost:8080.

### Frontend
Change directory to frontend. By typing **"npm install"** you'll install the dependencies into node_modules folder (currently ignored by .gitignore file). Then type **"npm start"**. The react app will run on localhost:3000.