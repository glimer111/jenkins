pipeline {
    agent any

    environment {
        SOURCE_DIR = '/workspace'
        VENV_DIR = '.venv'
        PIP_DISABLE_PIP_VERSION_CHECK = '1'
        BUILD_ID = 'dontKillMe'
        JENKINS_NODE_COOKIE = 'dontKillMe'
    }

    stages {
        stage('Sync Project') {
            steps {
                sh '''
                    cp -r ${SOURCE_DIR}/. ${WORKSPACE}/
                    ls -la ${WORKSPACE}
                '''
            }
        }

        stage('Setup') {
            steps {
                sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Download Data') {
            steps {
                sh '''
                    . ${VENV_DIR}/bin/activate
                    python download_data.py
                '''
            }
        }

        stage('Prepare Dataset') {
            steps {
                sh '''
                    . ${VENV_DIR}/bin/activate
                    python prepare_dataset.py
                '''
            }
        }

        stage('Train Model') {
            steps {
                sh '''
                    . ${VENV_DIR}/bin/activate
                    python train_model.py
                '''
            }
        }

        stage('Deploy Service') {
            steps {
                sh '''
                    . ${VENV_DIR}/bin/activate
                    pkill -f "uvicorn app:app" || true
                    nohup uvicorn app:app --host 0.0.0.0 --port 8000 > service.log 2>&1 &
                    sleep 8
                    cat service.log
                '''
            }
        }

        stage('Test Service') {
            steps {
                sh '''
                    . ${VENV_DIR}/bin/activate
                    python test_service.py
                    curl -s -X POST http://127.0.0.1:8000/predict \
                      -H "Content-Type: application/json" \
                      --data @sample_request.json
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'data/**/*.csv, models/*.pkl, models/*.json, service.log', allowEmptyArchive: true
            echo 'Pipeline completed'
        }
        failure {
            echo 'Pipeline failed'
        }
    }
}
