deploy-on-prem:
	docker compose -f docker-compose-on-prem.yaml --env-file .env up 
undeploy-on-prem:
	docker compose -f docker-compose-on-prem.yaml --env-file .env down
stop-on-prem:
	docker compose -f docker-compose-on-prem.yaml --env-file .env stop