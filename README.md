# Remote Node Exporter Agent

This setup runs node_exporter on a monitored host (e.g. EC2).

## Run

docker compose up -d

## Network

Expose port 9100 and allow access only from monitoring server IP.

## Test

curl http://<PUBLIC_IP>:9100/metrics
