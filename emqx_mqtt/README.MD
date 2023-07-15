
#### RUN cd emqx_mqtt/emqx_mosquitto_docker

#### RUN docker-compose -f emqx_docker-compose.yaml up -d

#### Default Usrname - admin
#### Default Password - public

## RUN cd ..
## RUN python emqx_sub.py
## RUN python emqx_pub.py