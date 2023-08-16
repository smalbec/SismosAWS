import json
import random
import time

def generate_random_data():
    
    timestamp = int(time.time()) - random.randint(1, 630720000)  # Generate a timestamp within the last 20 years
    country = random.choice(["CL", "BR", "AF", "US", "CN", "IN", "RU", "AU", "CA", "JP"])
    magnitude = round(random.uniform(3.0, 8.0), 1) 
    data = {
        "timestamp": timestamp,
        "country": country,
        "magnitude": magnitude
    }
    return data

data_strings = []

for _ in range(100):
    event_data = generate_random_data()
    data_string = json.dumps(event_data, indent=4)
    data_strings.append(data_string)

output = '{ "sismos": '+"[\n" + ",\n".join(data_strings) + "\n]}"

with open("dataSismosPOSTbody.json", "w") as file:
    file.write(output)

print("Data randomizada ha sido generada y guardada a 'dataSismosPOSTbody.json'.")