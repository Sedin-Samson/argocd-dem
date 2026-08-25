pipeline {
    agent any

    parameters {
        choice(
            name: 'SERVICE_TO_BUILD',
            choices: ['ALL', 'backend', 'frontend'],
            description: 'Select which microservice to build & deploy to AWS ECR'
        )
        string(
            name: 'TAG_NAME',
            defaultValue: 'v1.0.0',
            description: 'Enter the exact Tag Name to create and deploy (e.g. backend-v1.0.1, frontend-v2.0.1, v1.0.0)'
        )
    }

    environment {
        // AWS & ECR Configuration
        AWS_REGION      = "ap-south-1"
        AWS_ACCOUNT_ID  = "156916773321"
        ECR_REGISTRY    = "156916773321.dkr.ecr.ap-south-1.amazonaws.com"
        
        BACKEND_ECR     = "156916773321.dkr.ecr.ap-south-1.amazonaws.com/argocd-demo-backend"
        FRONTEND_ECR    = "156916773321.dkr.ecr.ap-south-1.amazonaws.com/argocd-demo-frontend"

        PATH            = "/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:$PATH"
        IMAGE_TAG       = "${params.TAG_NAME}"
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('AWS ECR Login') {
            steps {
                echo "🔐 Logging into AWS Elastic Container Registry (${ECR_REGISTRY})..."
                withCredentials([usernamePassword(credentialsId: 'aws-ecr-creds', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh """
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY} || true
                    """
                }
            }
        }

        stage('Build & Push Backend Microservice') {
            when {
                expression { params.SERVICE_TO_BUILD == 'ALL' || params.SERVICE_TO_BUILD == 'backend' }
            }
            steps {
                echo "=================================================="
                echo " 🛠️ Building Backend Docker Image: ${BACKEND_ECR}:${IMAGE_TAG}"
                echo "=================================================="
                sh "docker build -t ${BACKEND_ECR}:${IMAGE_TAG} -t ${BACKEND_ECR}:latest ./backend"

                echo "📤 Pushing Backend Docker Image to AWS ECR..."
                sh """
                    docker push ${BACKEND_ECR}:${IMAGE_TAG} || true
                    docker push ${BACKEND_ECR}:latest || true
                """

                echo "⚙️ Updating backend deployment manifest tag..."
                sh """
                    sed -i.bak "s|image: .*|image: ${BACKEND_ECR}:${IMAGE_TAG}|g" kubernetes/backend/backend-deployment.yaml
                    rm -f kubernetes/backend/backend-deployment.yaml.bak
                """
            }
        }

        stage('Build & Push Frontend Microservice') {
            when {
                expression { params.SERVICE_TO_BUILD == 'ALL' || params.SERVICE_TO_BUILD == 'frontend' }
            }
            steps {
                echo "=================================================="
                echo " 🛠️ Building Frontend Docker Image: ${FRONTEND_ECR}:${IMAGE_TAG}"
                echo "=================================================="
                sh "docker build -t ${FRONTEND_ECR}:${IMAGE_TAG} -t ${FRONTEND_ECR}:latest ./frontend"

                echo "📤 Pushing Frontend Docker Image to AWS ECR..."
                sh """
                    docker push ${FRONTEND_ECR}:${IMAGE_TAG} || true
                    docker push ${FRONTEND_ECR}:latest || true
                """

                echo "⚙️ Updating frontend deployment manifest tag..."
                sh """
                    sed -i.bak "s|image: .*|image: ${FRONTEND_ECR}:${IMAGE_TAG}|g" kubernetes/frontend/frontend-deployment.yaml
                    rm -f kubernetes/frontend/frontend-deployment.yaml.bak
                """
            }
        }

        stage('Commit & Push Manifests and Git Release Tag') {
            steps {
                echo "📤 Creating local Git Tag ${IMAGE_TAG} and pushing to GitHub..."
                withCredentials([string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')]) {
                    sh """
                        git config user.name "Jenkins CI"
                        git config user.email "samson@sedintechnologies.com"
                        git add kubernetes/
                        git commit -m "release(${params.SERVICE_TO_BUILD}): deploy ${IMAGE_TAG} [skip ci]" || echo "No changes to commit"
                        
                        # Create local Git Tag specified in parameter
                        git tag -a "${IMAGE_TAG}" -m "Release ${IMAGE_TAG} created by Jenkins" || true
                        
                        # Push branch and tag to GitHub
                        git push https://\${GITHUB_TOKEN}@github.com/Sedin-Samson/argocd-dem.git HEAD:main
                        git push https://\${GITHUB_TOKEN}@github.com/Sedin-Samson/argocd-dem.git "${IMAGE_TAG}" || true
                    """
                }
            }
        }
    }

    post {
        success {
            echo "✅ CI/CD Pipeline Completed Successfully for Service: ${params.SERVICE_TO_BUILD} with Tag: ${IMAGE_TAG}!"
        }
        failure {
            echo "❌ Pipeline failed! Please check logs."
        }
    }
}
