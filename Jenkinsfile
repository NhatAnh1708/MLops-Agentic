pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'danny1708/ai-agent-service'
        DOCKER_FULL_IMAGE = "${DOCKER_IMAGE}:latest"
        DOCKER_REGISTRY_CREDENTIAL = 'dockerhub'
        BLACKDUCK_PATH = "${WORKSPACE}/blackduck"  // Cài đặt Black Duck vào thư mục workspace
    }

    stages {
        stage('Check & Install Dependencies') {
            steps {
                script {
                    sh '''
                    set -e  # Dừng khi có lỗi

                    # Kiểm tra Python 3
                    if ! command -v python3 &> /dev/null; then
                        echo "Python3 not found! Installing..."
                        apt update && apt install python3 python3-venv -y
                    fi

                    # Kiểm tra và tải Black Duck nếu chưa có
                    if [ ! -f "${BLACKDUCK_PATH}/blackduck" ]; then
                        echo "Black Duck not found! Downloading..."
                        curl -LO https://detect.synopsys.com/detect.sh
                        chmod +x detect.sh
                        mkdir -p "${BLACKDUCK_PATH}"
                        mv detect.sh "${BLACKDUCK_PATH}/blackduck"
                    fi

                    # Kiểm tra quyền thực thi
                    chmod +x "${BLACKDUCK_PATH}/blackduck"
                    '''
                }
            }
        }

        stage('Setup') {
            steps {
                script {
                    sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Blackduck Scan') {
            steps {
                script {
                    sh '''
                    bash ${BLACKDUCK_PATH}/blackduck scan --detect.project.name=ai-agent-service \
                                  --detect.project.version.name=1.0 \
                                  --detect.source.path=. \
                                  --detect.blackduck.signature.scanner.snippet.mode=rapid
                    '''
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
                    sh '''
                    docker build -t ${DOCKER_IMAGE} . --platform linux/amd64
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    echo 'Pushing Docker image to the registry...'
                    docker.withRegistry('', DOCKER_REGISTRY_CREDENTIAL) {
                        docker.image("${DOCKER_IMAGE}").push()
                        docker.image("${DOCKER_IMAGE}").push('latest')
                    }
                }
            }
        }
    }
}
