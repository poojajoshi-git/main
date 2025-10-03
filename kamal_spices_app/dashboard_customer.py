import streamlit as st
from inventory import load_inventory
from orders import create_order, generate_invoice_pdf

def show_inventory():
    inventory_df = load_inventory()
    if "Image" in inventory_df.columns:
        inventory_df = inventory_df.drop(columns=["Image"])
    st.subheader("📦 Inventory Table")
    st.dataframe(inventory_df)
    return inventory_df

def show():
    st.header("🛍️ Customer Dashboard")
    st.write(f"Welcome, {st.session_state.username}")

    inventory_df = show_inventory()

    product = st.selectbox("Select Product", inventory_df["Product"])
    quantity = st.number_input("Quantity (kg)", min_value=1)

    if "order_placed" not in st.session_state:
        st.session_state.order_placed = False

    if st.button("Place Order"):
        order = create_order(st.session_state.username, product, quantity, "Customer")
        invoice_path = generate_invoice_pdf(order)
        st.session_state.order_placed = True
        st.session_state.invoice_path = invoice_path
        st.rerun()

    if st.session_state.order_placed:
        st.success("Order placed successfully!")
        with open(st.session_state.invoice_path, "rb") as f:
            st.download_button("Download Invoice", f, file_name=st.session_state.invoice_path.split("/")[-1])
        # Reset flag after showing
        st.session_state.order_placed = False

    st.subheader("🗣️ Feedback")
    st.markdown("[Click here to share your feedback](https://forms.gle/your-google-form-id)", unsafe_allow_html=True)

    if st.session_state.get("logged_in", False):
        st.divider()
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔙 Back to Main Screen"):
                st.session_state.logged_in = False

        with col2:
            if st.button("🚪 Logout"):
                for key in ["logged_in", "username", "role"]:
                    st.session_state.pop(key, None)
                st.success("Logged out successfully!")