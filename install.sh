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
### Setup python 3.6


