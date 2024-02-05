
# Makefile:18: *** target pattern contains no '%'.  Stop. BEI DIESEM FEHLER SOFORT ANRUFEN (3H Gebraucht mit GPT um das zu lösen..)

####
# Allgemein
####
.PHONY: help
help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_0-9]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help



####
# Kubernetes mit k3d
####
.PHONY: create_k3d_cluster
create_k3d_cluster: ## baut das k3d Cluster.
    # Setzt ein Workdir für Persitant Speicherplatz 
	mkdir -p "${PWD}"/kubernetes/k3dvol 
    # Erstellt das Cluster. Setzt die Registry damit Lokale images depployed werden können, setzt die Persitans und setzt für Agent 0 ein Portforwarding, damit man vom der Localen Machine auf die NodeIP (nicht ClusterIP) des Agendent 0 zugreifen kann, auf dem dann immer das Frontend läuft (siee frontend-deployment.yaml).
	k3d cluster create social-media-cluster -v "${PWD}"/kubernetes/registry/registries.yaml:/etc/rancher/k3s/registries.yaml -v "${PWD}"/kubernetes/k3dvol:/tmp/k3dvol --agents 2 -p "8082:30080@agent:0" -p "8001:30081@agent:0"
    # Setzt dem Agend 0 ein Label, dass verwendet werden kann um dem Persitant zu sagen, auf welchem Node es zu laufen hat. Immer Agend/Node 0 wegen dem Port-Forwarding.
	kubectl label nodes k3d-social-media-cluster-agent-0 node=agent0



.PHONY: delete_k3d_cluster
delete_k3d_cluster: ## delete das k3d Cluster.
	k3d cluster delete social-media-cluster
	rm -rf "${PWD}"/kubernetes/k3dvol

.PHONY: start_cluster
start_cluster: tag_push_images_to_registry ## startet die Anwendung.
    # Deployments hinzufügen
	kubectl apply -f kubernetes/deployment/db-deployment.yaml -n default
	kubectl apply -f kubernetes/deployment/microservice-one-deployment.yaml -n default
	kubectl apply -f kubernetes/deployment/frontend-deployment.yaml -n default
    # Services hinzufügen
	kubectl apply -f kubernetes/services/db-service.yaml -n default
	kubectl apply -f kubernetes/services/microservice_one-service.yaml -n default
	kubectl apply -f kubernetes/services/frontend-service.yaml -n default
    # Persistent hinzufügen
	kubectl apply -f kubernetes/persistens/postgres-data-persistentvolume.yaml -n default
	kubectl apply -f kubernetes/persistens/postgres-data-persistentvolumeclaim.yaml -n default
    # Jobs hinzufügen
	kubectl apply -f kubernetes/jobs/db-init.yaml -n default



.PHONY: stop_cluster
stop_cluster: 
    # Deployments löschen
	kubectl delete -f kubernetes/deployment/db-deployment.yaml -n default
	kubectl delete -f kubernetes/deployment/microservice-one-deployment.yaml -n default
	kubectl delete -f kubernetes/deployment/frontend-deployment.yaml -n default
    # Services löschen
	kubectl delete -f kubernetes/services/db-service.yaml -n default
	kubectl delete -f kubernetes/services/microservice_one-service.yaml -n default
	kubectl delete -f kubernetes/services/frontend-service.yaml -n default
    # Persistent Claims löschen
	kubectl delete -f kubernetes/persistens/postgres-data-persistentvolumeclaim.yaml -n default
    # Persistent löschen
	kubectl delete -f kubernetes/persistens/postgres-data-persistentvolume.yaml -n default
    # Jobs löschen
	kubectl delete -f kubernetes/jobs/db-init.yaml -n default

.PHONY: start_docker_registry
start_docker_registry: ## startet eine Docker Registry, welche im k3d Netzwerk sichtbar ist.
	docker container run -d --network k3d-social-media-cluster --name registry --restart always -p 5000:5000 registry:2

.PHONY: tag_push_images_to_registry
tag_push_images_to_registry: ## uploaded die Docker-Images zur Registry.
	docker tag social-media-platform_frontend:latest localhost:5000/social-media-platform_frontend:latest
	docker push localhost:5000/social-media-platform_frontend:latest
	docker tag social-media-platform_db:latest localhost:5000/social-media-platform_db:latest
	docker push localhost:5000/social-media-platform_db:latest
	docker tag social-media-platform_microservice_one:latest localhost:5000/social-media-platform_microservice_one:latest
	docker push localhost:5000/social-media-platform_microservice_one:latest
	docker tag social-media-platform_db_init:latest localhost:5000/social-media-platform_db_init:latest
	docker push localhost:5000/social-media-platform_db_init:latest


####
# Python mit Conda
####
# .PHONY: create-env
# create-env:
#     @echo "Creating Conda environment..."
#     conda create --name social_media --file requirements.txt
#     @echo "Activating the environment..."
#     conda activate     conda create --name social_media --file requirements.txt
#     @echo "Setting up Visual Studio Code Interpreter..."
#     python -c "import json, os; settings = {'python.pythonPath': os.path.join(os.environ['CONDA_PREFIX'], 'bin', 'python')}; open('.vscode/settings.json', 'w').write(json.dumps(settings))"


