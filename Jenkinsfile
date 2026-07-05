pipeline {
    agent any

    environment {
        PYTHONPATH = '.'
        TESTING = 'true'
    }

    triggers {
        githubPush()
    }

    options {
        timeout(time: 20, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Build') {
            steps {
                sh 'python3 -m pip install --upgrade pip'
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh 'pytest -q'
            }
        }

        stage('Deploy') {
            when {
                anyOf {
                    branch 'main'
                    branch 'staging'
                }
            }
            steps {
                script {
                    if (env.BRANCH_NAME == 'staging') {
                        sh 'echo "Deploying to the staging environment..."'
                    } else {
                        sh 'echo "Deploying the main branch to staging..."'
                    }
                }
            }
        }
    }

    post {
        success {
            mail to: 'your-email@example.com',
                 subject: "Jenkins Build ${env.JOB_NAME} #${env.BUILD_NUMBER} Succeeded",
                 body: "The pipeline completed successfully."
        }
        failure {
            mail to: 'your-email@example.com',
                 subject: "Jenkins Build ${env.JOB_NAME} #${env.BUILD_NUMBER} Failed",
                 body: "The pipeline failed. Please review the Jenkins console output."
        }
    }
}
