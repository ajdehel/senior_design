if [ $EUID -ne 0 ]; then
    echo "Please run as root."
    echo
    echo " $> sudo su"
    exit 1
fi

### Install MQTT Broker
apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
apt-get update
apt-get install mosquitto
apt-get install mosquitto-clients
### Install Python 3.6
add-apt-repository ppa:deadsnakes/ppa
apt-get update
apt-get install python3.6
### Install pip for Python3
apt-get install python3-pip
### Setup python 3.6
ln -s /usr/local/lib/python3.5 /usr/local/lib/python3.6
if [ -e /usr/bin/python3 ]; then
    echo "Changing symbolic link for /usr/bin/python3"
    rm /usr/bin/python3
fi
ln -s /usr/bin/python3 /usr/bin/python3.6
### MSSQL installs
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
### Install Plumbintel package
cd src
pip install .
### Move config file to /etc/
mv plumbintel.conf /etc
exit
