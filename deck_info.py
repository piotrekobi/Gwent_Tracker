from data_scraper import deck_data
from card import Card
from deck_selection import DeckSelection

from PIL import ImageTk, Image
from io import BytesIO

import tkinter as tk


class MainApp:
    def __init__(self):
        self.current_cards = []
        self.cards_clicked = []
        self.main_window = tk.Tk()

        self.screen_center_width = self.main_window.winfo_screenwidth() // 3
        self.screen_center_height = self.main_window.winfo_screenheight() // 3

        self.main_window.title("Gwent Deck Tracker")
        self.main_window.withdraw()
        self.main_window.resizable(False, False)
        self.main_window.geometry(
            f"+{self.screen_center_width}+0")

        self.new_button = tk.Button(self.main_window,
                                    text="New",
                                    command=self.new_button_clicked)
        self.new_button.grid(row=0, column=0, sticky="nesw")
        self.restart_button = tk.Button(self.main_window,
                                        text="Restart",
                                        command=self.restart_button_clicked)
        self.restart_button.grid(row=0, column=1, sticky="nesw")
        self.undo_button = tk.Button(self.main_window,
                                     text="Undo",
                                     command=self.undo_button_clicked,
                                     state="disabled")
        self.undo_button.grid(row=0, column=2, sticky="nesw")

        self.language_choice = tk.StringVar(self.main_window)
        self.language_menu = tk.OptionMenu(self.main_window,
                                           self.language_choice,
                                           "English",
                                           "Localized",
                                           command=self.language_menu_clicked)
        self.language_menu.config(width=2)
        self.current_language = "English"
        self.language_choice.set("English")
        self.language_menu.grid(row=0, column=3, sticky="nesw")

        new_window = tk.Toplevel(bg="gray")
        new_window.geometry(
            f"+{self.screen_center_width}+{self.screen_center_height}")
        new_window.protocol("WM_DELETE_WINDOW", self.main_window.destroy)

        try:
            self.show_deck_selection_window(new_window)
            self.main_window.deiconify()
            self.main_window.mainloop()
        except tk._tkinter.TclError:
            exit(0)

    def new_button_clicked(self):
        self.undo_button.config(state="disabled")
        self.cards_clicked.clear()
        new_window = tk.Toplevel(bg="gray")
        new_window.geometry(
            f"+{self.screen_center_width}+{self.screen_center_height}")
        new_window.protocol("WM_DELETE_WINDOW", self.main_window.destroy)

        self.show_deck_selection_window(new_window)

    def show_deck_selection_window(self, selection_window):
        selection_window.grab_set()
        DeckSelect = DeckSelection(selection_window)
        self.main_window.wait_window(selection_window)
        card_info = deck_data(DeckSelect.url)
        if card_info is None:
            self.main_window.destroy()
            return
        self.show_deck(card_info)

    def restart_button_clicked(self):
        self.undo_button.config(state="disabled")
        self.cards_clicked.clear()
        for row in self.current_cards:
            row.count = row.original_count
            row.tk_image = row.original_tk_image
            row.set_content()

    def undo_button_clicked(self):
        card = self.cards_clicked.pop()
        if len(self.cards_clicked) == 0:
            self.undo_button.config(state="disabled")
        if card.count == 0:
            card.tk_image = card.original_tk_image
            card.count = 1
        elif card.count == 1:
            card.count = card.original_count
        card.set_content()

    def language_menu_clicked(self, value):
        if self.current_language == value:
            return
        self.current_language = value
        for card in self.current_cards:
            card.text = card.names.get(value)
            card.set_content()

    def show_deck(self, card_info):
        images = []
        tk_images = []
        for row in self.current_cards:
            row.remove()

        self.current_cards.clear()
        card_dimensions = {
            "width": 6000 // len(card_info),
            "height": 800 // len(card_info),
            "font_size": 35 - len(card_info)
        }
        for (i, card) in enumerate(card_info):
            image = Image.open(BytesIO(card.get("image")))
            image = image.resize(
                (card_dimensions.get("width"), card_dimensions.get("height")))
            images.append(image)
            tk_images.append(ImageTk.PhotoImage(image))
            names = {
                "English": card.get("name"),
                "Localized": card.get("local_name")
            }
            row = Card(self, names, images[i], tk_images[i], card.get("type"),
                       card.get("provisions"), card.get("strength"),
                       card.get("count"), i + 1, card_dimensions)
            self.current_cards.append(row)


MainApp()
