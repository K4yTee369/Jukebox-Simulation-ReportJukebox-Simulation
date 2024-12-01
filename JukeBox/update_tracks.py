import tkinter as tk
import tkinter.scrolledtext as tkst
from tkinter import messagebox
import track_library as lib
import font_manager as fonts



def set_text(text_area, content):
    text_area.delete("1.0", tk.END)
    text_area.insert("1.0", content)



class UpdateTrack:
    def __init__(self, window):
        window.geometry("600x350")
        window.title("Update Track List")

        track_lbl = tk.Label(window, text="Enter Track Number")
        track_lbl.grid(row=0, column=1, padx=10, pady=10)

        self.track_num_entry = tk.Entry(window, width=3)
        self.track_num_entry.grid(row=0, column=2, padx=10, pady=10)

        rating_lbl = tk.Label(window, text="Enter Rating (1-5)")
        rating_lbl.grid(row=1, column=1, padx=10, pady=10)

        self.rating_entry = tk.Entry(window, width=3)
        self.rating_entry.grid(row=1, column=2, padx=10, pady=10)

        update_btn = tk.Button(window, text="Update Rating", command=self.update_rating)
        update_btn.grid(row=2, column=1, columnspan=2, pady=10)

        self.list_txt = tkst.ScrolledText(window, width=60, height=12, wrap="none")
        self.list_txt.grid(row=3, column=0, columnspan=3, sticky="W", padx=10, pady=10)

        self.display_all_tracks()




    def display_all_tracks(self):
        all_tracks = lib.list_all()
        set_text(self.list_txt, all_tracks)



    def update_rating(self):
        track_num = self.track_num_entry.get()
        try:
            new_rating = int(self.rating_entry.get())
            if new_rating < 1 or new_rating > 5:
                raise ValueError("Rating out of bounds")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid rating between 1 and 5.")
            return

        track_name = lib.get_name(track_num)
        if track_name:
            lib.set_rating(track_num, new_rating)
            play_count = lib.get_play_count(track_num)
            
            message = f"Track: {track_name}\nNew Rating: {new_rating}\nPlay Count: {play_count}"
            messagebox.showinfo("Rating Updated", message)
            self.display_all_tracks()
        else:
            messagebox.showerror("Track Not Found", "The track number entered does not exist.")



if __name__ == "__main__":  
    window = tk.Tk()        
    fonts.configure()
    UpdateTrack(window)     
    window.mainloop()
