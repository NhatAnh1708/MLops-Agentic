# Real-time-Agentic-MLops

A MLops pipeline for real-time agentic system.

[![Architecture](./assets/images/Architecture-realtime.png)](./assets/images/Architecture-realtime.png)

## Introduction

TBD

## Table of Contents

- [1. Introduction](#introduction)
- [2. Key Features](#key-features)
- [3. Project Structures](#project-structures)
- [4. Overall Architecture](#architecture)
- [5. Getting Started](#getting-started)
    - [5.1. Development stage](#development-stage)
        - [5.1.1. Set up environments](#set-up-environments)
            - [5.1.2. Install uv](#install-uv)
            - [5.1.3. Install libraries and dependencies](#install-libraries)
            - [5.1.4. Install docker](#install-docker)
        - [5.1.5. Inference FastAPI app](#inference-fastapi-app)
            - [5.1.6. Inference in localhost](#inference-in-localhost)
            - [5.1.7. Inference in Docker container](#inference-in-docker-container)
        - [5.1.8. Log and trace with laminar](#set-up-laminar-development)
    - [5.2. Production stage](#production-stage)
        - [5.2.1. Set up](#9-set-up)
            - [5.2.2. Set up Google Cloud Platform (GCP)](#91-set-up-gcp)
                - [5.2.2.1. Create a project in Google Cloud Platform (GCP)](#911-create-a-project-in-gcp)
                - [5.2.2.2. Enabling the Kubernetes Engine API](#912-enabling-the-kubernetes-engine-api)
                - [5.2.2.3. Install and setup Google Cloud CLI](#913-install-and-setup-google-cloud-cli)
                - [5.2.2.4. Install gke-cloud-auth-plugin](#914-install-gke-cloud-auth-plugin)
                - [5.2.2.5. Create a service account](#915-create-a-service-account)
            - [5.2.3. Install Terraform](#92-install-terraform)
            - [5.2.4. Install kubectl, kubectx and kubens](#93-install-kubectl-kubectx-and-kubens)
            - [5.2.5. Install helm](#94-install-helm)
        - [5.2.6. Using Terraform for Google Kubernetes Engine (GKE)](#using-terraform-for-google-kubernetes-engine-gke)
            - [5.2.6.1. Set up the cluster](#set-up-the-cluster)
            - [5.2.6.2. Retrive the cluster information](#retrive-cluster-information)
        - [5.2.7. Deployment to Google Kubernetes Engine (GKE)](#deployment-to-gke)
            - [5.2.7.1. Configure API Key Secret](#configure-api-key-secret)
            - [5.2.7.2. Deploy Nginx-Ingress controller](#deploy-nginx-ingress-controller)
            - [5.2.7.3. Deploy FastAPI controller](#deploy-fastapi-controller)
            - [5.2.7.4. Deploy Monitoring controller](#deploy-monitoring-controller)

        - [5.2.8. Continuous Integration/Continuous Deployment (CI/CD) with Ansible and Jenkins](#continuous-integrationcontinuous-deployment-cicd-with-travis-ci)
            - [5.2.8.1. Set up Jenkins Server](#set-up-travis-ci-server)
            - [5.2.8.2. Access Jenkins](#access-travis-ci)
            - [5.2.8.3. Install Jenkins Plugins](#install-travis-ci-plugins)
            - [5.2.8.4. Configure Jenkins](#configure-travis-ci)
            - [5.2.8.5. Test the setup](#test-the-travis-ci-setup)
        - [5.2.9. Log and trace with Laminar](#set-up-laminar-production)
        - [5.2.10. Monitoring with Prometheus and Gafana](#monitoring-with-prometheus-and-gafana)
            - [5.2.10.1. Quick start](#quick-start)
            - [5.2.10.2. Test the setup](#test-the-monitoring-setup)


- [6. Contributing](#contributing)
- [7. License](#license)
- [8. Citations](#citations)
- [9. Contact](#contact)

## Project Structures
Using project structures of [LLM-Kit](https://engineering.grab.com/supercharging-llm-application-development-with-llm-kit)
```
.
├── README.md
├── assets
│   ├── images
│   │   ├── Architecture-realtime.png
│   └── videos
├── notebooks
│   ├── data
│   ├── janus-poc
│   └── poc
│       ├── README.md
│       ├── downloads
│       │   └── dummy.pdf
│       ├── index copy.py
│       ├── index.html
│       ├── index.py
│       ├── main.py
│       ├── pcm-processor.js
│       ├── pyproject.toml
│       ├── static
│       │   └── js
│       │       └── chat.js
│       ├── storage
│       │   ├── default__vector_store.json
│       │   ├── docstore.json
│       │   ├── graph_store.json
│       │   ├── image__vector_store.json
│       │   └── index_store.json
│       └── uv.lock
└── src
    ├── Dockerfile
    ├── LICENSE
    ├── Makefile
    ├── __init__.py
    ├── agent
    │   ├── base_agent.py
    │   ├── gemini_agent.py
    │   ├── helper
    │   │   ├── dummy_data.json
    │   │   └── google_search.py
    │   ├── nvidia_agent.py
    │   └── pydantic_ai_agent.py
    ├── auth
    ├── core
    ├── frontend
    │   ├── index.html
    │   └── pcm-processor.js
    ├── models
    │   ├── action.py
    │   ├── authentication.py
    │   ├── base.py
    │   ├── google_search.py
    │   ├── history.py
    │   └── message.py
    ├── pyproject.toml
    ├── routes
    │   ├── health.py
    │   ├── index.py
    │   └── websocket.py
    ├── scripts
    │   └── clone-supabase.sh
    ├── server.py
    ├── storage
    ├── tools
    ├── travis-ci.yml
    ├── utils
    └── uv.lock
```





## Key features

- Sử dụng Websocket trong giao thức kết nối của chatbox, cải thiện độ trễ và tăng trải nghiệm người dùng.
- Rất dễ sử dụng với các khả năng scalability and flexibility, tùy chỉnh API giúp tiếp cận nhiều mô hình mới nhất. Khả năng triển khai nhanh chóng với một câu lệnh là có thể trải nghiệm được một hệ thống AI Agent hoàn chỉnh.
- Tối ưu chi phí vận hành xuống mức thấp nhất đối với một doanh nghiệp nhỏ (hoàn toàn có thể miễn phí nếu dưới 2500 requests/month).
- ...

## Getting Started

### Development Stage

#### Set up environments

> Before set up the enviroment, make sure your machine meets the following minimum system requirements:
>- CPU >= 2 Core
>- RAM >= 4 GiB
>- Storage >= 20GB

</br>

###### Install uv

This is easy to **install and use** UV package. You can install as instructions: [uv docs](https://github.com/astral-sh/uv)

```bash
uv --version
```
> **_IMPORTANT:_** If you want to check the uv package had installed, you should run the above scripts.

###### Install libraries and dependencies


TBD

###### Install docker

Install docker as instructions: [Docker installation](https://docs.docker.com/engine/install/)

We also push images to Docker Hub. You need to log in to Docker by using the following command:
```bash
docker login
```
You will be prompted to enter your Docker Hub username, password, and email address (optional). After successful authentication, you can proceed with your Docker tasks, such as pushing or pulling images from Docker Hub.


#### Set up Supabase database

###### Quick start

###### Inference FastAPI app

###### Inference in localhost

###### Inference in Docker container


##### Log and trace with Pydantic Logfire


### Production Stage

#### 9.1. Set up GCP

##### 9.1.1. Create a project in GCP

Refer to [Create a project in Google Cloud Platform (GCP)](#13-create-a-project-in-google-cloud-platform-gcp) in development stage.

##### 9.1.2. Enabling the Kubernetes Engine API

Navigate to the following link to enable Kubernetes Engine API: [Kubernetes Engine API](https://console.cloud.google.com/apis/library/container.googleapis.com)

![kubernetes-engine-api](static/images/kubernetes-engine-api.png)

##### 9.1.3. Install and setup Google Cloud CLI

Refer to [Install and setup Google Cloud CLI](#14-install-and-setup-google-cloud-cli) in development stage.

##### 9.1.4. Install gke-cloud-auth-plugin

Run the following command in your terminal:

```bash
sudo apt-get install google-cloud-cli-gke-gcloud-auth-plugin
```

##### 9.1.5. Create a service account

- Navigate to [Service acounts](https://console.cloud.google.com/iam-admin/serviceaccounts) and click "CREATE SERVICE ACCOUNT".
- Select `Kubernetes Engine Admin` role.
- Create new key as json type for your service account. Download this json file and save it in [terraform/.credentials](production/terraform/.credentials) directory. Update **credentials** in [terraform/main.tf](production/terraform/main.tf) with your json directory.
- Navigate to [IAM](https://console.cloud.google.com/iam-admin/iam) and click on "GRANT ACCESS". Then, add new principals; this principal should be your service account. Finally, select the `Owner` role.

After completion, this is the result:

![IAM](static/images/IAM.png)

#### 9.2. Install terraform

- Download terraform as instructions via this link: [Download terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
- Get terraform version and update **required_version** in [terraform/main.tf](production/terraform/main.tf)

    ![terraform-version](static/images/terraform-version.png)

#### 9.3. Install kubectl, kubectx and kubens

Kubectl, kubectx, and kubens are tools that can help with navigating clusters and namespaces in Kubernetes. Kubectl is a command-line tool that can be used to deploy applications, inspect resources, and view logs. Kubectx and kubens can help with faster context switching, which can reduce the need for manual command modifications.

- Install kubectl: [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
- Install kubectx and kubens: [kubectx and kubens](https://github.com/ahmetb/kubectx#manual-installation-macos-and-linux)

#### 9.4. Install helm

Helm helps you manage Kubernetes applications — Helm Charts help you define, install, and upgrade even the most complex Kubernetes application.

- Install helm: [helm](https://helm.sh/docs/intro/install/)

#### 9.5. Connect to a Google Kubernetes Engine (GKE) cluster

##### 9.5.1. Create the GKE cluster

Update your **project_id** in [terraform/variables.tf](production/terraform/variables.tf) and then, run the following command:

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

The GKE cluster I configured has 1 node and its machine is "e2-standard-4" (4 CPU and 16 GB Memory)

![GKE cluster](static/images/GKE-cluster.png)

##### 9.5.2. Connect to the GKE cluster

- Navigate to [GKE UI](https://console.cloud.google.com/kubernetes/list)
- Click on the vertical ellipsis icon and choose "Connect". A popup window will appear, displaying options to connect to the cluster as follow:

    ![GKE UI](static/images/gke-ui.png)

- Copy and run the command in the terminal:

    ```bash
    gcloud container clusters get-credentials [YOUR CLUSTER] --zone [YOUR REGION] --project [YOUR PROJECT ID]
    ```

- Check the connection from local using `kubectx`

    ![kubectx](static/images/kubectx.png)

### 10. Deploy to GKE

#### 10.1. Deploy Nginx Service Controller

> **_TIP:_** I set an alias 'k' for 'kubectl' for faster typing. 😆

```bash
alias k='kubectl'
```

NGINX Ingress Controller is a popular solution used in Kubernetes environments to manage incoming traffic to applications running in the cluster. It serves as a load balancer, routing external traffic to the appropriate services within the Kubernetes cluster based on defined rules and configurations.

Run the following command to deploy it:

```bash
cd helm_charts/nginx_ingress
k create ns nginx-ingress # Create the namespace nginx-ingress
kubens nginx-ingress # Switch to namespace nginx-ingress
helm upgrade --install nginx-ingress-controller .
```

Verify if the pod is running in the namespace **nginx-ingress**:

![nginx-ingress-pod](static/images/nginx-ingress-pod.png)

> **_IMPORTANT:_** Our application receives images through Nginx Ingress routing. Typically, these images are in MB (e.g., 10 MB). To accommodate large image sizes without encountering a '413 Entity Too Large' error, we must configure Nginx Ingress accordingly.

We can configure the size in [production/helm_charts/nginx_ingress/values.yaml](production/helm_charts/nginx_ingress/values.yaml):

![config-client-body-size](static/images/config-client-body-size.png)

#### 10.2. Deploy application service

We will deploy the FastAPI app to GKE in the namespace **model-serving**. It will be deployed with a NodePort type (nginx ingress will route requests to this service) and maintained by a Deployment with 2 replica pods.

```bash
cd helm_charts/app
k create ns model-serving
kubens model-serving
helm upgrade --install app .
```

```bash
k create secret generic agent-env --from-env-file=.env -n model-serving
k describe secret agent-env -n model-serving
```

Wait several minutes until it deployed sucessfully.

Now, we will test the app, do the following steps:

- Obtain the IP address of nginx-ingress

    ```bash
    k get ing
    ```

- Add the domain name `human-pose-estimation.com` of this IP to /etc/hosts where the hostnames are mapped to IP addresses.

    ```bash
    sudo nano /etc/hosts
    [YOUR_INGRESS_IP_ADDRESS] human-pose-estimation.com
    ```

    Example:

    ```nano
    35.240.217.148 human-pose-estimation.com
    ```

- Open a web browser and navigate to `human-pose-estimation.com/docs` to access the FastAPI app. Now we can test the app

    ![fastapi-gke](static/images/fastapi-gke.png)

#### 10.3. Deploy monitoring service

We use `kube-prometheus-stack` to deploy a monitoring solution for the Kubernetes cluster. This stack, provided by the Prometheus community, includes various components such as Prometheus, Grafana, Alertmanager, and other Prometheus ecosystem tools configured to monitor the health and performance of your cluster's resources.

Run these commands to deploy;

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
cd helm_charts/prometheus/kube-prometheus-stack
k create ns monitoring
kubens monitoring
helm upgrade --install kube-grafana-prometheus .
```

Add all the services of the IP to /etc/hosts

```bash
sudo nano /etc/hosts
[YOUR_INGRESS_IP_ADDRESS] human-pose-estimation.com
[YOUR_INGRESS_IP_ADDRESS] grafana.monitor.com
[YOUR_INGRESS_IP_ADDRESS] prometheus.monitor.com
[YOUR_INGRESS_IP_ADDRESS] alertmanager.monitor.com
```

Example:

```nano
35.240.217.148 human-pose-estimation.com
35.240.217.148 grafana.monitor.com
35.240.217.148 prometheus.monitor.com
35.240.217.148 alertmanager.monitor.com
```

Access the corresponding domain names to reach the service. The default username and password is **admin** and **prom-operator**.

How monitoring works: Prometheus will scape metrics from both nodes and pods within the GKE cluster. Grafana will then visualize this data, presenting metrics such as CPU and RAM usage for system health monitoring. Alerts regarding system health will be forwarded to Slack.

To send alert information to Slack, we need a Slack Webhook URL. You can follow the steps via this [link](https://sankalpit.com/plugins/documentation/how-to-create-slack-incoming-webhook-url/?ref=anaisurl.com) to create one.

Replace your slack api url in [production/helm_charts/prometheus/kube-prometheus-stack/values.yaml](production/helm_charts/prometheus/kube-prometheus-stack/values.yaml)

![slack-api-url](static/images/alert-slack.png)

Grafana dashboard:

![grafana-dashboard](static/images/grafana-dashboard.png)

Prometheus dashboard:

- RAM usage:

    ![prometheus-memory](static/images/prometheus-memory.png)

- CPU usage:

    ![prometheus-cpu](static/images/prometheus-cpu.png)


## Contributing

TBD

## License

TBD

## Citations

TBS

## Contact
