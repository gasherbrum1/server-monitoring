# Linux server live monitoring and dashboard stack (CPU, RAM, Disk usage + Uptime)

This project is designed primarily around AWS EC2 instances within the AWS Free Tier which have dynamic IPs, however any Linux target can work.

**❗** 9100 TCP must be exposed towards the monitoring host public IP in order for metrics to be scraped.

**❗** The stack also supports local host metrics collection.

## Architecture

The project uses a central monitoring server and one or more remote target hosts.

                   +-------------------------+
                   |     Central  Host       |
                   |      (main branch)      |
                   |                         |
                   |  +-------------------+  |
                   |  |    Prometheus     |<--------------------+
                   |  +-------------------+  |                    |
                   |           |             |                    |
                   |           v             |                    |
                   |  +-------------------+  |                    |
                   |  |     Grafana       |  |                    |
                   |  +-------------------+  |                    |
                   |                         |                    |
                   |  +-------------------+  |                    |
                   |  |  Node Exporter    |--+                    |
                   |  |   (local) :9100   |                       |
                   |  +-------------------+                       |
                   +-------------------------+                    |
                                                                  |
              +-------------------------------------------+       |
              |           Remote Target Host(s)           |       |
              |         (remote-agent branch)             |       |
              |                                           |       |
              |     +-------------------------------+     |       |
              |     |        Node Exporter :9100     |-----+-------+
              |     +-------------------------------+     |
              |                Linux Server                |
              +-------------------------------------------+

Data Flow:
Node Exporter(s)  -->  Prometheus  -->  Grafana

## Installation

❗**Prerequisites** ❗
- Central host: Linux, Git, Docker
- Remote server: Linux, Git, TCP Port 9100 exposed to host public IP

### Step 1: 
Install the central monitor on your Linux host. You just need to follow the instructions on this README.

#### Central monitoring stack consists of: 
- Prometheus
- Grafana
- Node Exporter (for local metrics)

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
From this point, you can open Grafana at "http://XXXXXXXXXX:3000" -> Navigtate to Dashboards -> Node Exporter Full.
- Change job to "manual" to see remote agents and to "node-exporter" to see local host metrics.

### Step 2: 
Install the remote agent. You can  switch to the **remote server** branch and check out the contents of that repo or just follow below:

```bash
1. git clone -b remote-server --single-branch https://github.com/gasherbrum1/server-monitoring.git
2. docker compose up -d
-> Wait for the stack to start and your Node Exporter should be ready to scrape and send.
```

### Step 3:
Let's now connect the host to the remote agent. On the host, follow the commands:

```bash
1. docker compose run --rm monitorctl
-> You will get prompted to input the Public IP of the remote server you installed the remote agent on.
-> Input the IP. It should now be added to Prometheus and pickec up by Grafana.
-> "http://XXXXXXXXXX:9090" to debug hosts connected to Prometheus.
```
Voila! Your should now be able to remotely monitor multiple instances from your central monitor host. Whenever you want to add a new IP to monitor just run "docker compose run --rm monitorctl" again and follow the input.

**Final notes and clarifications**
- This project is intended for homelabs and learning environments. Do not expose the monitoring host to the public internet. Access to Grafana should remain restricted to LAN or VPC networks.
- The .env file in the repository is provided only as an example for replicability. You should never commit real .env files containing secrets.
- Registered IPs do not persist after docker compose down or container rebuilds. This is intentional and aligns with the project goal of monitoring instances with dynamic IP addresses. When IPs change or containers are recreated, simply re-run:



