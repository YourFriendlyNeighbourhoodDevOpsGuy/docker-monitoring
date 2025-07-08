Docker CPU Monitor with SES Alerting & GitHub Actions CI/CD

This project monitors Docker container CPU usage and sends email alerts via AWS SES when usage exceeds a specified threshold. The system is containerized and deployed to an EC2 instance using GitHub Actions, with the Docker image hosted in Amazon ECR.

Features

Monitor Docker containers for high CPU usage
Send email alerts using AWS Simple Email Service (SES)
Containerized Python application
GitHub Actions CI/CD pipeline:
Build & push image to Amazon ECR
SSH into EC2 and deploy the container
Terraform automation for SES email identity setup
Project Structure

.
├── docker_monitoring.py (Main monitoring script)
├── Dockerfile (Docker image definition)
├── .dockerignore (Excludes terraform and dev files)
├── .github/
│ └── workflows/
│ └── workflows.yml (GitHub Actions workflow)
├── terraform/
│ ├── main.tf (SES setup)
│ ├── variables.tf
│ └── terraform.tfvars
└── README.txt (This file)

How It Works

docker_cpu_monitor.py checks running Docker containers.
If a container exceeds a CPU threshold (e.g., 80%), an alert is sent via SES.
The script runs inside a Docker container deployed to an EC2 instance.
GitHub Actions builds the Docker image, pushes it to ECR, and deploys it to EC2 via SSH.
Prerequisites

AWS:

Amazon SES with verified:
Sender email address
Recipient email address
An Amazon ECR repository (e.g., docker-cpu-monitor)
IAM user or role with permissions:
ses:SendEmail
ecr:*
EC2 instance:
Docker installed
AWS CLI configured or IAM Role attached
Your SSH public key added to ~/.ssh/authorized_keys
Setup & Deployment

Step 1: Configure SES with Terraform
I have included the terraform code which you can choose to run in local
cd terraform/
terraform init
terraform apply
Then verify both sender and recipient email addresses via links sent to your inbox.

Step 2: Add GitHub Secrets

Go to GitHub → Settings → Secrets and Variables → Actions → New Repository Secret

Add the following:
Depends on if you are integrating github actions or running directly from EC2 instance, in the latter case you can pick the steps from actions file and execute same in ec2 terminal

AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION (e.g., us-east-1)
ECR_ACCOUNT_ID (your 12-digit AWS account ID)
ECR_REPOSITORY (e.g., docker-cpu-monitor)
EC2_USER (e.g., ubuntu)
EC2_HOST (your EC2 public IP or DNS)
PRIVATE_KEY (your SSH private key content, in PEM format)
Step 3: Trigger Deployment

Push to the main branch to trigger:

Docker image build
Push to ECR
EC2 login over SSH
Image pull and container launch
