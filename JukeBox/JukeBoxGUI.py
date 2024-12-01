import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.scrolledtext as tkst
from PIL import ImageTk, Image

import track_library as lib
import font_manager as fonts
from image import Image4Song

def set_text(text_area, content):
    text_area.delete("1.0", tk.END)
    text_area.insert("1.0", content)

class JukeBox:
    def __init__(self, window):
        window.geometry("920x500") 
        window.title("JukeBox")
        
        self.playlist = []
        self.img_song = Image4Song()
    
        list_all_btn = tk.Button(window, text="List All", command=self.display_all_tracks)
        list_all_btn.grid(row=0, column=0)

        self.list_txt = tkst.ScrolledText(window, width=30, height=8, wrap="none")
        self.list_txt.grid(row=1, column=0, columnspan=3, sticky="W", padx=10, pady=10)
        
        self.search_txt = tk.Entry(window, width=20)
        self.search_txt.grid(row=2, column=1)
        
        search_lbl = tk.Label(window, text="Search by Name/Artist")
        search_lbl.grid(row=2, column=0, padx=10, pady=10)
        
        search_btn = tk.Button(window, text="Search", command=self.search_tracks_clicked)
        search_btn.grid(row=3, column=0, padx=10, pady=10)
        
        list_lbl = tk.Label(window, text="Create your playlist")
        list_lbl.grid(row=0, column=2, padx=10, pady=10)   

        self.track_txt = tk.Text(window, width=48, height=8, wrap="none")
        self.track_txt.grid(row=1, column=2, sticky="NW", padx=10, pady=10)
        
        self.input_txt = tk.Entry(window, width=3)
        self.input_txt.grid(row=2, column=2, padx=10, pady=10)
        
        add_tracks_btn = tk.Button(window, text="Add Tracks", command=self.add_track)
        add_tracks_btn.grid(row=3, column=2, padx=10, pady=10)
        
        play_tracks_btn = tk.Button(window, text="Play Tracks", command=self.play_playlist)
        play_tracks_btn.grid(row=4, column=2, padx=10, pady=10)
        
        clear_tracks_btn = tk.Button(window, text="Clear All Tracks", command=self.reset_playlist)
        clear_tracks_btn.grid(row=5, column=2, padx=10, pady=10)
        
        rating_track_lbl = tk.Label(window, text="Rating Track")
        rating_track_lbl.grid(row=0, column=3, padx=10, pady=10)   

        track_lbl = tk.Label(window, text="Enter Track Number")
        track_lbl.grid(row=1, column=3, padx=10, pady=10)

        self.track_num_entry = tk.Entry(window, width=3)
        self.track_num_entry.grid(row=1, column=4, padx=10, pady=10)

        rating_lbl = tk.Label(window, text="Enter Rating (1-5)")
        rating_lbl.grid(row=2, column=3, padx=10, pady=10)

        self.rating_entry = tk.Entry(window, width=3)
        self.rating_entry.grid(row=2, column=4, padx=10, pady=10)

        update_btn = tk.Button(window, text="Update Rating", command=self.update_rating)
        update_btn.grid(row=3, column=3, columnspan=2, pady=10)
        
        self.image_lb = tk.Label(window)
        self.image_lb.grid(row=4, column=0, padx=10, pady=10)

        self.display_all_tracks()
        

    def add_track(self):
        key = self.input_txt.get()
        name = lib.get_name(key)
        if name:
            image_path = self.img_song.get_image_path(key)
            artist = lib.get_artist(key)
            play_count = lib.get_play_count(key)

            track_details = {
                "key": key,
                "name": name,
                "artist": artist,
                "play_count": play_count
            }
            self.playlist.append(track_details)
            self.update_playlist_text()
            if image_path:
                self.display_image(image_path)
            else:
                self.image_lb.config(image='', text="No image available for this track.")
        else:
            messagebox.showerror("Error", "Invalid track number.")

    def update_playlist_text(self):
        display_text = "\n".join(
            f"{track['key']}: {track['name']} ({track['artist']}), plays: {track['play_count']}"
            for track in self.playlist
        )
        self.track_txt.delete("1.0", tk.END)
        self.track_txt.insert(tk.END, display_text + "\n")

    def reset_playlist(self):
        self.playlist = []
        self.update_playlist_text()
    
    def display_all_tracks(self):
        all_tracks = lib.list_all()
        set_text(self.list_txt, all_tracks)
        
    def play_playlist(self):
        if not self.playlist:
            messagebox.showinfo("Playlist Empty", "There are no tracks in the playlist to play.")
            return

        for track in self.playlist:
            key = track["key"]
            lib.increment_play_count(key)
            track["play_count"] = lib.get_play_count(key)

        self.update_playlist_text()
        messagebox.showinfo("Playing Playlist", "All tracks in the playlist have been played and play counts incremented.")

    def search_tracks_clicked(self):
        query = self.search_txt.get()
        if not query.strip(): 
            self.status_lbl.configure(text="Please enter a search query.")
            return
        results = lib.search_library(query) 
        set_text(self.list_txt, results)
        self.status_lbl.configure(text="Search completed.")
        

    def display_image(self, image_path):  
        try:
            img = Image.open(image_path)  
            resize_img = img.resize((200, 150), Image.ANTIALIAS)  
            converted_img = ImageTk.PhotoImage(resize_img)
            self.image_lb.config(image=converted_img)
            self.image_lb.image = converted_img
        except Exception as e: 
            self.image_lb.config(image='', text=f"Error loading image: {e}")
            
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
    JukeBox(window)
    window.mainloop()