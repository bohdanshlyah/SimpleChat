# Simple chat application
Simple chat aplication which works via websocket


## Running Instructions

### Running via docker-compose
```
docker-compose run —build -d
```
Application frontend [127.0.0.1:8080](127.0.0.1:8080)

### Local running BE
#### Dependencies
* python 3.9
* redis 
* postgresql

Install python requirements
```
cd ./chat-be/
pip install -r requirements.txt
```

Run migrations:
```
python manage.py migrate
```

Run application:
```
python manage.py runserver  0.0.0.0:8000
```

### Local running frontend (FE)

#### Requirements
* node 16

Install node modules
```
npm install
```

Run chat-ui dev application localy:
```
npm run dev
```