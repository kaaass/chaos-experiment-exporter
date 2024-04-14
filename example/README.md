# Example

This is an example of how to use the chaos-experiment-exporter.

1. Install `chaos-mesh` and `kube-prometheus-stack`.
2. Install `chaos-experiment-exporter`.

```bash
helm install chaos-experiment-exporter ./charts -n=chaos-mesh
```

3. Deploy the example pod.

```bash
kubectl create namespace my-namespace
kubectl apply -f nginx-deployment.yaml
```

4. (Optional) Install Grafana dashboard.
5. Inject a StressChaos to the example pod and check the metrics in Grafana / Prometheus.
