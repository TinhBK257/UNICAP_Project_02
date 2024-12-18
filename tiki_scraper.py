import requests
import json
import pandas as pd
import time
from pathlib import Path
import math

# Read product IDs from Excel file
df = pd.read_csv('tiki_product_IDs.csv')
product_ids = df['id'].tolist()

# Create output directory if it doesn't exist
output_dir = Path('tiki_products')
output_dir.mkdir(exist_ok=True)

# Function to get product details
def get_product_details(product_id):
    url = f'https://api.tiki.vn/product-detail/api/v1/products/{product_id}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Extract required fields
            return {
                'id': data.get('id'),
                'name': data.get('name'),
                'url_key': data.get('url_key'),
                'price': data.get('price'),
                'description': data.get('description'),
                'image_url': data.get('images', [{}])[0].get('url') if data.get('images') else None
            }
        return None
    except:
        return None

# Process products in batches of 1000
batch_size = 1000
total_batches = math.ceil(len(product_ids) / batch_size)

for batch_num in range(total_batches):
    start_idx = batch_num * batch_size
    end_idx = min((batch_num + 1) * batch_size, len(product_ids))
    batch_products = []
    
    print(f"Processing batch {batch_num + 1}/{total_batches}")
    
    for product_id in product_ids[start_idx:end_idx]:
        product_data = get_product_details(product_id)
        if product_data:
            batch_products.append(product_data)
        time.sleep(0.1)  # Add delay to avoid overwhelming the API
    
    # Save batch to JSON file
    if batch_products:
        output_file = output_dir / f'tiki_products_batch_{batch_num + 1}.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(batch_products, f, ensure_ascii=False, indent=2)
        
        print(f"Saved {len(batch_products)} products to {output_file}")

print("Data collection completed")