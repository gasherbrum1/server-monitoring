# Linux server live monitoring and dashboard stack 

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

❗**Prerequisites** -> Linux, Git, Docker❗

### Step 1: 
Install the central monitor on your Linux host. You just need to follow the instructions on this README, on the **main** branch.

### Central monitoring stack consists of: 
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

### Step 2: 
Install the remote agent. From this point you'll need to switch to the **remote agent** branch and follow the instructions over there.

