
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
	mkdir -p "${PWD}"/kubernetes/k3dvol 
	k3d cluster create social-media-cluster -v "${PWD}"/kubernetes/registry/registries.yaml:/etc/rancher/k3s/registries.yaml -v "${PWD}"/kubernetes/k3dvol:/tmp/k3dvol --agents 2 -p "8082:30080@agent:0"

.PHONY: delete_k3d_cluster
delete_k3d_cluster: ## delete das k3d Cluster.
	k3d cluster delete social-media-cluster
	rm -rf "${PWD}"/kubernetes/k3dvol

.PHONY: start_cluster
start_cluster: tag_push_images_to_registry ## startet die Anwendung.
	kubectl apply -f kubernetes/deployment/frontend-deployment.yaml -n default
	kubectl apply -f kubernetes/services/frontend-service.yaml -n default

.PHONY: stop_cluster
stop_cluster: 
	kubectl delete -f kubernetes/deployment/frontend-deployment.yaml -n default
	kubectl delete -f kubernetes/services/frontend-service.yaml -n default

.PHONY: start_docker_registry
start_docker_registry: ## startet eine Docker Registry, welche im k3d Netzwerk sichtbar ist.
	docker container run -d --network k3d-social-media-cluster --name registry --restart always -p 5000:5000 registry:2

.PHONY: tag_push_images_to_registry
tag_push_images_to_registry: ## uploaded die Docker-Images zur Registry.
	docker tag social-media-platform_frontend:latest localhost:5000/social-media-platform_frontend:latest
	docker push localhost:5000/social-media-platform_frontend:latest


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


