import pandas as pd
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import qrcode
import smtplib
from email.mime.text import MIMEText
from inventory import load_inventory


INVOICE_DIR = "data/invoices"
ORDERS_FILE = "data/orders.xlsx"

# Ensure folders exist
os.makedirs("data", exist_ok=True)
os.makedirs(INVOICE_DIR, exist_ok=True)

def create_order(customer, product, quantity, role):
    # Load or create orders file
    if not os.path.exists(ORDERS_FILE):
        df = pd.DataFrame(columns=["OrderID", "Date", "Customer", "Product", "Quantity", "Type", "Status"])
    else:
        df = pd.read_excel(ORDERS_FILE)

    # Create new order
    order_id = f"KMP-{int(datetime.now().timestamp())}"
    new_order = {
        "OrderID": order_id,
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Customer": customer,
        "Product": product,
        "Quantity": quantity,
        "Type": role,
        "Status": "Pending"
    }
    df = pd.concat([df, pd.DataFrame([new_order])], ignore_index=True)
    df.to_excel(ORDERS_FILE, index=False)

    # ✅ Update inventory
    inventory_file = "data/inventory.xlsx"
    if os.path.exists(inventory_file):
        inventory = pd.read_excel(inventory_file)
        if product in inventory["Product"].values:
            current_stock = inventory.loc[inventory["Product"] == product, "Stock"].values[0]
            updated_stock = max(current_stock - quantity, 0)
            inventory.loc[inventory["Product"] == product, "Stock"] = updated_stock
            inventory.to_excel(inventory_file, index=False)

    # ✅ Send email alert
    send_email_alert(new_order)

    return new_order

def generate_invoice_pdf(order):
    inventory_df = load_inventory()
    product_row = inventory_df[inventory_df["Product"] == order["Product"]]
    price = product_row.iloc[0]["Price"] if not product_row.empty else 0
    hsn = product_row.iloc[0].get("HSN", "0910")

    gst_rate = 0.05
    base_amount = order["Quantity"] * price
    gst_amount = base_amount * gst_rate
    total = base_amount + gst_amount

    if not os.path.exists(INVOICE_DIR):
        os.makedirs(INVOICE_DIR)

    filename = f"{INVOICE_DIR}/invoice_{order['OrderID']}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    c.setFont("Helvetica", 12)

    # Header
    c.drawString(50, 800, "Kamal Food Products")
    c.drawString(50, 785, "GSTIN: 27ABCDE1234F1Z5")
    c.drawString(50, 770, "Address: Ahilyanagar, Maharashtra, India")

    # Order Info
    c.drawString(50, 740, f"Order ID: {order['OrderID']}")
    c.drawString(50, 725, f"Date: {order['Date']}")
    c.drawString(50, 710, f"Customer: {order['Customer']}")
    c.drawString(50, 695, f"Product: {order['Product']} (HSN: {hsn})")
    c.drawString(50, 680, f"Quantity: {order['Quantity']} kg")
    c.drawString(50, 665, f"Price per kg: ₹{price:.2f}")

    # Tax Breakdown
    c.drawString(50, 640, f"Base Amount: ₹{base_amount:.2f}")
    c.drawString(50, 625, f"GST (5%): ₹{gst_amount:.2f}")
    c.drawString(50, 610, f"Total Amount: ₹{total:.2f}")

    # QR Code
    qr = qrcode.make(f"OrderID: {order['OrderID']}, Total: ₹{total:.2f}")
    qr_path = f"{INVOICE_DIR}/qr_{order['OrderID']}.png"
    qr.save(qr_path)
    c.drawImage(qr_path, 400, 700, width=100, height=100)

    c.save()
    return filename

def send_email_alert(order):
    try:
        msg = MIMEText(f"New order placed:\n\nOrder ID: {order['OrderID']}\nCustomer: {order['Customer']}\nProduct: {order['Product']}\nQuantity: {order['Quantity']} kg\nType: {order['Type']}")
        msg["Subject"] = f"🧾 New Order: {order['OrderID']}"
        msg["From"] = "your_email@example.com"
        msg["To"] = "admin@example.com"

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("your_email@example.com", "your_password")
            server.send_message(msg)
    except Exception as e:
        print(f"Email alert failed: {e}")