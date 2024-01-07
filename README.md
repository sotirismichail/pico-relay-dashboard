# Pico-Relay Control Dashboard
### MQTT-based control software and web dashboard for RaspberryPi Pico based relays

## Overview
Using MQTT, the user can turn on, off or power cycle the relays the RaspberryPi Pico W is controlling remotely. This control software has been written in MicroPython for the RaspberryPi Pico W software, uses RabbitMQ as the message broker, and StompJs for the web dashboard. Being an early version, excuse the crude design of the dashboard and the overall lack of any sleek features. 

Currently, only the basic control of the WaveShare Pico-Relay-B board is supported, which itself is using a RaspberryPi Pico W, thus making this project easy to adapt if one wishes to implement their own control board, by adapting the configuration file.

## Setting up the Pico W
First, to load the control software on the Raspberry Pi Pico, either boot into load mode using the on-board BOOTSEL button, or use Thonny. 

**Setting the network credentials and the MQTT host is necessary.**

For the network credentials, modify the config/secrets file and for the MQTT host details, modify the config/mqtt file. It is strongly recommended to change the credentials for the relay's MQTT access. Note the password you have used in order to set it during the deployment of RabbitMQ in the next step.

To do that, enter your wireless network's credentials to 
Afterwards, copy the latest Pico firmware and the contents of the "pico-control" folder into it, making sure the main file stands at the root of the Pico's internal storage.

## Setting up the control dashboard

To deploy the control dashboard, you need to create an .env file based on the sample file provided. After setting your access credentials there, set the users in the rabbitmq/definitions file, ensuring that the relay's credentials match the ones set in the previous step.

After setting the users, simple run

`docker compose build && docker compose up`

And the dashboard should be accessible at `localhost:80`

## Contact details
[Sotiris Michail (LinkedIn)](https://www.linkedin.com/in/smichail/) - [@michail_sotiris](https://twitter.com/michail_sotiris) - michailsotiris@outlook.com

Project Link: [https://github.com/sotirismichail/pico-relay-dashboard](https://github.com/sotirismichail/pico-relay-dashboard)