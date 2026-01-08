#!/usr/bin/env bash
set -euo pipefail

# This script is intended for Ubuntu EC2 (apt-based).
# It installs Docker + docker compose plugin, enables Docker at boot,
# and starts node-exporter using the docker-compose.yml in this folder.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ $EUID -eq 0 ]]; then
  echo "Please run as a normal user with sudo (not as root)."
  exit 1
fi

if ! command -v apt-get >/dev/null 2>&1; then
  echo "This installer currently supports Ubuntu/Debian (apt-get)."
  exit 1
fi

echo "==> Updating apt and installing prerequisites..."
sudo apt-get update -y
sudo apt-get install -y ca-certificates curl gnupg lsb-release

if ! command -v docker >/dev/null 2>&1; then
  echo "==> Installing Docker Engine + docker compose plugin..."

  sudo install -m 0755 -d /etc/apt/keyrings
  if [[ ! -f /etc/apt/keyrings/docker.gpg ]]; then
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg
  fi

  UBUNTU_CODENAME="$(. /etc/os-release && echo "${VERSION_CODENAME}")"
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu ${UBUNTU_CODENAME} stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list >/dev/null

  sudo apt-get update -y
  sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
else
  echo "==> Docker already installed."
fi

echo "==> Enabling & starting Docker service..."
sudo systemctl enable docker
sudo systemctl start docker

echo "==> Adding current user to docker group (for future logins)..."
sudo usermod -aG docker "$USER" || true

echo "==> Starting node-exporter (docker compose)..."
sudo docker compose -f "${SCRIPT_DIR}/docker-compose.yml" up -d

echo ""
echo "Done. node-exporter should be listening on port 9100."
echo "If 'docker' without sudo fails later, log out and back in (group refresh)."
