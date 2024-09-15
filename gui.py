import json
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import webbrowser

def load_json_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def process_followers(data):
    followers = []
    for item in data:
        for user_data in item["string_list_data"]:
            followers.append(user_data["value"])
    return followers

def process_following(data):
    following = []
    for item in data["relationships_following"]:
        for user_data in item["string_list_data"]:
            following.append(user_data["value"])
    return following

def select_followers_file():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        followers_entry.delete(0, tk.END)
        followers_entry.insert(0, file_path)

def select_following_file():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        following_entry.delete(0, tk.END)
        following_entry.insert(0, file_path)

def open_instagram_profile(username):
    webbrowser.open(f"https://www.instagram.com/{username}")

def analyze_followers():
    followers_file = followers_entry.get()
    following_file = following_entry.get()

    if not followers_file or not following_file:
        messagebox.showerror("Error", "Please select both followers and following files.")
        return

    try:
        followers_data = load_json_file(followers_file)
        following_data = load_json_file(following_file)

        followers = process_followers(followers_data)
        following = process_following(following_data)

        not_following_back = set(following) - set(followers)

        # Clear previous results
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        # Add new results
        tk.Label(scrollable_frame, text="Accounts you follow but don't follow you back:").pack(pady=5)

        for username in not_following_back:
            frame = tk.Frame(scrollable_frame)
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            tk.Label(frame, text=username, anchor="w").pack(side=tk.LEFT)
            tk.Button(frame, text="Open Profile", command=lambda u=username: open_instagram_profile(u)).pack(side=tk.RIGHT)

        tk.Label(scrollable_frame, text=f"\nTotal followers: {len(followers)}").pack(pady=2)
        tk.Label(scrollable_frame, text=f"Total following: {len(following)}").pack(pady=2)
        tk.Label(scrollable_frame, text=f"Number of accounts not following you back: {len(not_following_back)}").pack(pady=2)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create main window
root = tk.Tk()
root.title("Instagram Follower Checker")
root.geometry("600x500")

tk.Label(root, text="Ektrak file zip, lalu cari file follower_1 dan following").pack(pady=5)

# Followers file selection
tk.Label(root, text="Follower_1 JSON:").pack(pady=5)
followers_entry = tk.Entry(root, width=50)
followers_entry.pack(side=tk.TOP, pady=5)
tk.Button(root, text="Browse", command=select_followers_file).pack(pady=5)

# Following file selection
tk.Label(root, text="Following JSON:").pack(pady=5)
following_entry = tk.Entry(root, width=50)
following_entry.pack(side=tk.TOP, pady=5)
tk.Button(root, text="Browse", command=select_following_file).pack(pady=5)

# Analyze button
tk.Button(root, text="Analyze", command=analyze_followers).pack(pady=10)

# Result display with scrollbar
result_frame = tk.Frame(root)
result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

canvas = tk.Canvas(result_frame)
scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

root.mainloop()
