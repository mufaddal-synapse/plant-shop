pipeline {
  agent any
  parameters {
    string(name: 'ECR_ACCOUNT_ID', defaultValue: '', description: 'AWS account ID for ECR')
    string(name: 'ECR_REGION', defaultValue: 'us-east-1', description: 'AWS region')
    string(name: 'ECR_REPO', defaultValue: 'plant-web-app', description: 'ECR repository name')
    string(name: 'IMAGE_TAG', defaultValue: '', description: 'Image tag (defaults to BUILD_NUMBER)')
  }
  stages {
    stage('Test') {
      steps {
        script {
          sh 'docker run --rm -v "$PWD":/src -w /src python:3.11-slim bash -lc "if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi; pytest -q"'
        }
      }
    }
    stage('Build') {
      steps {
        script {
          def tag = params.IMAGE_TAG ?: env.BUILD_NUMBER
          def image = "${params.ECR_ACCOUNT_ID}.dkr.ecr.${params.ECR_REGION}.amazonaws.com/${params.ECR_REPO}"
          sh "docker build -t ${image}:${tag} ."
        }
      }
    }
    stage('Push') {
      steps {
        script {
          def tag = params.IMAGE_TAG ?: env.BUILD_NUMBER
          def image = "${params.ECR_ACCOUNT_ID}.dkr.ecr.${params.ECR_REGION}.amazonaws.com/${params.ECR_REPO}"
          withCredentials([usernamePassword(credentialsId: 'aws-creds', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
            sh """
              aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
              aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
              aws configure set region ${params.ECR_REGION}
              aws ecr get-login-password --region ${params.ECR_REGION} | docker login --username AWS --password-stdin ${params.ECR_ACCOUNT_ID}.dkr.ecr.${params.ECR_REGION}.amazonaws.com
              aws ecr create-repository --repository-name ${params.ECR_REPO} >/dev/null 2>&1 || true
              docker push ${image}:${tag}
            """
          }
        }
      }
    }
  }
}
