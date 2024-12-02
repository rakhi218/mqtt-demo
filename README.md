# MQTT-Messaging---FastAPI-RabbitMQ-MongoDB

Producer send MQTT msg every second with a "status" field containing a random value between 0 and 6 to RabbitMQ. FasApi server consumes the MQTT msg from RabbitMQ and stores in MongoDB with timestamps. It provides an endpoint that accept timestamp range and return the count of each status within the specified time range using aggregate pipeline.

# Important commands

# Setup guide
install docker

# follow the procedure defined
https://docs.docker.com/engine/install/ubuntu/

# run command - to install rabbitmq image
docker pull rabbitmq:3-management

# run the docker image
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 -p 1883:1883 rabbitmq:3-management 

# run below command to list rabbitmq container id and copy it
docker ps

# enable mqtt plugin
docker exec -it <container_id> rabbitmq-plugins enable rabbitmq_mqtt

# install python and create virutal env
sudo apt install python3
virtualenv <virtual_env_name>

# activate virtual env
source <virtual_env_name>/bin/activate

# install packages in requirements.txt
pip install -r requirements.txt

# install mongodb - follow the steps
https://www.geeksforgeeks.org/how-to-install-and-configure-mongodb-in-ubuntu/

# run the producer and consumer files
# producer
python3 -m producer

# consumer
uvicorn consumer:app --reload --port <port_number>