import time

import network
import ujson
from config.mqtt import MQTT_CLIENT_ID
from config.mqtt import MQTT_HOST
from config.mqtt import MQTT_PASS
from config.mqtt import MQTT_PORT
from config.mqtt import MQTT_USER
from config.mqtt import PUBLISH_INTERVAL
from config.mqtt import PUBLISH_TOPIC
from config.mqtt import SUBSCRIBE_TOPIC
from config.pin_layouts import WAVESHARE_PICO_RELAY_B as PIN_LAYOUT
from config.secrets import WIFI_PASS
from config.secrets import WIFI_SSID
from interfaces.beeper import Beeper
from interfaces.neopixel import NeoPixel
from machine import Pin
from picozero import pico_temp_sensor
from umqtt.simple import MQTTClient

relays = [Pin(PIN_LAYOUT["CH" + str(i)], Pin.OUT) for i in range(1, 9)]
status_led = NeoPixel()
buzzer = Beeper(PIN_LAYOUT["BUZZER"])


def connect_to_wifi(wlan):
    if not wlan.isconnected():
        print("[NETWORK] Attempting to connect to:", WIFI_SSID)
        wlan.active(True)
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            time.sleep(1)
    print("[NETWORK] Connected to:", wlan.ifconfig()[0])


def sub_cb(topic, msg):
    print(f"[COMM] Received: {msg}")
    try:
        data = ujson.loads(msg)
        buzzer.short_beep()
        for ch, action in data.items():
            if ch == "chall":
                for relay in relays:
                    if action == "up":
                        relay.on()
                    elif action == "down":
                        relay.off()
                    elif action == "cycle":
                        relay.off()
                        time.sleep(5)
                        relay.on()
            else:
                relay_num = int(ch[2:]) - 1
                if 0 <= relay_num < len(relays):
                    if action == "up":
                        relays[relay_num].on()
                    elif action == "down":
                        relays[relay_num].off()
                    elif action == "cycle":
                        relays[relay_num].off()
                        time.sleep(5)
                        relays[relay_num].on()
    except ValueError:
        print("[COMM/ERROR] Invalid message received")


def publish_status(client):
    relay_status = {
        f"CH{i+1}": "on" if relay.value() else "off" for i, relay in enumerate(relays)
    }
    status_payload = {
        "temp": pico_temp_sensor.temp,
        "relays": relay_status,
    }
    print(status_payload)
    client.publish(PUBLISH_TOPIC, ujson.dumps(status_payload))


def mqtt_connect(wlan, status_led, buzzer):
    while True:
        try:
            mqtt_client = MQTTClient(
                MQTT_CLIENT_ID,
                MQTT_HOST,
                MQTT_PORT,
                MQTT_USER,
                MQTT_PASS,
            )
            mqtt_client.set_callback(sub_cb)
            mqtt_client.connect()
            mqtt_client.subscribe(SUBSCRIBE_TOPIC)
            print("[MQTT] Connected to MQTT Broker:", MQTT_HOST)

            return mqtt_client
        except Exception as e:
            print("[MQTT] Failed to connect to MQTT Broker:", e)
            status_led.pulsate_color(status_led.RED, pulse_duration=2)
            buzzer.long_beep()
            time.sleep(5)


def main():
    wlan = network.WLAN(network.STA_IF)
    connect_to_wifi(wlan)

    try:
        mqtt_client = mqtt_connect(wlan, status_led, buzzer)
        last_published_time = time.time()

        while True:
            try:
                status_led.set_color(status_led.GREEN)
                mqtt_client.check_msg()
                if (time.time() - last_published_time) >= PUBLISH_INTERVAL:
                    publish_status(mqtt_client)
                    last_published_time = time.time()
                time.sleep(1)

            except OSError as e:
                print("[MQTT] MQTT connection error:", e)
                status_led.pulsate_color(status_led.ORANGE, pulse_duration=2)
                buzzer.long_beep()
                mqtt_client = mqtt_connect(wlan, status_led, buzzer)

            except Exception as e:
                print("[SYSTEM] An unexpected error occurred:", e)
                status_led.pulsate_color(status_led.RED, pulse_duration=2)
                buzzer.long_beep()

    except Exception as e:
        print("[SYSTEM] Critical error:", e)
        status_led.pulsate_color(status_led.RED, pulse_duration=2)
        buzzer.long_beep()

    finally:
        if mqtt_client:
            mqtt_client.disconnect()
        wlan.disconnect()


if __name__ == "__main__":
    main()
