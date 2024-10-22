import json
import os
import sys

filename = sys.argv[1]
suffix = sys.argv[2]

# Load the JSON data
with open(filename, 'r') as file:
    data = json.load(file)

# Create the output directory if it doesn't exist
self_file_path = os.path.realpath(__file__)
output_base = os.path.join(os.path.dirname(self_file_path), '../sample_data')
output_dir = os.path.join(output_base, "_".join(['output', suffix]))
stem = os.path.basename(filename).split("-")[0]
os.makedirs(output_dir, exist_ok=True)

# Write each dictionary to a separate file
for item in data:
    id = item['id']
    filename = f'{stem}_{id}.json'
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w') as file:
        json.dump(item, file, indent=2)
    print(f'Saved {filename}')
