import streamlit as st
import json
import os
from datetime import datetime

class LibraryManager:
    def __init__(self):
        self.library = [] 
        self.filename = "library_data.json"
        self.load_library()

    def load_library(self):
        """Load library data from JSON file"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as file:
                    self.library = json.load(file)
        except Exception as e:
            self.library = []

    def save_library(self):
        """Save library data to JSON file"""
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.library, file, indent=4)
        except Exception as e:
            st.error(f"Error saving library: {e}")

    def add_book(self, title, author, year, genre, read_status):
        """Add a new book to the library"""
        book = {
            'title': title.strip(),
            'author': author.strip(),
            'year': year,
            'genre': genre.strip(),
            'read': read_status,
            'date_added': datetime.now().strftime("%Y-%m-%d")
        }
        self.library.append(book)
        self.save_library()

    def remove_book(self, title):
        """Remove a book from the library"""
        initial_count = len(self.library)
        self.library = [book for book in self.library if book['title'].lower() != title.lower()]
        if len(self.library) < initial_count:
            self.save_library()

    def search_books(self, search_term, search_by):
        """Search for books by title or author"""
        if search_by == "title":
            return [book for book in self.library if search_term.lower() in book['title'].lower()]
        elif search_by == "author":
            return [book for book in self.library if search_term.lower() in book['author'].lower()]

    def display_all_books(self):
        """Return all books in the library"""
        return self.library

    def display_statistics(self):
        """Return library statistics"""
        total_books = len(self.library)
        read_books = sum(1 for book in self.library if book['read'])
        read_percentage = (read_books / total_books) * 100 if total_books > 0 else 0
        return total_books, read_books, read_percentage

# Streamlit UI
def main():
    st.title("Personal Library Manager")

    library = LibraryManager()

    # Sidebar for navigation
    menu = ["Add Book", "Remove Book", "Search Books", "Display All Books", "Statistics"]
    choice = st.sidebar.selectbox("Choose an option", menu)

    # Add a book
    if choice == "Add Book":
        st.subheader("Add New Book")
        title = st.text_input("Enter title")
        author = st.text_input("Enter author")
        year = st.number_input("Enter publication year", min_value=1000, max_value=datetime.now().year)
        genre = st.text_input("Enter genre")
        read_status = st.radio("Has the book been read?", ('Yes', 'No')) == 'Yes'

        if st.button("Add Book"):
            if title and author and genre:
                library.add_book(title, author, year, genre, read_status)
                st.success(f"Book '{title}' added successfully!")
            else:
                st.warning("Please fill in all fields!")

    # Remove a book
    elif choice == "Remove Book":
        st.subheader("Remove Book")
        title = st.text_input("Enter the title of the book to remove")
        if st.button("Remove Book"):
            if title:
                library.remove_book(title)
                st.success(f"Book '{title}' removed successfully!")
            else:
                st.warning("Please enter a title!")

    # Search books
    elif choice == "Search Books":
        st.subheader("Search Books")
        search_by = st.radio("Search by", ['title', 'author'])
        search_term = st.text_input(f"Enter {search_by}")
        if st.button("Search"):
            if search_term:
                found_books = library.search_books(search_term, search_by)
                if found_books:
                    for book in found_books:
                        st.write(f"**Title**: {book['title']}")
                        st.write(f"**Author**: {book['author']}")
                        st.write(f"**Year**: {book['year']}")
                        st.write(f"**Genre**: {book['genre']}")
                        st.write(f"**Read**: {'Yes' if book['read'] else 'No'}")
                        st.write(f"**Date Added**: {book['date_added']}")
                        st.write("---")
                else:
                    st.warning("No books found!")
            else:
                st.warning("Please enter a search term!")

    # Display all books
    elif choice == "Display All Books":
        st.subheader("All Books")
        all_books = library.display_all_books()
        if all_books:
            for book in all_books:
                st.write(f"**Title**: {book['title']}")
                st.write(f"**Author**: {book['author']}")
                st.write(f"**Year**: {book['year']}")
                st.write(f"**Genre**: {book['genre']}")
                st.write(f"**Read**: {'Yes' if book['read'] else 'No'}")
                st.write(f"**Date Added**: {book['date_added']}")
                st.write("---")
        else:
            st.warning("No books in the library!")

    # Display statistics
    elif choice == "Statistics":
        st.subheader("Library Statistics")
        total_books, read_books, read_percentage = library.display_statistics()
        st.write(f"**Total Books**: {total_books}")
        st.write(f"**Books Read**: {read_books}")
        st.write(f"**Percentage Read**: {read_percentage:.1f}%")

if __name__ == "__main__":
    main()
