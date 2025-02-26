pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                script {
                    sh 'python3 -m venv venv'
                    sh '. venv/bin/activate && pip install -r requirements.txt'
                }
            }
        }
        stage('Blackduck Scan') {
            steps {
                script {
                    sh 'blackduck scan --detect.project.name=ai-agent-service --detect.project.version.name=1.0 --detect.source.path=. --detect.blackduck.signature.scanner.snippet.mode=rapid'
                }
            }
        }


        stage('Run Simulation') {
            steps {
                script {
                    sh '''
                    . venv/bin/activate
                    uvicorn server:app --reload --port 8000 --host 0.0.0.0 &
                    sleep 5
                    kill $(lsof -t -i:8000)
                    '''
                }
            }
        }


        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t danny1708/ai-agent-service . --platform linux/amd64'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    // Đăng nhập vào Docker Hub (nếu cần)
                    sh 'echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin'
                    // Đẩy Docker image lên Docker Hub
                    sh 'docker push danny1708/ai-agent-service-m1'
                }
            }
        }
    }

    environment {
        DOCKER_USERNAME = credentials('docker-username') // Thay thế bằng ID credential của bạn
        DOCKER_PASSWORD = credentials('docker-password') // Thay thế bằng ID credential của bạn
    }
}
