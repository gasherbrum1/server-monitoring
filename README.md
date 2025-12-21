## Simple  live server monitoring dashboard stack.

Fully Dockerized server monitoring stack + dashboard using **Prometheus + Grafana + Node Exporter** to monitor Linux host CPU/RAM/Disk/Network.

✅ Easily deployable
✅ Persists after reboot
✅ Works on any modern Linux system

## How it works?
You (User) / Browser -> Grafana -> Prometheus -> Node Exporter -> Linux Host Metrics

## What do you need to replicate?
-> Linux, Git, Docker

## How to replicate & run?
```bash
1. git clone https://github.com/gasherbrum1/server-monitoring.git
2. cd server-monitoring
3. docker compose up -d
-> Wait for the stack to start
4. docker compose logs show-host-ip
-> You should see:
show-host-ip  | Grafana available at:
show-host-ip  | http://Your server IP:3000
show-host-ip  | http://:3000

```
### On any device on the same LAN network as your Linux server, you can input " http:// Your server IP:3000 " to see Grafana:
-> Grafana will load -> Dashboards -> Node Exporter Full

Congratulations! Your dashboard should now be ready to go and persist after restart

❗**NOTE** You can always edit the .env file located in the /server-monitoring dir with your own variables. The one pushed on this repo is purely for example and replicability.❗
