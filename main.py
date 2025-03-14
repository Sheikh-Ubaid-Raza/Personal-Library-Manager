import json
import os
import streamlit as st

# File to store library data
data_file = 'example.txt'

def load_library():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            return json.load(file)
    return []

def save_library(library):
    with open(data_file, 'w') as file:
        json.dump(library, file, indent=4)

# Load library data
library = load_library()

# Custom CSS for better UI
st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 10px;
            width: 100%;
        }
        .stTextInput>div>div>input {
            border-radius: 5px;
        }
        .stMetric {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("📚 Library Manager Menu")
menu = st.sidebar.radio("Choose an action", [
    "Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "View Statistics"])

# Add a Book
if menu == "Add a Book":
    st.title("➕ Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1000, max_value=9999, step=1)
    category = st.text_input("Category")
    read = st.checkbox("Have you read this book?")
    
    if st.button("Add Book"):
        if title and author and year and category:
            new_book = {
                "title": title,
                "author": author,
                "year": year,
                "category": category,
                "read": read
            }
            library.append(new_book)
            save_library(library)
            st.success(f'✅ Book "{title}" added successfully!')
        else:
            st.error("❌ Please fill all fields!")

# Remove a Book
elif menu == "Remove a Book":
    st.title("🗑️ Remove a Book")
    remove_title = st.text_input("Enter title to remove")
    if st.button("Remove Book"):
        updated_library = [book for book in library if book["title"].lower() != remove_title.lower()]
        if len(updated_library) < len(library):
            save_library(updated_library)
            st.success(f'🗑️ Book "{remove_title}" removed successfully!')
        else:
            st.error(f'❌ Book "{remove_title}" not found!')

# Search for a Book
elif menu == "Search for a Book":
    st.title("🔍 Search for a Book")
    search_by = st.radio("Search by", ["Title", "Author"])
    search_term = st.text_input(f"Enter {search_by.lower()}")
    if st.button("Search"):
        results = [book for book in library if search_term.lower() in book[search_by.lower()].lower()]
        if results:
            st.write("### 🔎 Search Results")
            for book in results:
                st.write(f'📘 **{book["title"]}** by *{book["author"]}* ({book["year"]}) - {"✅ Read" if book["read"] else "❌ Not Read"}')
        else:
            st.warning("❌ No books found!")

# Display All Books
elif menu == "Display All Books":
    st.title("📚 Library Collection")
    if library:
        for book in library:
            st.write(f'📘 **{book["title"]}** by *{book["author"]}* ({book["year"]}) - {"✅ Read" if book["read"] else "❌ Not Read"}')
    else:
        st.info("📭 The library is empty.")

# Display Statistics
elif menu == "View Statistics":
    st.title("📊 Library Statistics")
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    perc_read = (read_books / total_books) * 100 if total_books > 0 else 0
    
    st.metric("📖 Total Books", total_books)
    st.metric("📖 Books Read", read_books)
    st.metric("📈 Percentage Read", f"{perc_read:.2f}%")