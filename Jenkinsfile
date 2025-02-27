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
                    echo 'Pushing Docker image to the registry...'
                    docker.withRegistry('', DOCKER_REGISTRY_CREDENTIAL) {
                        docker.image("${DOCKER_FULL_IMAGE}").push()
                        docker.image("${DOCKER_FULL_IMAGE}").push('latest')
                    }
                }
            }
        }
    }

    environment {
        DOCKER_IMAGE = 'danny1708/ai-agent-service'
        DOCKER_FULL_IMAGE = "${DOCKER_IMAGE}:lastest"
        DOCKER_REGISTRY_CREDENTIAL = 'dockerhub'
    }
}
