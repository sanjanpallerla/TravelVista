import tkinter as tk
from tkinter import ttk, scrolledtext
import pandas as pd
from PIL import Image, ImageTk

# Assume 'data' is your DataFrame loaded elsewhere
file_path = 'travelvisitplaces.csv'
data = pd.read_csv(file_path)

def update_types(event):
    selected_state = state_var.get()
    types = sorted(list(data[data['State'].str.lower() == selected_state.lower()]['Type'].unique()))
    type_combobox['values'] = types
    type_combobox.current(0)

def update_ranges(event):
    selected_state = state_var.get()
    selected_type = type_var.get()
    if selected_state and selected_type:
        filtered_data = data[(data['State'].str.lower() == selected_state.lower()) &
                             (data['Type'].str.lower() == selected_type.lower())]
        if not filtered_data.empty:
            min_rating, max_rating = filtered_data['Google review rating'].min(), filtered_data['Google review rating'].max()
            min_fee, max_fee = filtered_data['Entrance Fee in INR'].min(), filtered_data['Entrance Fee in INR'].max()
            rating_scale.config(from_=min_rating, to=max_rating)
            fee_scale.config(from_=min_fee, to=max_fee)

def recommend():
    user_state = state_var.get()
    user_type = type_var.get()
    user_rating = float(rating_scale.get())
    user_fee = int(fee_scale.get())

    if user_state.lower() not in data['State'].str.lower().unique():
        result_label.config(text="State not found in the dataset. Please enter a valid state.")
    else:
        type_data = data[(data['State'].str.lower() == user_state.lower()) & 
                         (data['Type'].str.lower() == user_type.lower())]
        if not type_data.empty:
            recommendation = type_data[(type_data['Google review rating'] >= user_rating) & 
                                       (type_data['Entrance Fee in INR'] <= user_fee)]
            if not recommendation.empty:
                recommendations_text = ""
                for _, place in recommendation.iterrows():
                    recommendations_text += f"Name: {place['Name']}, Rating: {place['Google review rating']}, Entrance Fee: {place['Entrance Fee in INR']} INR\n"
                recommendation_display.delete('1.0', tk.END)
                recommendation_display.insert(tk.END, recommendations_text)
                recommended_place = recommendation.iloc[0]
                result_label.config(text=f"Found {len(recommendation)} recommendations.")
            else:
                result_label.config(text="Sorry, no places match your preferences.")
        else:
            result_label.config(text="No types found for the selected state. Please try a different state or type.")

root = tk.Tk()
root.title("Travel Place Recommendation System")
root.geometry("600x600")

# Load the background image
background_image = Image.open("tourismBg.jpg")
background_image = background_image.resize((1550, 1000), Image.BICUBIC)

# Create a copy of the image and adjust the opacity
background_image_opacity = background_image.copy()
background_image_opacity.putalpha(160)  # Adjust the opacity value (0-255)

background_photo = ImageTk.PhotoImage(background_image_opacity)

# Create a label with the background image
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Adding style components
style = ttk.Style()
style.configure('TButton', foreground='blue', font=('Arial', 12))
style.configure('TLabel', font=('Arial', 12))

title_label = ttk.Label(root, text="Travel Place Recommendation System", font=('Arial', 30, 'bold'))
title_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

state_var = tk.StringVar()
state_label = ttk.Label(root, text="Select a State:")
state_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
state_combobox = ttk.Combobox(root, textvariable=state_var)
state_combobox['values'] = sorted(list(data['State'].unique()))
state_combobox.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
state_combobox.bind('<<ComboboxSelected>>', update_types)

type_var = tk.StringVar()
type_label = ttk.Label(root, text="Select a Type:")
type_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
type_combobox = ttk.Combobox(root, textvariable=type_var)
type_combobox.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
type_combobox.bind('<<ComboboxSelected>>', update_ranges)

rating_label = ttk.Label(root, text="Minimum Rating Preference:")
rating_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
rating_scale = tk.Scale(root, from_=0, to=5, orient='horizontal', resolution=0.1)
rating_scale.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

fee_label = ttk.Label(root, text="Maximum Acceptable Entrance Fee:")
fee_label.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
fee_scale = tk.Scale(root, from_=0, to=5000, orient='horizontal')
fee_scale.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

result_label = ttk.Label(root, text="Your recommendation will appear here.", wraplength=350)
result_label.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

recommendation_display = scrolledtext.ScrolledText(root, height=10, width=50)
recommendation_display.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

recommend_button = ttk.Button(root, text="Recommend", command=recommend)
recommend_button.place(relx=0.5, rely=0.98, anchor=tk.CENTER)

root.mainloop()
