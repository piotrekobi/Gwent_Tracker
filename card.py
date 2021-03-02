import tkinter as tk
from PIL import ImageTk


class Card:
    def __init__(self, app, names, image, tk_image, card_type, provisions,
                 strength, count, row_num, dimensions):
        self.app = app
        self.text = names.get("English")
        self.names = names
        self.image = image
        self.original_tk_image = tk_image
        self.tk_image = tk_image
        self.type = card_type
        self.strength = strength
        self.original_count = count
        self.count = count
        self.dimensions = dimensions
        self.card_canvas = tk.Canvas(width=self.dimensions.get("width"),
                                     height=self.dimensions.get("height"),
                                     bd=-2,
                                     highlightthickness=0)
        self.card_canvas.bind("<Button-1>", self.card_clicked)
        self.card_canvas.grid(row=row_num, columnspan=4)
        self.set_content()

    def remove(self):
        self.card_canvas.grid_remove()

    def set_content(self):
        self.card_canvas.delete("all")
        self.card_canvas.create_image(0, 0, anchor="nw", image=self.tk_image)
        if self.count > 0:
            self.card_canvas.create_text(
                self.dimensions.get("width") // 10,
                self.dimensions.get("height") // 2,
                fill="white",
                anchor="w",
                font=("Arial", self.dimensions.get("font_size")),
                text=self.text)
        if self.count == 2:
            self.card_canvas.create_text(
                0.9 * self.dimensions.get("width"),
                self.dimensions.get("height") // 2,
                fill="white",
                anchor="w",
                font=("Arial", self.dimensions.get("font_size") + 2),
                text="x2")

    def card_clicked(self, event):
        if self.count == 2:
            self.count = 1
            self.set_content()
        elif self.count == 1:
            self.image = self.image.convert("LA")
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.count = 0
            self.set_content()
        else:
            return
        self.app.undo_button.config(state="normal")
        self.app.cards_clicked.append(self)
