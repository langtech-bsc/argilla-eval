
## A/B test argilla tempalte

Clone this repository and cd.
```bash
git clone git@github.com:langtech-bsc/argilla-eval.git
```

### INSTALLATION
Cd into the repository and download the docker-compose.yaml
```bash
wget -O docker-compose.yaml https://raw.githubusercontent.com/argilla-io/argilla/main/examples/deployments/docker/docker-compose.yaml
```

Deploy the Argilla server locally.
```bash
docker compose up -d
```

Create a venv and install requirements
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### .ENV FILE
Create an .env file with the following variables.

Argilla server requires:
```bash
API_URL=http://localhost:6900
API_KEY=argilla.apikey
```

Depending on the ptoject change them:
```bash
RG_WORKSPACE=eval_workspace
NUMBER_USERS=3
DATASET_NAME=prompts-eval-dataset
DATASET_PATH=dataset.json
```

### USAGE
Once Argilla server is deployed we need to interact with it via sdk.

Run `workspace.py` to create a workspace on the argilla server.
```bash
python workspace.py
```

Run `users.py` to handle users on workspaces.
```bash
python users.py
```
Generated dynamically from `NUMBER_USERS`.
Users and passwords are sotred at root level as`users.csv`

Run `datasets.py` to create and manipulate datasets.
```bash
python datasets.py
```
Datasets are loaded from `/datasets/your_dataset.json`

Run `records` to query and extract records.
```bash
python records.py
```
Rercods are stored at root level as `records.json`


## License
This project is distributed under the Apache-2.0 license. See the [LICENSE](https://github.com/langtech-bsc/argilla-eval/main/LICENSE) file for more information.
