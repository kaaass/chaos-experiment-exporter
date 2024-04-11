import os
import requests


API_LIST_POD = "/api/common/pods"
API_LIST_EXPERIMENTS = "/api/experiments"
API_GET_EXPERIMENT = "/api/experiments/{uid}"
API_GET_COMMON_CONFIG = "/api/common/config"

API_HOST = os.getenv("API_HOST", None)
API_ACCESS_TOKEN = os.getenv("API_ACCESS_TOKEN", None)


def get_host() -> str:
    if API_HOST is None:
        raise ValueError("API_HOST must be configured to chaos-dashboard!")
    return API_HOST


def get_access_token() -> str:
    if API_ACCESS_TOKEN is not None:
        return API_ACCESS_TOKEN

    # read sa token if env not specified
    sa_file = "/var/run/secrets/kubernetes.io/serviceaccount/token"
    if os.path.exists(sa_file):
        with sa_file.open("r") as f:
            return f.read()

    raise ValueError("API_ACCESS_TOKEN or service account must be configured")


def request_api(endpoint: str, method: str, json_data: dict = None) -> dict:
    headers = {
        "Authorization": "Bearer " + get_access_token(),
        "Content-Type": "application/json",
    }
    method_func = {
        "GET": requests.get,
        "POST": requests.post,
        "PUT": requests.put,
        "DELETE": requests.delete,
    }[method]
    url = get_host() + endpoint
    response = method_func(url, headers=headers, json=json_data)
    return response.json()


def list_pod(selector: dict) -> list:
    """List all pods in cluster by selector."""
    return request_api(API_LIST_POD, "POST", selector)


def list_experiments() -> list:
    """List all experiments summary in cluster."""
    return request_api(API_LIST_EXPERIMENTS, "GET")


def get_experiment(uid: str) -> dict:
    """Get experiment detail by uid. uid can be retrieved by `list_experiments`."""
    return request_api(API_GET_EXPERIMENT.format(uid=uid), "GET")


def get_common_config() -> dict:
    """Get common config of chaos-dashboard instance."""
    return request_api(API_GET_COMMON_CONFIG, "GET")


def _test():
    selector = {
        "namespaces": ["my-namespace"],
        "labelSelectors": {"app": "nginx"},
        "annotationSelectors": {},
    }
    pods = list_pod(selector)
    print(pods)

    experiments = list_experiments()
    print(experiments)

    experiment = get_experiment(experiments[0]["uid"])
    print(experiment)


if __name__ == "__main__":
    _test()
