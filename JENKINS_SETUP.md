# Jenkins setup on AWS EC2 for this pipeline

This guide shows how to create a fresh Jenkins instance on an AWS EC2 instance and configure it to run the pipeline contained in this repository (the `Jenkinsfile` in the repo).

Important: this repository's `Jenkinsfile` has hardcoded ECR account, region and image names for demo purposes. Do NOT use this configuration in production.

## Overview
- Launch an EC2 instance (Ubuntu 22.04 or Amazon Linux 2).
- Install Docker, Java, and Jenkins.
- Install recommended Jenkins plugins (Pipeline, Git, Docker Pipeline, Amazon ECR plugin or configure AWS CLI).
- Create a Pipeline job pointing to this repository's `Jenkinsfile`.

## Prerequisites
- AWS account and permissions to create EC2 instances and (optionally) ECR repositories.
- Key pair for SSH access to EC2.
- Security Group allowing:
  - SSH (TCP 22) from your IP
  - Jenkins (TCP 8080) from your IP or VPN

Optional (recommended): create an IAM role with ECR permissions and attach it to the EC2 instance so Jenkins can push to ECR without storing long-term keys.

## Launch an EC2 instance
Example using the AWS CLI (Ubuntu 22.04, t3.small):

```bash
# replace AMI/KEY/SG/ZONE with your values
aws ec2 run-instances \
  --image-id ami-0xxxxxxxxxxxxxxx \
  --instance-type t3.small \
  --key-name my-keypair \
  --security-group-ids sg-0123456789abcdef0 \
  --subnet-id subnet-xxxxxxxx \
  --associate-public-ip-address
```

Or pick an Ubuntu 22.04 / Amazon Linux 2 image from the console and launch.

## SSH into the instance

```bash
ssh -i /path/to/my-keypair.pem ubuntu@<EC2_PUBLIC_IP>
```

## Install Docker
For Ubuntu:

```bash
sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io
sudo systemctl enable --now docker
```

For Amazon Linux 2:

```bash
sudo amazon-linux-extras enable docker
sudo yum install -y docker
sudo systemctl enable --now docker
```

Add the `jenkins` user to the `docker` group after Jenkins is installed (below) so Jenkins can use Docker:

```bash
sudo usermod -aG docker jenkins
```

## Install Java and Jenkins
For Ubuntu:

```bash
sudo apt update
sudo apt install -y openjdk-11-jdk
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" \
  | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt update
sudo apt install -y jenkins
sudo systemctl enable --now jenkins
```

For Amazon Linux 2 (example):

```bash
sudo yum install -y java-11-amazon-corretto
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key
sudo yum install -y jenkins
sudo systemctl enable --now jenkins
```

Wait a few seconds and open your browser at http://<EC2_PUBLIC_IP>:8080. Retrieve the initial admin password:

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Follow the web UI to install suggested plugins. Manually ensure the following plugins are installed:
- Pipeline
- Git
- Docker Pipeline
- (Optional) Amazon ECR plugin or Amazon Web Services Credentials Plugin

## Configure Jenkins

1. Create credentials:
   - If you attached an IAM role with ECR permissions to the instance, you may skip AWS keys.
   - Otherwise create an AWS credential set (username/password style) in Jenkins (or use the `usernamePassword` credential binding with ID `aws-creds`).
   - Add Git credentials if your repo is private.

2. Ensure the `jenkins` user can run Docker (restart Jenkins after adding `jenkins` to the `docker` group):

```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

3. Create a new Pipeline job:
   - New Item → Pipeline → choose a name
   - Under `Pipeline` → `Definition` choose `Pipeline script from SCM`
   - SCM: `Git`
   - Repository URL: (this repository URL)
   - Credentials: (select credential if needed)
   - Branch: `*/main` (or whichever branch)
   - Script Path: `Jenkinsfile`

4. Save and Run the pipeline.

## What the pipeline does (repo's `Jenkinsfile`)
- Runs tests inside a Python container (if `requirements.txt` exists).
- Builds a Docker image named `test-namespace/plant`.
- Tags the image and pushes to the hardcoded ECR registry `024122091944.dkr.ecr.ap-south-1.amazonaws.com/test-namespace/plant:latest`.

The push step in the `Jenkinsfile` uses this command (already hardcoded in the repo):

```bash
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 024122091944.dkr.ecr.ap-south-1.amazonaws.com
docker push 024122091944.dkr.ecr.ap-south-1.amazonaws.com/test-namespace/plant:latest
```

If you are not using an instance role, ensure `aws configure` is run on the instance or the Jenkins environment has valid AWS credentials (or create Jenkins credentials and adapt the pipeline to use them).

## Optional: secure Jenkins and housekeeping
- Restrict access to port 8080 using Security Groups.
- Rotate or remove hardcoded values before production.
- Consider using an ECR credential helper or IAM roles rather than embedding credentials.

## Troubleshooting
- If Docker commands fail from Jenkins, check `jenkins` is in the `docker` group and Jenkins restarted.
- Check `/var/log/jenkins/jenkins.log` for Jenkins errors.
- Verify AWS CLI version: `aws --version` (ECR login requires modern AWS CLI).

## Next steps I can do for you
- Commit the new `JENKINS_SETUP.md` to the repo and push.
- Update the `Jenkinsfile` to use credentials or to accept pipeline parameters instead of hardcoded values.
