import random
import datetime
import json
import requests


def generate_random_data(server_name, start_time, num_entries, interval_minutes):
    """
    Generate random but believable data for a Minecraft server.

    Args:
        server_name (str): Name of the server.
        start_time (datetime): Starting timestamp for the data.
        num_entries (int): Number of data entries to generate.
        interval_minutes (int): Time interval between data points in minutes.

    Returns:
        list: A list of dictionaries containing the generated data.
    """
    data = []
    current_time = start_time

    for _ in range(num_entries):
        tps = round(random.uniform(14.5, 20.0), 2)  # TPS close to 20
        chunks = random.randint(400, 600)  # Chunks loaded
        cpu_usage = round(random.uniform(50, 80), 2)  # CPU usage in percentage
        memory_usage = round(random.uniform(60, 90), 2)  # Memory usage in percentage

        data.append({
            "server_name": server_name,
            "metric_name": "TPS",
            "value": tps,
            "timestamp": current_time.isoformat()
        })
        data.append({
            "server_name": server_name,
            "metric_name": "Chunks",
            "value": chunks,
            "timestamp": current_time.isoformat()
        })
        data.append({
            "server_name": server_name,
            "metric_name": "CPU_Usage",
            "value": cpu_usage,
            "timestamp": current_time.isoformat()
        })
        data.append({
            "server_name": server_name,
            "metric_name": "Memory_Usage",
            "value": memory_usage,
            "timestamp": current_time.isoformat()
        })

        # Increment the time by the specified interval
        current_time += datetime.timedelta(minutes=interval_minutes)

    return data

def generate_smooth_data(server_name, start_time, num_entries, interval_minutes):
    """
    Generate smooth and believable data for a Minecraft server.

    Args:
        server_name (str): Name of the server.
        start_time (datetime): Starting timestamp for the data.
        num_entries (int): Number of data entries to generate.
        interval_minutes (int): Time interval between data points in minutes.

    Returns:
        list: A list of dictionaries containing the generated data.
    """
    data = []
    current_time = start_time

    # Initial values for metrics
    tps = 20.0
    chunks = 500
    cpu_usage = 65.0
    memory_usage = 75.0

    for _ in range(num_entries):
        # Gradually adjust TPS, keeping it close to 20
        tps += random.uniform(-0.1, 0.1)
        tps = max(19.5, min(20.0, round(tps, 2)))  # Clamp between 19.5 and 20.0

        # Gradually adjust chunks, keeping it within a reasonable range
        chunks += random.randint(-10, 10)
        chunks = max(400, min(600, chunks))  # Clamp between 400 and 600

        # Gradually adjust CPU usage
        cpu_usage += random.uniform(-1.0, 1.0)
        cpu_usage = max(50.0, min(80.0, round(cpu_usage, 2)))  # Clamp between 50% and 80%

        # Gradually adjust memory usage
        memory_usage += random.uniform(-1.0, 1.0)
        memory_usage = max(60.0, min(90.0, round(memory_usage, 2)))  # Clamp between 60% and 90%

        # Add data points for each metric
        data.append({
            "server_name": server_name,
            "metric_name": "TPS",
            "value": tps,
            "timestamp": current_time.isoformat()
        })
        data.append({
            "server_name": server_name,
            "metric_name": "Chunks",
            "value": chunks,
            "timestamp": current_time.isoformat()
        })
        data.append({
            "server_name": server_name,
            "metric_name": "CPU_Usage",
            "value": cpu_usage,
            "timestamp": current_time.isoformat()
        })
        data.append({
            "server_name": server_name,
            "metric_name": "Memory_Usage",
            "value": memory_usage,
            "timestamp": current_time.isoformat()
        })

        # Increment the time by the specified interval
        current_time += datetime.timedelta(minutes=interval_minutes)

    return data

if __name__ == "__main__":
    # Configuration
    server_name = "MinecraftServer"
    start_time = datetime.datetime(2025, 4, 6, 12, 0, 0)  # Starting at 2025-04-06 12:00:00
    num_entries = 50  # Number of data points
    interval_minutes = 5  # 5-minute intervals

    # Generate data
    random_data = generate_smooth_data(server_name, start_time, num_entries, interval_minutes)

    # Print the generated data as JSON
    print(json.dumps(random_data, indent=2))

    r = requests.post("http://localhost:8000/data", json=random_data)
    print(r.status_code)