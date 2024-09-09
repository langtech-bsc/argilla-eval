deploy-on-prem:
	docker compose -f docker-compose-on-prem.yaml --env-file .env up 