import RPi.GPIO as GPIO
import time
from flask import Flask, render_template, send_file, make_response, request, url_for

app = Flask(__name__)
channel = 21

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)


def motor_on(pin):
    GPIO.output(pin, GPIO.HIGH)  # Turn motor on
    relay_status = 'On'
    return relay_status


def motor_off(pin):
    GPIO.output(pin, GPIO.LOW)  # Turn motor off
    relay_status = 'Off'
    return relay_status


def check_relay_status():
    if GPIO.input(channel):
        pin_status = GPIO.input(channel)
    else:
        pin_status = GPIO.input(channel)
    return pin_status


@app.route("/relay", methods=['GET', 'POST'])
def relay():
    if "turn_on" in request.form:
        relay_status = motor_on(channel)
        print("Relay Energize Requested")
        GPIO.cleanup()


    if "turn_off" in request.form:
        relay_status = motor_off(channel)
        print("Relay Off Requested")
        GPIO.cleanup()


    return render_template('relay.html', relay_status=relay_status)


if __name__ == '__main__':
    try:
        GPIO.cleanup()
    except KeyboardInterrupt:
        GPIO.cleanup()