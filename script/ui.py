import tkinter as tk
import time

class ErzaehlomatUI:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)  # Vollbild
        self.root.configure(bg='beige')  # Hintergrundfarbe Beige

        # question label
        self.question_label = tk.Label(
            root,
            text="Hallo! Das ist der Erzählomat",  # Startfrage
            font=("Arial", 50),  # Große Schrift
            bg="beige",
            fg="black",
            wraplength=1000,
            justify="center"
        )
        self.question_label.place(relx=0.5, rely=0.4, anchor="center")

        # empty frame
        self.base_label = tk.Label(
            root,
            text="",  # Anweisung
            font=("Arial", 24),
            bg="beige",
            fg="black",
            justify="center",
            wraplength=500
        )
        self.base_label.place(relx=0.5, rely=0.8, anchor="center", width=600, height=300)

        # Escape-Taste zum Beenden
        root.bind('<Escape>', lambda e: root.destroy())
    
    def show_recording_frame(self):
        """
        shows Frame if visible.
        If already visible its not shown again.
        """
        self.base_label.config(text="Aufnahme läuft...",
            font=("Arial", 30),
            bg="red",
            fg="black",
            justify="center",
            wraplength=500,            
            bd=2,
            relief="groove")
        self.root.update()

    def show_saved_frame(self):
        """
        changes base frame to saved frame.
        """
        self.base_label.config(text="Aufnahme gespeichert",
            font=("Arial", 30),
            bg="green",
            fg="white",
            justify="center",
            wraplength=500,            
            bd=2)
        self.root.update()

    def show_wait_frame(self):
        """
        changes base frame to saved frame.
        """
        self.base_label.config(text="Bitte warten",  # Anweisung
            font=("Arial", 30),
            bg="white",
            fg="black",
            justify="center",
            wraplength=500,
            bd=2,)
        self.root.update()       

    def hide_frame(self):
        """
        Changes back to invisible base frame
        """
        self.base_label.config(text="",bg="beige",bd=0)
        self.root.update()

    # Methode zum Aktualisieren der Frage
    def update_question(self, new_question):
        """
        Updates Label with new question.
        :param new_question: The new question to be displayed. Needs a string.
        :type new_question: str"
        """
        self.question_label.config(text=new_question)
        self.root.update()


def main():
    root = tk.Tk()
    ui = ErzaehlomatUI(root)

    # from ui2 import ErzaehlomatUI
    # ui = ErzaehlomatUI(root)
    
    # Update questions sequentially with delays
    ui.update_question("Was war Ihr nächst schöneres Erlebnis?")
    time.sleep(1)
    ui.update_question("Wie alt sind Sie?")
    time.sleep(1)
    ui.show_wait_frame()
    time.sleep(1)
    ui.show_recording_frame()
    time.sleep(1)
    ui.show_saved_frame()
    time.sleep(1)
    ui.hide_frame()
    time.sleep(1)

if __name__ == "__main__":
    main()