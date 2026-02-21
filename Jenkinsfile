pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps {
        script {
          git branch: 'main', url: 'https://github.com/mufaddal-synapse/plant-shop.git'
        }
      }
    }
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
          sh 'docker build -t test-namespace/plant .'
        }
      }
    }
    stage('Tag') {
      steps {
        script {
          sh 'docker tag test-namespace/plant:latest 024122091944.dkr.ecr.ap-south-1.amazonaws.com/test-namespace/plant:latest'
        }
      }
    }
    stage('Push') {
      steps {
        script {
          sh '''
            aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 024122091944.dkr.ecr.ap-south-1.amazonaws.com
            docker push 024122091944.dkr.ecr.ap-south-1.amazonaws.com/test-namespace/plant:latest
          '''
        }
      }
    }
  }
}
