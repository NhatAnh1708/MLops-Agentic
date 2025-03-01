#!/bin/bash

set -e  # Dừng ngay khi gặp lỗi

echo "🚀 Bắt đầu cài đặt kubens, kubectl, và Terraform trên Ubuntu..."

# Kiểm tra quyền root
if [ "$(id -u)" -ne 0 ]; then
    echo "⚠️ Vui lòng chạy script với quyền root (sudo)!"
    exit 1
fi

echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
sudo apt update
sudo apt-get install google-cloud-sdk-gke-gcloud-auth-plugin
echo "##vso[task.setvariable variable=USE_GKE_GCLOUD_AUTH_PLUGIN]True"

# Cài đặt kubectl
echo "🔹 Đang cài đặt kubectl..."
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
chmod +x kubectl
mkdir -p ~/.local/bin
mv ./kubectl ~/.local/bin/kubectl
kubectl version --client


# Cài đặt kubens & kubectx
echo "🔹 Đang cài đặt kubens & kubectx..."
KUBECTX_DIR="/opt/kubectx"
git clone https://github.com/ahmetb/kubectx.git $KUBECTX_DIR
ln -s $KUBECTX_DIR/kubectx /usr/local/bin/kubectx
ln -s $KUBECTX_DIR/kubens /usr/local/bin/kubens
kubens --help


echo "🔹 Đang cài đặt Helm...."
sudo apt install update -y
sudo snap install helm --classic

# Cài đặt Terraform
echo "🔹 Đang cài đặt Terraform..."
TERRAFORM_VERSION=$(curl -sL https://api.github.com/repos/hashicorp/terraform/releases/latest | grep -oP '"tag_name": "\K(.*?)(?=")')
wget -q https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip
unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip
mv terraform /usr/local/bin/
rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip
terraform version

echo "✅ Cài đặt hoàn tất!"
