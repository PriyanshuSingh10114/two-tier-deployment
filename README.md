🚀 Two-Tier Flask Application Deployment
---

Docker · Kubernetes · Helm · AWS (Kind → EKS Ready)

---


📌 Project Overview

This project demonstrates a complete end-to-end DevOps workflow for deploying a Two-Tier Flask + MySQL application, starting from local development to Kubernetes and Helm, with cloud-ready architecture for AWS.

---

✔ What this project covers

- Flask backend + MySQL database

- Dockerized application & database

- Docker Compose (local testing)

- Kubernetes manifests

- Helm charts (MySQL + Flask app)

- Kind cluster (local Kubernetes)

- GitHub → DockerHub → Kubernetes → Helm → AWS-ready pipeline

---

Real-world troubleshooting (DB wait, InitContainers, ImagePull issues)

---

  🏗️ Architecture
  
    Developer (GitHub)
            |
            v
       GitHub Repo
            |
            v
       Docker Build
            |
            v
       DockerHub
            |
            v
       Kubernetes Cluster
            |
            v
         Helm Charts
            |
            v
       AWS (EKS Ready)

---

Two containers:

- Flask App (Python)

- MySQL Database

---

🛠️ Tech Stack

 Layer	Technology
 
 - Backend	Flask (Python)
 
 - Database	MySQL 5.7
 
 - Containers	Docker
 
 - Orchestration	Kubernetes
 
 - Package Manager	Helm
 
 - Local K8s	Kind
 
 - Cloud Target	AWS (EKS)
 
 - CI/CD Ready	GitHub + DockerHub
 
 ---
 
📁 Repository Structure

    two-tier-flask-app/
    ├── app.py
    ├── requirements.txt
    ├── Dockerfile
    ├── Dockerfile-multistage
    ├── docker-compose.yml
    ├── message.sql
    ├── templates/
    │   └── index.html
    ├── k8s/
    │   ├── deployment.yml
    │   ├── svc.yml
    │   └── mysql.yml
    ├── mysql-chart/
    │   └── Helm chart for MySQL
    ├── flask-app-chart/
    │   └── Helm chart for Flask app
    ├── kind-setup/
    │   └── config.yml
    ├── Jenkinsfile
    ├── Makefile
    └── README.md

⚙️ Application Configuration

AWS EC2 Instance minimum requirements

 - ec2 linux ubuntu instance
   
 - instance type : t2.medium
   
 - Storage 20GB

 - Give access from all ports

 - insatnce -1

   ---
   
Environment Variables (Flask App)

     MYSQL_HOST=mysql
     MYSQL_USER=admin
     MYSQL_PASSWORD=admin
     MYSQL_DB=myDb

 ---

🐳 Docker Setup

🔹 Build Flask Image

docker build -t <dockerhub-username>/flask-app:latest .

🔹 Push to DockerHub

docker login

docker push <dockerhub-username>/flask-app:latest

🧪 Local Testing with Docker Compose

docker compose up -d

Check:

docker ps

Stop:

docker compose down -v

---

☸️ Kubernetes Setup (Kind)

🔹 Install Kind

    curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.23.0/kind-linux-amd64
    chmod +x kind
    sudo mv kind /usr/local/bin/

🔹 Kind Cluster Config (kind-setup/config.yml)

    kind: Cluster
    apiVersion: kind.x-k8s.io/v1alpha4
    nodes:
    - role: control-plane
    - role: worker
    - role: worker

🔹 Create Cluster

    kind create cluster --name tws-cluster --config kind-setup/config.yml

---

Verify:

kubectl get nodes

☸️ Kubernetes Deployment (YAML)

   🔹 Deploy MySQL
   
   kubectl apply -f k8s/mysql.yml
   
   🔹 Deploy Flask App
   
   kubectl apply -f k8s/deployment.yml
   
   kubectl apply -f k8s/svc.yml

Check:

kubectl get pods

kubectl get svc

---

📦 Helm Setup
🔹 Install Helm

    curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

Verify:

    helm version

📦 Helm: MySQL Chart

cd mysql-chart

    helm lint .
    helm install mysql-chart .


Check:

    kubectl get pods
    kubectl get svc mysql-chart

📦 Helm: Flask App Chart

cd flask-app-chart

    helm lint .
    helm install flask-app-chart .


Check:

    kubectl get pods
    kubectl get svc flask-app-chart

---

⏳ MySQL Dependency Handling (IMPORTANT)

Flask app uses an InitContainer to wait for MySQL:

    initContainers:
    - name: wait-for-mysql
      image: mysql:5.7
      command:
        - sh
        - -c
        - |
          until mysqladmin ping -h mysql-chart -uroot -padmin --silent; do
            echo "Waiting for MySQL..."
            sleep 5
          done


This avoids CrashLoopBackOff.

---

🌐 Access the Application
NodePort
kubectl get svc flask-app-chart

Example:

http://<NODE-IP>:32230

Port Forward (Local)
kubectl port-forward svc/flask-app-chart 8080:80

---


🧹 Cleanup

    helm uninstall flask-app-chart
    helm uninstall mysql-chart
    kind delete cluster --name tws-cluster
    docker system prune -af

---

👨‍💻 Author

Priyanshu Singh
DevOps | Cloud | Kubernetes | Helm

⭐ If you found this useful

Star ⭐ the repo and fork 🍴 it to build your own production pipelines.

