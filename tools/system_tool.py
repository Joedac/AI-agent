import datetime
import platform
import matplotlib.pyplot as plt
import psutil
from smolagents import tool


class SystemMonitorTool:
    """Outil pour surveiller et rapporter l'état du système"""

    @staticmethod
    @tool
    def get_system_info() -> str:
        """
        Retrieves and saves system information.

        Returns:
            System Status Report or error
        """
        try:
            system_info = platform.uname()
            cpu_info = {
                "utilisation": psutil.cpu_percent(interval=1),
                "coeurs_physiques": psutil.cpu_count(logical=False),
                "coeurs_total": psutil.cpu_count(logical=True),
            }

            memory = psutil.virtual_memory()

            disk = psutil.disk_usage("/")

            boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.datetime.now() - boot_time

            network = psutil.net_io_counters()

            report = f"""RAPPORT SYSTÈME - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SYSTÈME:
  OS: {system_info.system} {system_info.release}
  Version: {system_info.version}
  Machine: {system_info.machine}
  Processeur: {system_info.processor}

CPU:
  Utilisation: {cpu_info['utilisation']}%
  Coeurs physiques: {cpu_info['coeurs_physiques']}
  Coeurs logiques: {cpu_info['coeurs_total']}

MÉMOIRE:
  Total: {memory.total / (1024 ** 3):.2f} GB
  Disponible: {memory.available / (1024 ** 3):.2f} GB
  Utilisée: {memory.used / (1024 ** 3):.2f} GB ({memory.percent}%)

DISQUE:
  Total: {disk.total / (1024 ** 3):.2f} GB
  Libre: {disk.free / (1024 ** 3):.2f} GB
  Utilisé: {disk.used / (1024 ** 3):.2f} GB ({disk.percent}%)

TEMPS DE FONCTIONNEMENT:
  Démarré le: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}
  En fonctionnement depuis: {str(uptime).split('.')[0]}

RÉSEAU:
  Octets envoyés: {network.bytes_sent / (1024 ** 2):.2f} MB
  Octets reçus: {network.bytes_recv / (1024 ** 2):.2f} MB
            """

            # Créer un graphique d'utilisation des ressources
            fig, axs = plt.subplots(2, 1, figsize=(10, 8))

            axs[0].bar(["CPU"], [cpu_info["utilisation"]], color="blue")
            axs[0].set_ylim(0, 100)
            axs[0].set_ylabel("Utilisation (%)")
            axs[0].set_title("Utilisation CPU")

            resources = ["Mémoire", "Disque"]
            usage = [memory.percent, disk.percent]
            axs[1].bar(resources, usage, color=["orange", "green"])
            axs[1].set_ylim(0, 100)
            axs[1].set_ylabel("Utilisation (%)")
            axs[1].set_title("Utilisation Mémoire et Disque")

            plt.tight_layout()

            chart_filename = f"files/ressources_systeme_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(chart_filename)
            plt.close()

            return f"{report}\n\nRapport enregistré dans {output_filename}\nGraphique enregistré dans {chart_filename}"

        except Exception as e:
            return f"Erreur lors de la récupération des informations système: {str(e)}"
