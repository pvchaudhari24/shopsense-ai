import streamlit as st
from products import products
import hashlib
import os

# -----------------------------
# BASE PATH (FIX FOR STREAMLIT CLOUD)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="ShopSense AI",
    page_icon="🛒",
    layout="wide"
)

# -----------------------------
# SESSION STATE
# -----------------------------
if "cart" not in st.session_state:
    st.session_state.cart = []

if "checkout" not in st.session_state:
    st.session_state.checkout = False

# -----------------------------
# STABLE RATING SYSTEM
# -----------------------------
def get_rating(name):
    hash_val = int(hashlib.md5(name.encode()).hexdigest(), 16)
    return round(3.5 + (hash_val % 15) / 10, 1)

# -----------------------------
# STYLE
# -----------------------------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #0b1220, #05070d);
    color: white;
}

.title {
    text-align: center;
    font-size: 52px;
    font-weight: 800;
    color: #38bdf8;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
}

.price {
    color: #22c55e;
    font-size: 18px;
    font-weight: bold;
}

div.stButton > button {
    width: 100%;
    border-radius: 10px;
    background-color: #2563eb;
    color: white;
}

div.stButton > button:hover {
    background-color: #1d4ed8;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("<div class='title'>🛒 ShopSense AI</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI Shopping Assistant</div>", unsafe_allow_html=True)

# -----------------------------
# INPUTS
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    search = st.text_input("Search products")

with col2:
    budget = st.slider("Budget", 0, 1000, 300)

with col3:
    category = st.selectbox("Category", ["All", "shoes", "electronics", "accessories"])

# -----------------------------
# FILTER PRODUCTS
# -----------------------------
filtered = []

for p in products:
    if category != "All" and p["category"] != category:
        continue

    if search.strip() == "" or (
        search.lower() in p["name"].lower() or
        search.lower() in p["category"].lower()
    ):
        if p["price"] <= budget:
            filtered.append(p)

# -----------------------------
# AI TOP PICK
# -----------------------------
def score(p):
    s = 0
    if search.lower() in p["name"].lower():
        s += 3
    s += max(0, 5 - (p["price"] / 150))
    return s

best = max(filtered, key=score) if filtered else None

# -----------------------------
# CART FUNCTION
# -----------------------------
def add_to_cart(pid):
    if pid not in st.session_state.cart:
        st.session_state.cart.append(pid)
        st.toast("Added to cart 🛒")
    else:
        st.toast("Already in cart")

# -----------------------------
# IMAGE SAFE LOADER (FIX)
# -----------------------------
def load_image(path):
    full_path = os.path.join(BASE_DIR, path)
    return full_path

# -----------------------------
# TOP PICK
# -----------------------------
if best:
    st.markdown("## 🏆 AI TOP PICK")

    colA, colB = st.columns([1, 2])

    with colA:
        st.image(load_image(best["image"]), use_container_width=True)

    with colB:
        st.markdown(f"### {best['name']}")
        st.markdown(f"<div class='price'>${best['price']}</div>", unsafe_allow_html=True)

        if st.button("Add Top Pick"):
            add_to_cart(best["id"])

# -----------------------------
# PRODUCT GRID
# -----------------------------
st.markdown("## 🛍️ Products")

cols = st.columns(4)

for i, item in enumerate(filtered):
    with cols[i % 4]:

        st.image(load_image(item["image"]), use_container_width=True)

        st.markdown(f"**{item['name']}**")
        st.markdown(f"<div class='price'>${item['price']}</div>", unsafe_allow_html=True)

        st.write(f"⭐ {get_rating(item['name'])}/5")

        if st.button("Add to Cart", key=item["id"]):
            add_to_cart(item["id"])

# -----------------------------
# SIDEBAR CART
# -----------------------------
st.sidebar.title("🛒 Cart")

cart_items = [p for p in products if p["id"] in st.session_state.cart]

total = 0

for item in cart_items:
    st.sidebar.write(f"{item['name']} - ${item['price']}")
    total += item["price"]

    if st.sidebar.button(f"Remove {item['name']}", key="rm_" + item["id"]):
        st.session_state.cart.remove(item["id"])
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.write(f"💰 Total: ${total}")

if cart_items and st.sidebar.button("Checkout"):
    st.session_state.checkout = True

# -----------------------------
# CHECKOUT
# -----------------------------
if st.session_state.checkout:

    st.markdown("## 🧾 Checkout")

    cart_items = [p for p in products if p["id"] in st.session_state.cart]

    total = sum(p["price"] for p in cart_items)

    for item in cart_items:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(load_image(item["image"]), width=100)
        with col2:
            st.write(item["name"])
            st.write(f"${item['price']}")

    st.markdown("---")
    st.markdown(f"### Total: ${total}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Confirm Purchase"):
            st.session_state.cart = []
            st.session_state.checkout = False
            st.success("Order placed successfully 🎉")

    with col2:
        if st.button("Cancel"):
            st.session_state.checkout = False
            st.rerun()