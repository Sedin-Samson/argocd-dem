pipeline {
    agent any

    environment {
        // Dynamic build version tag based on Jenkins Build Number
        IMAGE_TAG = "v1.0.${BUILD_NUMBER}"
        GIT_REPO_URL = "git@github.com:Sedin-Samson/argocd-dem.git"
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Backend Docker Image with tag: backend:${IMAGE_TAG}"
                sh "docker build -t backend:${IMAGE_TAG} ./backend"
            }
        }

        stage('Load Image to Cluster') {
            steps {
                echo "Loading backend:${IMAGE_TAG} into local Minikube cluster..."
                sh "minikube image load backend:${IMAGE_TAG}"
            }
        }

        stage('Update Kubernetes Manifest') {
            steps {
                echo "Updating backend deployment image tag to backend:${IMAGE_TAG}"
                // Update image tag in kubernetes/backend-deployment.yaml using sed
                sh """
                    sed -i.bak "s|image: backend:.*|image: backend:${IMAGE_TAG}|g" kubernetes/backend-deployment.yaml
                    rm -f kubernetes/backend-deployment.yaml.bak
                """
            }
        }

        stage('Commit & Push Manifest to GitOps Repo') {
            steps {
                echo "Pushing updated manifest tag to GitHub..."
                sh """
                    git config user.name "Jenkins CI"
                    git config user.email "jenkins@sedintechnologies.com"
                    git add kubernetes/backend-deployment.yaml
                    git commit -m "ci(argocd): update backend image tag to backend:${IMAGE_TAG} [skip ci]" || echo "No changes to commit"
                    git push origin main
                """
            }
        }
    }

    post {
        success {
            echo "✅ CI/CD Pipeline Completed Successfully! Argo CD will now detect and sync backend:${IMAGE_TAG}."
        }
        failure {
            echo "❌ Pipeline failed! Please check logs."
        }
    }
}
