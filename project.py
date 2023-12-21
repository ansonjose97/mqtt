import json
import time
import paho.mqtt.client as mqtt

# Define the MQTT settings
broker_address = "broker.hivemq.com"
publish_topic = "cloud_to_vehicle/commands"
subscribe_topic = "vehicle_to_cloud/telemetry"

# MQTT client instantiation
cloud_client = mqtt.Client("Cloud_Service")
vehicle_client = mqtt.Client("Vehicle_Service")

# Define the on_connect callback for the cloud client
def cloud_on_connect(client, userdata, flags, rc):
    print("Cloud Service Connected with result code " + str(rc))

# Define the on_connect callback for the vehicle client
def vehicle_on_connect(client, userdata, flags, rc):
    print("Vehicle Connected with result code " + str(rc))
    # Subscribe to the commands topic once connected
    client.subscribe(publish_topic)

# Define the on_message callback for the vehicle client
def vehicle_on_message(client, userdata, msg):
    command = json.loads(msg.payload)  # Assume that command is a JSON string
    print(f"Vehicle received command: {command}")
    # Vehicle would process the command here and perform actions

# Configure cloud client
cloud_client.on_connect = cloud_on_connect

# Configure vehicle client
vehicle_client.on_connect = vehicle_on_connect
vehicle_client.on_message = vehicle_on_message

# Connect both clients to the broker
cloud_client.connect(broker_address, 1883, 60)
vehicle_client.connect(broker_address, 1883, 60)

# Start the loop for both clients
cloud_client.loop_start()
vehicle_client.loop_start()

# Simulate sending a command from the cloud to the vehicle
command_data = {
    "command": "lock_doors",
    "parameters": {
        "lock": True
    }
}

# Cloud publishes a command to the vehicle
cloud_client.publish(publish_topic, json.dumps(command_data))

# Vehicle would be continuously listening for commands, and the on_message callback handles any commands received
# This is simulated here with a sleep, in a real-world scenario the vehicle client would be running on the vehicle's system
time.sleep(2)

# Publish telemetry data as a response from the vehicle to the cloud
telemetry_data = {
    "vehicle_id": "WP0ZZZ99ZTS392124",
    "status": "doors_locked"
}

# Vehicle publishes telemetry data to the cloud
vehicle_client.publish(subscribe_topic, json.dumps(telemetry_data))

# Give some time for the communication to complete
time.sleep(2)

# Stop the loop for both clients and disconnect
cloud_client.loop_stop()
vehicle_client.loop_stop()
cloud_client.disconnect()
vehicle_client.disconnect()
