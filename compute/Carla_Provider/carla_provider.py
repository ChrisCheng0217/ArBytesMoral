import carla
import time
import math
import paho.mqtt.client as mqtt
import json

# -------------------------------
# Configuration
# -------------------------------
CARLA_HOST = '192.168.43.249'
CARLA_PORT = 2000
TM_PORT = 8000

MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC_SPEED = 'carla/vehicle/speed'
MQTT_TOPIC_LAT = 'carla/vehicle/lat'
MQTT_TOPIC_LON = 'carla/vehicle/lon'
MQTT_TOPIC_ALT = 'carla/vehicle/alt'
MQTT_TOPIC_WETNESS = 'carla/vehicle/wetness'

# -------------------------------
# Helper functions
# -------------------------------
def velocity_to_speed_kmh(vel):
    return math.sqrt(vel.x**2 + vel.y**2 + vel.z**2) * 3.6

def mqtt_publish(client, topic, value):
    client.publish(topic, str(value))

# -------------------------------
# Connect to MQTT
# -------------------------------
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
mqtt_client.loop_start()
print(f"Connected to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")

# -------------------------------
# Connect to CARLA
# -------------------------------
client = carla.Client(CARLA_HOST, CARLA_PORT)
client.set_timeout(10.0)

world = client.get_world()

# Synchronous mode
settings = world.get_settings()
settings.synchronous_mode = True
settings.fixed_delta_seconds = 0.05
world.apply_settings(settings)

# Blueprints and spawn points
blueprints = world.get_blueprint_library()
spawn_points = world.get_map().get_spawn_points()

# -------------------------------
# Spawn vehicle
# -------------------------------
vehicle = None
if spawn_points:
    bp = blueprints.find("vehicle.mercedes.coupe_2020")
    vehicle = world.spawn_actor(bp, spawn_points[0])
    vehicle.set_autopilot(True, TM_PORT)
    print(f"Vehicle spawned: {bp.id}, autopilot enabled on TM port {TM_PORT}")
else:
    raise RuntimeError("No spawn points found in CARLA map")

# -------------------------------
# Attach GNSS sensor
# -------------------------------
gnss_bp = blueprints.find("sensor.other.gnss")
gnss_bp.set_attribute("sensor_tick", "0.05")
gnss_transform = carla.Transform(carla.Location(x=0.0, y=0.0, z=1.8))
gnss_sensor = world.spawn_actor(gnss_bp, gnss_transform, attach_to=vehicle)

gnss_data = {"lat": 0.0, "lon": 0.0, "alt": 0.0}

def gnss_callback(measurement):
    gnss_data["lat"] = measurement.latitude
    gnss_data["lon"] = measurement.longitude
    gnss_data["alt"] = measurement.altitude

gnss_sensor.listen(gnss_callback)

# -------------------------------
# Main loop: tick world, update weather, publish to MQTT
# -------------------------------
cnt = 0
direction_up = True

try:
    while True:
        world.tick()  # advance simulation

        # Animate wetness 0..20
        if direction_up:
            cnt += 1
            if cnt >= 20:
                direction_up = False
        else:
            cnt -= 1
            if cnt <= 0:
                direction_up = True
                cnt = 0
        wetness = cnt

        # Read speed
        speed = velocity_to_speed_kmh(vehicle.get_velocity())

        # Read GNSS
        lat, lon, alt = gnss_data["lat"], gnss_data["lon"], gnss_data["alt"]

        # Publish to MQTT
        mqtt_publish(mqtt_client, MQTT_TOPIC_SPEED, speed)
        mqtt_publish(mqtt_client, MQTT_TOPIC_LAT, lat)
        mqtt_publish(mqtt_client, MQTT_TOPIC_LON, lon)
        mqtt_publish(mqtt_client, MQTT_TOPIC_ALT, alt)
        mqtt_publish(mqtt_client, MQTT_TOPIC_WETNESS, wetness)

        print(f"Speed: {speed:.1f} km/h | lat: {lat:.6f}, lon: {lon:.6f}, alt: {alt:.1f} m | Wetness: {wetness} %")

        time.sleep(0.05)  # match fixed_delta_seconds

except KeyboardInterrupt:
    print("Simulation stopped by user")

finally:
    # Cleanup
    if gnss_sensor is not None:
        gnss_sensor.stop()
        gnss_sensor.destroy()
    if vehicle is not None:
        vehicle.destroy()

    # Restore async mode
    settings = world.get_settings()
    settings.synchronous_mode = False
    settings.fixed_delta_seconds = None
    world.apply_settings(settings)
    mqtt_client.loop_stop()
    print("Vehicle destroyed and world restored to async mode")

