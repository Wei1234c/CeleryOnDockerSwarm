echo "# Set Docker hosts IPs ____________________________________"
rpi201='192.168.0.109'
rpi202='192.168.0.114'
master01=${rpi202}
node01=${rpi201}
echo ${master01}
echo ${node01}



eval $(docker-machine env master01)

echo "# Create Consul server ____________________________________"
docker                                 run -d --restart=always -p 8500:8500  --name=consul --hostname=consul nimblestratus/rpi-consul -server -bootstrap 
  
  
  
echo "# Create Swarm manager ____________________________________"
docker run -d \
--restart=always \
--name swarm-agent-master \
-p 3376:3376 \
-v /etc/docker:/etc/docker \
hypriot/rpi-swarm \
manage \
--tlsverify \
--tlscacert=/etc/docker/ca.pem \
--tlscert=/etc/docker/server.pem \
--tlskey=/etc/docker/server-key.pem \
-H tcp://0.0.0.0:3376 \
--strategy spread  consul://${master01}:8500

 docker run -d \
--restart=always \
--name swarm-agent \
hypriot/rpi-swarm \
join --advertise ${master01}:2376 consul://${master01}:8500


echo " Create Swarm node ____________________________________"
eval $(docker-machine env node01)
docker run -d \
--restart=always \
--name swarm-agent \
hypriot/rpi-swarm \
join --advertise ${node01}:2376 consul://${master01}:8500


  
docker $(docker-machine config --swarm master01) info  