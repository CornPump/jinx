pipeline {
    agent any

        parameters {
            string(name: 'WORK_SPACE_PATH', defaultValue: '/var/lib/jenkins/workspace/', description: 'Path Jenkins work space')
        }

        stages {
            stage("Clone Git Repository") {
                steps {
                    git(
                        url: "https://github.com/CornPump/jinx.git",
                        branch: "master",
                        changelog: true,
                        poll: true
                    )
                }
            }

            stage('Set Credentials') {
                steps {
                    sh "cp ${WORK_SPACE_PATH}config.py credentials/"
                }
            }

            stage('Set Up Python Environment') {
                steps {
                    script {
                        // Create and activate a virtual environment
                        sh 'python -m venv venv'
                        sh 'chmod +x venv/bin/activate'
                        sh './venv/bin/activate'

                        // Install project dependencies
                        def targetDirectory = params.WORK_SPACE_PATH
                        def path = "${targetDirectory}/jinx_testing/venv/bin/pip3"
                        sh "${path} install -r requirements.txt"
                    }
                }
            }

            stage('Run Tests') {
                steps {
                    // Run all tests using pytest
                    sh 'venv/bin/pytest tests/'
                }
            }
        }

        post {

            success {
                echo 'Tests passed successfully'
                // You can add further actions here for a successful build
                echo 'Deleting work evnironment'
                deleteDir() /* clean up our workspace */
            }

            failure {
                echo 'Tests failed!'
                // You can add further actions here for a failed build
            }


        }
}
