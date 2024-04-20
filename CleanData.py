import pandas as pd
import json

# Read the CSV file into a DataFrame
df = pd.read_csv("your_file.csv")

# Function to extract the URL from the product_images column
def extract_url(images):
    try:
        
        # Parse the JSON-like string
        image_list = json.loads(images.replace("'", "\""))
        # Extract the URLs from the first dictionary
        urls = list(image_list[0].keys())
        return urls[0] if urls else None
    except Exception as e:
        return None

# Apply the function to the product_images column
df['product_images'] = df['product_images'].apply(extract_url)

# Save the modified DataFrame back to the CSV file
df.to_csv("your_modified_file.csv", index=False)
