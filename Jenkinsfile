#!/usr/bin/env groovy

pipeline {
    parameters {
        string(name: 'Allan White', defaultValue: 'devOps', description: 'Team')
    }
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
        timestamps()
        timeout(time: 7, unit: 'MINUTES')
    }
    agent any
    stages {
        stage('Initialization') {
            steps {
                buildName "devOps_${BUILD_NUMBER}"
                buildDescription "NODE_NAME = ${NODE_NAME}"
            }
        }
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Run Selenium') {
            steps {
                script {
                    sh '''
                        chrome=$(docker inspect --format '{{json .State.Running}}' node-chrome || true)
                        if [ "$chrome" = true ]; then
                           echo "Container node-chrome is running. Stoping..."
                           docker stop node-chrome
                           # container will be removed automatically (auto_remove=True)
                        else
                           echo "Container node-chrome is NOT running."
                        fi

                        selenium=$(docker inspect --format '{{json .State.Running}}' selenium-hub || true)
                        if [ "$selenium" = true ]; then
                           echo "Container selenium-hub is running. Removing..."
                           docker stop selenium-hub
                           # container will be removed automatically (auto_remove=True)
                        else
                           echo "Container selenium-hub is NOT running."
                        fi

                        network=$(docker network ls|grep grid || true)
                        if [ "$network" ]; then
                           echo "Network grid exists. Removing..."
                           docker network rm `docker network ls --filter name=grid -q`
                        else
                           echo "Network grid doesn't exist"
                        fi

                        if [ ! "$(docker ps -q -f name=node-chrome)" ]; then
                            if [ "$(docker ps -aq -f status=exited -f name=node-chrome)" ]; then
                                # cleanup
                                docker rm node-chrome selenium-grid
                                docker network rm grid
                                # run containers
                                python3 run_selenium.py
                            fi
                            python3 run_selenium.py
                        fi
                    '''
                }
            }
        }
        stage('Test Selenium') {
            steps {
                script {
                    sh '''
                        python3 test_selenium.py | tee -a "test_${BUILD_NUMBER}.log"
                    '''
                }
            }
        }
        stage('Post Logs') {
            steps {
                script {
                    sh '''#!/bin/bash
                        stdout=$(<test_${BUILD_NUMBER}.log)
                        echo "${stdout}"
                        curl -X POST -H "Content-Type: application/json" \
                        -d '{"pipeline": "DevOps", "stage": "Test Selenium", "stdout": "'"$stdout"'"' \
                        https://webhook.site/3677cf3a-a0d6-4b98-bdb2-4cc5e4421ab4
                    '''
                }
            }
        }
        stage('Allowed Range') {
            steps {
                script {
                    sh '''#!/bin/bash
                        nodes=$(tail -1 test_${BUILD_NUMBER}.log | grep -Eo '[0-9]+$')
                        echo "Available nodes: ${nodes}"
                        if [ $nodes -ge 1 -a $nodes -le 5 ]; then
                            echo "The number of nodes within the allowed range. Moving ahead to the deployment stage."
                        else
                            echo "The number of available nodes is outside the allowed range."
                            exit 1
                        fi
                    '''
                }
            }
        }
    }
}
