import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageOps
from keras.models import load_model
import numpy as np

class Task3: 
    # Load the model
    model = load_model("keras_Model.h5", compile=False)

    # Load the labels
    class_names = open("labels.txt", "r").readlines()

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
        return class_name, confidence_score

    def __init__(self):
        # Create a Tkinter window
        self.root = tk.Tk()
        self.root.geometry("300x300")
        self.root.title("Flower Species Classification")  # Set the title here

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
        self.result_text.set(f"Class: {class_name}\nConfidence Score: {confidence_score}")


