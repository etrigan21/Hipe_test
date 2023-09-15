# Installing Dependencies And Running the App

1. Creating env 

```
python3 -m venv env
```

2. Activate the env

```
source env/bin/activate
```

3. Add the necessary configs

```
MONGO_URL="mongodb://127.0.0.1:27017/testDB?authSource=testDB"
DBNAME="testDB"
DBCOLLECTION="events"
```

4. Install Dependencies

```
pip3 install -r requirements.txt
```

5. Run the app

```
python3 main.py
```