Create an .env file with the following variables
```bash
API_URL=http://localhost:6900
API_KEY=argilla.apikey
```

Once cloned download docker-compose.yaml
```bash
wget -O docker-compose.yaml https://raw.githubusercontent.com/argilla-io/argilla/main/examples/deployments/docker/docker-compose.yaml
```

Deploy the Argilla server locally
```bash
docker compose up -d
```

Once Argilla server is deployed we need to create a virtual environment to interact with the server via the sdk.

Create a venv and install requirements
```bash
python -m venv venv
pip install -r requirements.txt
```

Run `main.py` to create a workspace on the argilla server.
```bash
python main.py
```

Run `users.py` to handle users on workspaces.
```bash
python users.py
```

Run `datasets.py` to manipulate datasets.
```bash
python datasets.py
```

Run `records` to query and extract records.
```bash
python records.py
```
