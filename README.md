# Remote Node Exporter Agent
This setup runs node_exporter on a remote agent host (e.g. EC2).

## Network
❗Expose port 9100 and allow access only from monitoring server IP.❗

## Run
```bash
1. git clone -b remote-server --single-branch https://github.com/gasherbrum1/server-monitoring.git
2. docker compose up -d
```

## Test

curl http://<PUBLIC_IP>:9100/metrics
