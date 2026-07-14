import base64
import tkinter as tk

import customtkinter as ctk
from PIL import Image, ImageTk
import cv2

from app.models.image_data import ImageData


class ImageViewer(ctk.CTkFrame):
    
    # Image Viewer Component

    def __init__(self, master):

        super().__init__(master)

        self.image_label = None
        self.info_label = None
        self.photo = None

        self.build_ui()

    def build_ui(self):

        title = ctk.CTkLabel(
            self,
            text="Attendance Sheet Preview",
            font=("Arial", 20, "bold")
        )

        title.pack(pady=10)

        self.image_label = ctk.CTkLabel(
            self,
            text=""
        )

        self.image_label.pack(
            padx=15,
            pady=10
        )

        self.info_label = ctk.CTkTextbox(
            self,
            width=400,
            height=170
        )

        self.info_label.pack(
            padx=10,
            pady=10,
            fill="x"
        )

        self.info_label.configure(state="disabled")

    def display_image(self, image_data: ImageData):

        image = image_data.rgb_image

        image = Image.fromarray(image)

        image.thumbnail((900, 650))

        self.photo = ImageTk.PhotoImage(image)

        self.image_label.configure(
            image=self.photo
        )

        self.image_label.image = self.photo

        self.show_information(image_data)

    def show_information(self, image_data: ImageData):

        info = image_data.summary()

        self.info_label.configure(state="normal")

        self.info_label.delete(
            "1.0",
            "end"
        )

        for key, value in info.items():

            self.info_label.insert(
                "end",
                f"{key:<20}: {value}\n"
            )

        self.info_label.configure(
            state="disabled"
        )

    def clear(self):

        self.image_label.configure(
            image=None,
            text="No Image Loaded"
        )

        self.info_label.configure(state="normal")

        self.info_label.delete(
            "1.0",
            "end"
        )

        self.info_label.configure(
            state="disabled"
        )