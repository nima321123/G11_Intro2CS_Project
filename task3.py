import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageOps, ImageTk
from keras.models import load_model
import numpy as np
import pyttsx3


class Task3: 
    # Load the model
    model = load_model("keras_Model.h5", compile=False)

    # Load the labels
    class_names = [line.strip() for line in open("labels.txt", "r").readlines()]

    def select_image(self):
        # Open file dialog to select an image file
        file_path = filedialog.askopenfilename()
        
        # Process the image and make a prediction
        image = Image.open(file_path).convert("RGB")
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        data[0] = normalized_image_array

        prediction = self.model.predict(data)
        index = np.argmax(prediction)
        class_name = self.class_names[index]
        confidence_score = prediction[0][index]

        # Display the image in the Tkinter window
        # Display the image in the Tkinter window
        image = image.resize((300, 300), Image.Resampling.LANCZOS)  
        # Use Image.Resampling.LANCZOS instead of Image.ANTIALIAS

        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo  # Keep a reference to the image to prevent it from being garbage collected

        return class_name, confidence_score

    def get_suggestion(self, class_name):
        # Provide suggestions based on the weather condition
        suggestions = {
            "Snowing": "Stay warm and enjoy the snow! \nDrive slowly and carefully on snowy or icy roads to stay safe.",
            "Cloudy": "It might be a bit gloomy outside. \nBring a light jacket or sweater in case it gets chilly.",
            "Raining": "Don't forget your umbrella or raincoat!",
            "Sunshine": "It's a great day for outdoor activities. \nRemember to put on sunscreen to protect your skin from the sun. Stay hydrated by drinking plenty of water.",
        }
        return suggestions.get(class_name, "The weather condition is not recognized. Please try again.")

    def __init__(self):
        # Create a Tkinter window
        self.root = tk.Tk()
        self.root.geometry("400x400")
        self.root.title("Weather condition")  # Set the title here

        # Add a label to display the image
        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        # Add a label to display the prediction and confidence score
        self.result_text = tk.StringVar()
        result_label = tk.Label(self.root, textvariable=self.result_text)
        result_label.pack()

        # Add a button to select an image
        select_button = tk.Button(self.root, text="Select an image", command=self.update_result_text)
        select_button.pack()

        # Start the Tkinter event loop
        self.root.mainloop()

    def update_result_text(self):
        class_name, confidence_score = self.select_image()
        suggestion = self.get_suggestion(class_name)
        self.result_text.set(f"Class: {class_name}\nConfidence Score: {confidence_score}\nSuggestion: {suggestion}")
        
        # Initialize the text-to-speech engine
        engine = pyttsx3.init()
        # Set the properties for the speech
        engine.setProperty('rate', 125)     # Speed of speech
        engine.setProperty('volume', 0.8)  # Volume (0.0 to 1.0)
        # Say the text
        engine.say(f"Weather condition: {class_name}. {suggestion}")
        # Wait for the speech to finish
        engine.runAndWait()
   
Task3()
