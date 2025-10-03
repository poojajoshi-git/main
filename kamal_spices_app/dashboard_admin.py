import streamlit as st
import pandas as pd
import os

ORDERS_FILE = "data/orders.xlsx"
INVENTORY_FILE = "data/inventory.xlsx"

# 📥 Load orders
def load_orders():
    if os.path.exists(ORDERS_FILE):
        return pd.read_excel(ORDERS_FILE)
    else:
        return pd.DataFrame(columns=["OrderID", "Date", "Customer", "Product", "Quantity", "Type", "Status"])

# 📥 Load inventory
def load_inventory():
    if os.path.exists(INVENTORY_FILE):
        return pd.read_excel(INVENTORY_FILE)
    else:
        return pd.DataFrame(columns=["Product", "Stock", "Barcode"])

# 💾 Save new inventory item
def save_inventory_item(product, stock, barcode):
    df = load_inventory()
    new_row = pd.DataFrame([[product, stock, barcode]], columns=["Product", "Stock", "Barcode"])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_excel(INVENTORY_FILE, index=False)

# 🛠️ Admin dashboard
def show():
    apply_custom_style()
    st.header("🛠️ Admin Dashboard")
    st.write(f"Welcome, {st.session_state.username}")

    # 📦 Orders section
    st.subheader("📦 Orders")
    orders_df = load_orders()

    status_filter = st.selectbox("Filter Orders by Status", ["All", "Pending", "Delivered"])
    filtered_df = orders_df if status_filter == "All" else orders_df[orders_df["Status"] == status_filter]

    # ✅ Manual table with headers and buttons
    header_cols = st.columns([2, 2, 2, 1.5, 1.5, 1.5, 2])
    header_cols[0].write("**Order ID**")
    header_cols[1].write("**Customer**")
    header_cols[2].write("**Product**")
    header_cols[3].write("**Quantity**")
    header_cols[4].write("**Type**")
    header_cols[5].write("**Status**")
    header_cols[6].write("**Action**")

    for i, row in filtered_df.iterrows():
        cols = st.columns([2, 2, 2, 1.5, 1.5, 1.5, 2])
        cols[0].write(row["OrderID"])
        cols[1].write(row["Customer"])
        cols[2].write(row["Product"])
        cols[3].write(f"{row['Quantity']} kg")
        cols[4].write(row["Type"])
        cols[5].write(row["Status"])

        if row["Status"] != "Delivered":
            if cols[6].button("✅ Mark Delivered", key=row["OrderID"]):
                full_df = load_orders()
                full_df.loc[full_df["OrderID"] == row["OrderID"], "Status"] = "Delivered"
                full_df.to_excel(ORDERS_FILE, index=False)
                st.success(f"Order {row['OrderID']} marked as Delivered")
                st.rerun()
        else:
            cols[6].write("✔️ Delivered")

    # 📊 Order summary chart
    st.subheader("📊 Order Summary")
    summary = orders_df["Status"].value_counts()
    st.bar_chart(summary)

    # 📦 Inventory section
    st.subheader("📦 Inventory Overview")
    inventory_df = load_inventory()
    if "Image" in inventory_df.columns:
        inventory_df = inventory_df.drop(columns=["Image"])
    st.dataframe(inventory_df)

    # 🔄 Update stock for existing products
    st.subheader("🔄 Update Inventory Stock")
    existing_products = inventory_df["Product"].tolist()
    selected_product = st.selectbox("Select Product", existing_products)
    added_stock = st.number_input("Add Quantity (kg)", min_value=0)

    if st.button("Update Stock"):
        inventory_df.loc[inventory_df["Product"] == selected_product, "Stock"] += added_stock
        inventory_df.to_excel(INVENTORY_FILE, index=False)
        st.success(f"{added_stock} kg added to {selected_product}")
        st.rerun()

    # ➕ Add new product
    st.subheader("➕ Add New Product")
    with st.form("add_new_product"):
        new_product = st.text_input("Product Name")
        new_stock = st.number_input("Initial Stock (kg)", min_value=0)
        new_barcode = st.text_input("Barcode")
        submitted = st.form_submit_button("Add Product")

        if submitted:
            if new_barcode in inventory_df["Barcode"].values:
                st.error("Barcode already exists.")
            else:
                save_inventory_item(new_product, new_stock, new_barcode)
                st.success(f"{new_product} added to inventory.")
                st.rerun()

    # 📤 Export orders
    st.subheader("📤 Export Orders")
    csv = orders_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Orders CSV", csv, file_name="orders.csv", mime="text/csv")

    # 🚪 Navigation
    if st.session_state.get("logged_in", False):
        st.divider()
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔙 Back to Main Screen"):
                st.session_state.logged_in = False
                st.rerun()

        with col2:
            if st.button("🚪 Logout"):
                for key in ["logged_in", "username", "role"]:
                    st.session_state.pop(key, None)
                st.success("Logged out successfully!")
                st.rerun()