
UID := $(shell id -u)
GID := $(shell id -g)
DOCKER_COMPOSE := UID=$(UID) GID=$(GID) docker compose

.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  web          Lance l'application en mode web"
	@echo "  cli          Lance l'application en mode terminal interactif"
	@echo "  build        Construit les images Docker"
	@echo "  clean        Arrête les conteneurs et nettoie les conteneurs orphelins"
	@echo "  rebuild      Nettoie et reconstruit les images puis lance le mode web"
	@echo "  logs         Affiche les logs de l'application web"
	@echo "  setup        Prépare l'environnement (crée le dossier files)"
	@echo "  help         Affiche ce message d'aide"

.PHONY: setup
setup:
	@mkdir -p files
	@echo "Dossier 'files' configuré"

.PHONY: build
build: setup
	@echo "Construction des images Docker..."
	@$(DOCKER_COMPOSE) build

.PHONY: web
web: setup
	@echo "Démarrage de l'application en mode Web..."
	@$(DOCKER_COMPOSE) up ai-agent-web

.PHONY: web-daemon
web-daemon: setup
	@echo "Démarrage de l'application en mode Web en arrière-plan..."
	@$(DOCKER_COMPOSE) up -d ai-agent-web

.PHONY: cli
cli: setup
	@echo "Démarrage de l'application en mode CLI..."
	@$(DOCKER_COMPOSE) run --rm ai-agent-cli

.PHONY: logs
logs:
	@$(DOCKER_COMPOSE) logs -f ai-agent-web

.PHONY: clean
clean:
	@echo "Arrêt des conteneurs et nettoyage..."
	@$(DOCKER_COMPOSE) down --remove-orphans

.PHONY: rebuild
rebuild: clean
	@echo "Reconstruction des images Docker..."
	@$(DOCKER_COMPOSE) build --no-cache
	@echo "Démarrage de l'application en mode Web..."
	@$(DOCKER_COMPOSE) up ai-gent-web
