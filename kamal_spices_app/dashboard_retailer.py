import streamlit as st
from inventory import load_inventory, update_inventory
from orders import create_order, generate_invoice_pdf


def show():
    st.header("🏪 Retailer Dashboard")
    inventory_df = load_inventory()

    name = st.text_input("Retailer Name", key="retail_name")
    product = st.selectbox("Choose Product", inventory_df["Product"].tolist(), key="retail_product")
    quantity = st.number_input("Quantity (kg)", min_value=5, key="retail_qty")

    product_row = inventory_df[inventory_df["Product"] == product].iloc[0]
    st.image(product_row["Image"], width=200)
    st.write(f"💰 Price per kg: ₹{product_row['Price']}")
    total_price = quantity * product_row["Price"]
    st.write(f"🧾 Total: ₹{total_price}")

    if st.button("Place Bulk Order", key="retail_submit"):
        if product_row["Stock"] >= quantity:
            order = create_order(name, product, quantity, "Retailer")
            update_inventory(product, -quantity)
            st.success("Bulk order placed!")
            invoice_path = generate_invoice_pdf(order)
            with open(invoice_path, "rb") as f:
                st.download_button("Download PDF Invoice", f, file_name=invoice_path.split("/")[-1])
        else:
            st.error("Not enough stock available.")