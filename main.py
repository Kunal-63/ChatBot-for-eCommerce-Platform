import os
import pandas as pd
from fuzzywuzzy import process
import re

def extract_price_range(prompt):
    # Regular expression pattern to match price range specified as various expressions
    pattern = r'(less\s*than|under|lower\s*than|cheaper\s*than|more\s*than|over|higher\s*than|pricier\s*than|between|inside|within)\s*(\d+)(?:\s*and\s*(\d+))?'
    match = re.search(pattern, prompt)
    if match:
        comparison_operator = match.group(1).strip()  # Extract the comparison operator
        lower_limit = int(match.group(2))  # Extract the lower limit
        upper_limit = int(match.group(3)) if match.group(3) else float('inf')  # Extract the upper limit if present, set to infinity if absent
        return comparison_operator, lower_limit, upper_limit
    else:
        return None, None, None  # Return None for all values if no match found

def suggest_products(prompt):
    # Map keywords to product categories
    category_mapping = {
        't-shirts': 't-shirts.csv',
        'shirts': 'shirts.csv',
        'hoodies': 'hoodies_sweatshirts.csv',
        'jeans': 'jeans.csv',
        'trousers': 'trousers.csv',
        'blazers': 'blazers.csv',
        'jackets': 'jackets.csv',
        'shorts': 'shorts.csv',
        'shoes': 'shoes.csv',
        'bags': 'bags_backpacks.csv',
        'accessories': 'accessories.csv',
        'perfumes': 'perfumes.csv',
        'beauty': 'beauty.csv',
        'polo': 'polo shirts.csv',
        'overshirts': 'overshirts.csv',
        'swimwear': 'swin_wear.csv'
    }

    # Known brands and colors
    known_brands = ['puma', 'adidas', 'zara', 'nike']
    known_colors = ['black', 'white', 'blue', 'red', 'green', 'yellow']

    # Process user prompt to identify keywords
    keywords = prompt.lower().split()

    # Extract price range from user prompt
    comparison_operator, min_price, max_price = extract_price_range(prompt)

    print("Comparison Operator:", comparison_operator)  # Debugging
    print("Min Price:", min_price)  # Debugging
    print("Max Price:", max_price)  # Debugging

    # Fuzzy matching to find the closest category match
    best_match = process.extractOne(prompt.lower(), category_mapping.keys())

    print("Best Match:", best_match)  # Debugging

    # If no match found or similarity is below a threshold, return error message
    if best_match is None or best_match[1] < 50:
        return "Sorry, I couldn't identify the product category mentioned in your prompt."

    # Retrieve the CSV file for the best match category
    category = category_mapping[best_match[0]]
    csv_file = os.path.join('menswear_data', category)
    print("CSV File:", csv_file)  # Debugging

    # If CSV file does not exist, return error message
    if not os.path.exists(csv_file):
        return "Sorry, I couldn't find any products in that category."

    # Read the CSV file
    df = pd.read_csv(csv_file)
    print("Column Names:", df.columns.tolist())  # Debugging

    # Check if the required columns exist in the DataFrame
    required_columns = ['product_name', 'price', 'link', ' product_images', 'brand', 'color']
    if not all(col in df.columns for col in required_columns):
        return "Sorry, the product data is incomplete."

    # Convert 'price' column to numeric type
    df['price'] = pd.to_numeric(df['price'], errors='coerce')

    # Filter products based on price range
    # Filter products based on price range
    if comparison_operator in ["less than", "under", "less then", "below", "lower than", "lower then", "cheaper than", "cheaper then", "less expensive than", "less expensive then", "inside", "within"]:
        df = df[df['price'] < min_price]
        print("Filtered DataFrame:", df)
    elif comparison_operator in ["more than", "over", "more then", "above", "higher than", "higher then", "pricier than", "pricier then", "more expensive than", "more expensive then"]:
        df = df[df['price'] > min_price]
        print("Filtered DataFrame:", df)
    elif comparison_operator == "between":
        df = df[(df['price'] >= min_price) & (df['price'] <= max_price)]
        print("Filtered DataFrame:", df)


    # Filter products based on brand and color
    brand_prompt = [word for word in keywords if word in known_brands]
    color_prompt = [word for word in keywords if word in known_colors]
    if brand_prompt:
        df = df[df['brand'].str.lower().isin(brand_prompt)]
    if color_prompt:
        df = df[df['color'].str.lower().isin(color_prompt)]

    if len(df) == 0:
        return "Sorry, I couldn't find any products in that category within the specified price range."
    else:
        return df[required_columns].head(5).to_dict(orient='records')

user_prompt = "show me black nike shoes more than 1000"
recommendations = suggest_products(user_prompt)
for i in recommendations:
    print(i, end="\n\n")
