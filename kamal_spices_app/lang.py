# lang.py

translations = {
    "en": {
        "add_product": "Add Product",
        "product_name": "Product Name",
        "quantity": "Quantity",
        "submit": "Submit",
        "inventory_overview": "Inventory Overview",
    },
    "hi": {
        "add_product": "उत्पाद जोड़ें",
        "product_name": "उत्पाद का नाम",
        "quantity": "मात्रा",
        "submit": "जमा करें",
        "inventory_overview": "इन्वेंटरी अवलोकन",
    },
    "mr": {
        "add_product": "उत्पादन जोडा",
        "product_name": "उत्पादनाचे नाव",
        "quantity": "प्रमाण",
        "submit": "सबमिट करा",
        "inventory_overview": "साठा आढावा",
    }
}

def t(key, lang="en"):
    return translations.get(lang, translations["en"]).get(key, key)