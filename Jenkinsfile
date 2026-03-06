pipeline {
  agent any

  environment {
    IMAGE_NAME = "devops-demo-app"
    CONTAINER_NAME = "devops-demo-running"
  }

  stages {

    stage('Checkout') {
      steps {
        checkout scm
        sh 'ls -la'
      }
    }

    stage('Build') {
      steps {
        sh """
          echo "Construyendo imagen Docker..."
          docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
        """
      }
    }

    stage('Test') {
        steps {
            sh '''
            echo "Ejecutando pruebas con pytest usando el volumen jenkins_home..."
            docker run --rm \
                -v jenkins_home:/var/jenkins_home \
                -w /var/jenkins_home/workspace/demo \
                python:3.11-slim \
                bash -lc "ls -la && pip install --no-cache-dir -r requirements.txt && pytest -q"
            '''
        }
    }

    stage('Deploy Simulation') {
        steps {
            sh '''
            echo "Simulando despliegue (docker run) + health check..."
            docker rm -f ${CONTAINER_NAME} || true

            docker run -d --name ${CONTAINER_NAME} \
                --add-host=host.docker.internal:host-gateway \
                -p 5001:5000 \
                ${IMAGE_NAME}:${BUILD_NUMBER}

            sleep 6
            curl -sSf http://host.docker.internal:5001/health
            echo ""
            echo "OK - App arriba en /health"
            '''
        }
    }
  }

  post {
    always {
      sh """
        echo "Limpieza (opcional)..."
        docker logs ${CONTAINER_NAME} || true
      """
    }
    success {
      echo "Pipeline completado con ÉXITO."
    }
    failure {
      echo "Pipeline FALLÓ. Revisa la consola."
    }
  }
}