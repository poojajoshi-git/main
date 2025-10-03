import pandas as pd
import os
from reportlab.pdfgen import canvas

from app.kamal_spices_app.inventory import load_inventory


def read_excel_safe(path, columns=None):
    if not os.path.exists(path):
        return pd.DataFrame(columns=columns if columns else [])
    return pd.read_excel(path)

def write_excel_safe(df, path):
    df.to_excel(path, index=False)

def generate_order_id():
    from datetime import datetime
    return f"KMP-{int(datetime.now().timestamp())}"

def export_analytics_pdf(summary_df, filename="data/reports/analytics.pdf"):
    c = canvas.Canvas(filename)
    c.setFont("Helvetica", 12)
    c.drawString(50, 800, "Kamal Food Products - Monthly Analytics")
    y = 780
    for index, row in summary_df.iterrows():
        c.drawString(50, y, f"{index}: Orders={row['Orders']}, Quantity={row['Quantity']}")
        y -= 20
    c.save()
    return filename

translations = {
    "en": {"Order": "Order", "Customer": "Customer"},
    "hi": {"Order": "ऑर्डर", "Customer": "ग्राहक"},
    "mr": {"Order": "ऑर्डर", "Customer": "ग्राहक"}
}

def t(key, lang="en"):
    return translations.get(lang, {}).get(key, key)

import cv2

def scan_qr_or_barcode(image_path):
    detector = cv2.QRCodeDetector()
    img = cv2.imread(image_path)

    if img is None:
        return "Image not found or unreadable"

    data, bbox, _ = detector.detectAndDecode(img)
    if bbox is not None and data:
        inventory_df = load_inventory()
        match = inventory_df[inventory_df["Code"].astype(str) == data]
        if not match.empty:
            product = match.iloc[0]["Product"]
            price = match.iloc[0]["Price"]
            stock = match.iloc[0]["Stock"]
            return f"✅ Match Found: {product} | ₹{price}/kg | Stock: {stock} kg"
        else:
            return f"🔍 Code detected: {data} — No matching product found"
    else:
        return "No QR code or barcode detected"
