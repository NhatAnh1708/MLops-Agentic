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
	uv run fastapi dev server.py 

