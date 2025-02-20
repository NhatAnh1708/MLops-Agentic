# Real-time-Agentic-MLops

A MLops pipeline for real-time agentic system.

[![Architecture](./assets/images/Architecture-realtime.png)](./assets/images/Architecture-realtime.png)

## Introduction

TBD

## Table of Contents

- [Introduction](#introduction)
- [Key Features](#key-features)
- [Project Structures](#project-structures)
- [Overall Architecture](#architecture)
- [Getting Started](#getting-started)
    - [Development stage](#development-stage)
        - [Set up environments](#set-up-environments)
            - [Install uv](#install-uv)
            - [Install libraries and dependencies](#install-libraries)
            - [Install docker](#install-docker)
        - [Set up Supabase database](#set-up-supabase-database)
            - [Quick start](#quick-start-supabase)
        - [Inference FastAPI app](#inference-fastapi-app)
            - [Inference in localhost](#inference-in-localhost)
            - [Inference in Docker container](#inference-in-docker-container)
        - [Log and trace with Pydantic Logfire](#set-up-logfire-development)
    - [Production stage](#production-stage)
        - [Set up](#9-set-up)
            - [Set up Google Cloud Platform (GCP)](#91-set-up-gcp)
                - [Create a project in Google Cloud Platform (GCP)](#911-create-a-project-in-gcp)
                - [Enabling the Kubernetes Engine API](#912-enabling-the-kubernetes-engine-api)
                - [Install and setup Google Cloud CLI](#913-install-and-setup-google-cloud-cli)
                - [Install gke-cloud-auth-plugin](#914-install-gke-cloud-auth-plugin)
                - [Create a service account](#915-create-a-service-account)
            - [Install Terraform](#92-install-terraform)
            - [Install kubectl, kubectx and kubens](#93-install-kubectl-kubectx-and-kubens)
            - [Install helm](#94-install-helm)
        - [Using Terraform for Google Kubernetes Engine (GKE)](#using-terraform-for-google-kubernetes-engine-gke)
            - [Set up the cluster](#set-up-the-cluster)
            - [Retrive the cluster information](#retrive-cluster-information)
        - [Deployment to Google Kubernetes Engine (GKE)](#deployment-to-gke)
            - [Configure API Key Secret](#configure-api-key-secret)
            - [Deploy Nginx-Ingress controller](#deploy-nginx-ingress-controller)
            - [Deploy Database controller](#deploy-database-controller)
            - [Deploy Redis controller](#deploy-redis-controller)
            - [Deploy FastAPI controller](#deploy-fastapi-controller)
        - [Continuous Integration/Continuous Deployment (CI/CD) with Travis CI](#continuous-integrationcontinuous-deployment-cicd-with-travis-ci)
            - [Set up Travis CI Server](#set-up-travis-ci-server)
            - [Access Travis CI](#access-travis-ci)
            - [Install Travis CI Plugins](#install-travis-ci-plugins)
            - [Configure Travis CI](#configure-travis-ci)
            - [Test the setup](#test-the-travis-ci-setup)
        - [Log and trace with Pydantic Logfire](#set-up-logfire-production)
        - [Monitoring with Prometheus and Gafana](#monitoring-with-prometheus-and-gafana)
            - [Quick start](#quick-start)
            - [Test the setup](#test-the-monitoring-setup)
        

- [Contributing](#contributing)
- [License](#license)
- [Citations](#citations)
- [Contact](#contact)

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
TBD


## Contributing

TBD

## License

TBD

## Citations

TBS

## Contact



