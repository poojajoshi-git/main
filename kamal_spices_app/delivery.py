import pandas as pd
import os

ORDERS_FILE = "data/orders.xlsx"

def update_status(order_id, new_status):
    df = pd.read_excel(ORDERS_FILE)
    df.loc[df["OrderID"] == order_id, "Status"] = new_status
    df.to_excel(ORDERS_FILE, index=False)

def get_pending_orders():
    df = pd.read_excel(ORDERS_FILE)
    return df[df["Status"] != "Delivered"]