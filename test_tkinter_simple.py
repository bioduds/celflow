#!/usr/bin/env python3
"""
Simple tkinter test to verify GUI functionality
"""

import tkinter as tk
from tkinter import messagebox


def test_tkinter():
    """Test basic tkinter functionality"""
    try:
        # Create a simple window
        root = tk.Tk()
        root.title("SelFlow tkinter Test")
        root.geometry("300x200")

        # Add a label
        label = tk.Label(root, text="✅ tkinter is working!", font=("Arial", 16))
        label.pack(pady=50)

        # Add a button
        def on_click():
            messagebox.showinfo("Success", "tkinter is fully functional!")
            root.quit()

        button = tk.Button(
            root, text="Test Button", command=on_click, font=("Arial", 12)
        )
        button.pack(pady=20)

        print("✅ tkinter window created successfully")
        root.mainloop()

    except Exception as e:
        print(f"❌ tkinter test failed: {e}")
        return False

    return True


if __name__ == "__main__":
    print("🧪 Testing tkinter functionality...")
    success = test_tkinter()
    if success:
        print("✅ tkinter test completed successfully")
    else:
        print("❌ tkinter test failed")
