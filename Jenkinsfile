 node {

 
   stage('Git checkout') {
       git 'https://github.com/fcaudillo/celeryworker.git'
   }
   
   stage('Construyendo imagen') {
       sh ('docker build --build-arg BUILD_USU_MQ=${USUARIO_MQ} --build-arg BUILD_PASS_MQ=${PASSWORD_MQ} -t  fcaudillo/celeryreload . ') 
   }
  
   stage('Subiendo la imagen.') {
        withDockerRegistry([ credentialsId: "my_crends_docker", url: '' ]) {   
           sh "docker push fcaudillo/celeryreload "    
           
       }    
   }
   
   stage('Deploy a produccion') {
       sh "cd main && docker-compose stop celeryworker"
       sh "cd main && docker-compose up -d --no-deps --build celeryworker"
   }

}