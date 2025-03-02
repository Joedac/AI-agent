
UID := $(shell id -u)
GID := $(shell id -g)
DOCKER_COMPOSE := UID=$(UID) GID=$(GID) docker compose

# Cible par défaut
.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  web          Lance l'application en mode web (Streamlit)"
	@echo "  cli          Lance l'application en mode terminal interactif"
	@echo "  build        Construit les images Docker"
	@echo "  clean        Arrête les conteneurs et nettoie les conteneurs orphelins"
	@echo "  rebuild      Nettoie et reconstruit les images puis lance le mode web"
	@echo "  logs         Affiche les logs de l'application web"
	@echo "  setup        Prépare l'environnement (crée le dossier data)"
	@echo "  help         Affiche ce message d'aide"

# Vérifie si le dossier data existe et le crée si nécessaire
.PHONY: setup
setup:
	@mkdir -p data
	@echo "Dossier 'data' configuré"

# Construit les images Docker
.PHONY: build
build: setup
	@echo "Construction des images Docker..."
	@$(DOCKER_COMPOSE) build

# Lance l'application en mode web
.PHONY: web
web: setup
	@echo "Démarrage de l'application en mode Web (Streamlit)..."
	@$(DOCKER_COMPOSE) up ai-agent-web

# Lance l'application en mode web en arrière-plan
.PHONY: web-daemon
web-daemon: setup
	@echo "Démarrage de l'application en mode Web (Streamlit) en arrière-plan..."
	@$(DOCKER_COMPOSE) up -d ai-agent-web

# Lance l'application en mode terminal
.PHONY: cli
cli: setup
	@echo "Démarrage de l'application en mode Terminal..."
	@$(DOCKER_COMPOSE) run --rm ai-agent-cli

# Affiche les logs
.PHONY: logs
logs:
	@$(DOCKER_COMPOSE) logs -f ai-agent-web

# Arrête les conteneurs et nettoie
.PHONY: clean
clean:
	@echo "Arrêt des conteneurs et nettoyage..."
	@$(DOCKER_COMPOSE) down --remove-orphans

# Nettoie et reconstruit
.PHONY: rebuild
rebuild: clean
	@echo "Reconstruction des images Docker..."
	@$(DOCKER_COMPOSE) build --no-cache
	@echo "Démarrage de l'application en mode Web..."
	@$(DOCKER_COMPOSE) up ai-gent-web
