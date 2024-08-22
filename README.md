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

Create a venv and install requirements
```bash
python -m venv venv
pip install -r requirements.txt
```

Run the script main.py to interact with the Argilla server
```bash
python main.py
```
