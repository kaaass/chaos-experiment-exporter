import os
import sys
import traceback
from prometheus_client import start_http_server, Gauge
import time
import api


CHAOS_EXPERIMENT = Gauge(
    "chaos_experiment",
    "Description of chaos_experiment",
    ["exp_uuid", "exp_name", "exp_type", "namespace", "pod"],
)


def check_api():
    """Check if chaos-dashboard API is available."""
    try:
        config = api.get_common_config()
        print(f"Connected to chaos-dashboard API, server version: {config['version']}")
    except Exception:
        print(f"Failed to connect to chaos-dashboard API")
        traceback.print_exc()
        sys.exit(1)


def update_metrics():
    """Update metrics from chaos-dashboard API."""
    for experiment in api.list_experiments():
        detail = api.get_experiment(experiment["uid"])
        # list injected pods by selector in spec
        # FIXME: current select result may differ from the actual injected pods
        selector = detail.get("kube_object", {}).get("spec", {}).get("selector", {})
        pods = api.list_pod(selector)
        for pod in pods:
            CHAOS_EXPERIMENT.labels(
                exp_uuid=experiment["uid"],
                exp_name=experiment["name"],
                exp_type=experiment["kind"],
                namespace=pod["namespace"],
                pod=pod["name"],
            ).set(1)


if __name__ == "__main__":
    print("Checking chaos-dashboard API...")
    check_api()

    port = int(os.getenv("PORT", 8000))
    start_http_server(port)
    print(f"Prometheus exporter is running on port {port}")

    while True:
        update_metrics()
        # Update every 5 seconds
        time.sleep(5)
