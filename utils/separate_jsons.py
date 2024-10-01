import json
import os
import sys

filename = sys.argv[1]

# Load the JSON data
with open(filename, 'r') as file:
    data = json.load(file)

# Create the output directory if it doesn't exist
output_base = os.path.dirname(filename)
output_dir = os.path.join(output_base, 'output')
stem = os.path.splitext(os.path.basename(filename))[0]
os.makedirs(output_dir, exist_ok=True)

# Write each dictionary to a separate file
for item in data:
    id = item['id']
    filename = f'{stem}_{id}.json'
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w') as file:
        json.dump(item, file, indent=2)
    print(f'Saved {filename}')
