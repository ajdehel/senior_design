# PlumbIntelligent (a Senior Design project)

## Dependencies

This software was developed on and tested for Python 3.6 running on Ubuntu 16.04.

### Install MQTT Broker

sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
sudo apt-get update
sudo apt-get install mosquitto
sudo apt-get install mosquitto-clients

### Install Python 3.6

sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.6

### Install pip for Python3
apt-get install python3-pip

### MSSQL Installs

apt-get install msodbcsql
apt-get install mssql-tools
apt-get install unixodbc-dev
apt-get install mssql-server
apt-get update
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/16.04/mssql-server-2014.list | sudo tee /etc/apt/sources.list.d/mssql-server-2014.list
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/16.04/mssql-server-2017.list | sudo tee /etc/apt/sources.list.d/mssql-server-2017.list
/opt/mssql/bin/mssql-conf setup


