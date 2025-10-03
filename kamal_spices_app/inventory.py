import pandas as pd
import os

INVENTORY_FILE = "data/inventory.xlsx"

def load_inventory():
    if not os.path.exists(INVENTORY_FILE):
        df = pd.DataFrame({
            "Product": ["Turmeric", "Chili", "Coriander", "Garam Masala"],
            "Stock": [100, 100, 100, 100],
            "Price": [120, 150, 130, 200],
            "Image": [
                "https://kamalfoodproducts.com/images/turmeric.jpg",
                "https://kamalfoodproducts.com/images/chili.jpg",
                "https://kamalfoodproducts.com/images/coriander.jpg",
                "https://kamalfoodproducts.com/images/garammasala.jpg"
            ]
        })
        df.to_excel(INVENTORY_FILE, index=False)
    else:
        df = pd.read_excel(INVENTORY_FILE)

    # Ensure required columns
    if "Price" not in df.columns:
        df["Price"] = [120, 150, 130, 200]
    if "Image" not in df.columns:
        df["Image"] = [
            "https://kamalfoodproducts.com/images/turmeric.jpg",
            "https://kamalfoodproducts.com/images/chili.jpg",
            "https://kamalfoodproducts.com/images/coriander.jpg",
            "https://kamalfoodproducts.com/images/garammasala.jpg"
        ]
    return df

def update_inventory(product, change):
    df = load_inventory()
    df.loc[df["Product"] == product, "Stock"] += change
    df.to_excel(INVENTORY_FILE, index=False)

