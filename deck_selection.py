import tkinter as tk


class DeckSelection:
    def __init__(self, window):
        self.url = ""
        self.show_window(window)

    def show_window(self, window):
        self.window = window
        self.window.resizable(False, False)
        self.window.geometry("520x50")
        link_label = tk.Label(window,
                              text="Deck link:",
                              font=("Arial", 15),
                              bg="gray",
                              fg="white").place(x=200, y=3)
        self.link_text_field = tk.Text(window,
                                       width=55,
                                       height=1,
                                       font=("Arial", 13),
                                       bg="lightgray",
                                       highlightthickness=0)
        self.link_text_field.place(x=10, y=25)
        self.link_text_field.bind("<Return>", self.set_deck_link)
        submit_button = tk.Button(window,
                                  text="Confirm",
                                  font=("Arial", 14),
                                  highlightbackground="gray",
                                  command=self.set_deck_link).place(x=460,
                                                                    y=22)

    def set_deck_link(self, event=None):
        self.url = self.link_text_field.get("1.0", "end-1c")
        self.close_window()

    def close_window(self):
        self.window.destroy()
