```bash
API_URL=http://localhost:6900
API_KEY=argilla.apikey
```

Once cloned download docker-compose.yaml
```bash
wget -O docker-compose.yaml https://raw.githubusercontent.com/argilla-io/argilla/main/examples/deployments/docker/docker-compose.yaml
```

Deploy the server
```bash
docker compose up -d
```

