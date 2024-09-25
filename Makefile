deploy-on-prem-dev:
	docker compose -f docker-compose-on-prem.yaml --env-file .env up 
deploy-on-prem-production:
	docker compose -f docker-compose-production-on-prem.yaml --env-file .env up 
undeploy-on-prem:
	docker compose -f docker-compose-on-prem.yaml --env-file .env down
stop-on-prem:
	docker compose -f docker-compose-on-prem.yaml --env-file .env stop