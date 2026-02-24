import streamlit as st
import sqlite3

# ---------- Database Setup ----------
conn = sqlite3.connect("bookmarks.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bookmarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    url TEXT NOT NULL
)
""")
conn.commit()

# ---------- Functions ----------
def add_bookmark(title, url):
    cursor.execute("INSERT INTO bookmarks (title, url) VALUES (?, ?)", (title, url))
    conn.commit()

def get_bookmarks():
    cursor.execute("SELECT * FROM bookmarks")
    return cursor.fetchall()

def update_bookmark(id, title, url):
    cursor.execute("UPDATE bookmarks SET title=?, url=? WHERE id=?", (title, url, id))
    conn.commit()

def delete_bookmark(id):
    cursor.execute("DELETE FROM bookmarks WHERE id=?", (id,))
    conn.commit()

# ---------- UI ----------
st.title("📌 Smart Bookmark Manager")

menu = st.sidebar.selectbox("Choose Action", ["Add", "View", "Update", "Delete"])

# ADD
if menu == "Add":
    st.subheader("Add New Bookmark")
    title = st.text_input("Enter Title")
    url = st.text_input("Enter URL")

    if st.button("Add Bookmark"):
        if title and url:
            add_bookmark(title, url)
            st.success("Bookmark Added Successfully!")
        else:
            st.warning("Please fill all fields")

# VIEW
elif menu == "View":
    st.subheader("All Bookmarks")
    data = get_bookmarks()

    if data:
        for row in data:
            st.write(f"ID: {row[0]}")
            st.write(f"Title: {row[1]}")
            st.markdown(f"[Visit Link]({row[2]})")
            st.write("---")
    else:
        st.info("No bookmarks found")

# UPDATE
elif menu == "Update":
    st.subheader("Update Bookmark")
    data = get_bookmarks()
    ids = [row[0] for row in data]

    if ids:
        selected_id = st.selectbox("Select ID", ids)
        new_title = st.text_input("New Title")
        new_url = st.text_input("New URL")

        if st.button("Update"):
            update_bookmark(selected_id, new_title, new_url)
            st.success("Bookmark Updated Successfully!")
    else:
        st.info("No bookmarks available")

# DELETE
elif menu == "Delete":
    st.subheader("Delete Bookmark")
    data = get_bookmarks()
    ids = [row[0] for row in data]

    if ids:
        selected_id = st.selectbox("Select ID", ids)

        if st.button("Delete"):
            delete_bookmark(selected_id)
            st.success("Bookmark Deleted Successfully!")
    else:
        st.info("No bookmarks available")