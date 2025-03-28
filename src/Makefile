# Makefile for the MLops-Agentic project


# Scripts for the Supabase
clone-supabase:
	@ls
	@echo "Cloning Supabase..."
	bash ./scripts/clone-supabase.sh

run-supabase:
	@echo "Running Supabase..."
	cd storage/supabase/docker
	docker compose up -d

stop-supabase:
	@echo "Stopping Supabase..."
	cd storage/supabase/docker
	docker compose down


# Scripts for fastapi
dev:
	uv run uvicorn server:app --reload


docker-prune:
	docker system prune
docker-amd64:
	docker build -t danny1708/ai-agent-service . --platform linux/amd64
docker-m1: docker-prune
	docker build -t danny1708/ai-agent-service-m1 .

prod: docker-m1
	docker run \
  --env-file .env \
  -p 30000:30000 \
  danny1708/ai-agent-service-m1
stop:
	docker stop ai-agent-service

prune:
	docker system prune

vnc:
	docker run --platform linux/amd64 -d -p 5901:5901 -p 6901:6901 -p 4444:4444 --user root accetto/xubuntu-vnc-novnc-chrome

vnc-connect:
	ssh -p 5901 root@localhost

vnc-stop:
	docker stop $(docker ps -q --filter ancestor=consol/rocky-xfce-vnc)

help:
	@echo "Makefile for the MLops-Agentic project"
	@echo "Usage:"
	@echo "  make dev        - Start the development environment"
	@echo "  make docker     - Build the Docker container"
	@echo "  make prod       - Start the production environment in Docker"
	@echo "  make stop       - Stop all running Docker containers for this project"
	@echo "  make prune      - Remove all unused Docker containers, networks, and images"
	@echo "  make vnc        - Start a VNC server for remote desktop access"
	@echo "  make vnc-connect - Connect to the running VNC server"
	@echo "  make vnc-stop   - Stop the running VNC server"
	@echo "  make help       - Display this help message"
