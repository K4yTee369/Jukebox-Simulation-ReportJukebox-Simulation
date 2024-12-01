import tkinter as tk
from tkinter import messagebox
import tkinter.scrolledtext as tkst
from PIL import ImageTk, Image

import track_library as lib
from image import Image4Song


def set_text(text_area, content):
    text_area.delete("1.0", tk.END)
    text_area.insert(1.0, content)


class CreateTrack():
    def __init__(self, window):
        window.geometry("1000x600")
        window.title("Create Track List")

        self.playlist = []
        self.img_song = Image4Song()  # Initialize the Image4Song instance

        add_tracks_btn = tk.Button(window, text="Add Tracks", command=self.add_track)
        add_tracks_btn.grid(row=0, column=0, padx=10, pady=10)

        self.input_txt = tk.Entry(window, width=3)
        self.input_txt.grid(row=0, column=1, padx=10, pady=10)

        self.track_txt = tk.Text(window, width=48, height=8, wrap="none")
        self.track_txt.grid(row=0, column=2, sticky="NW", padx=10, pady=10)

        play_tracks_btn = tk.Button(window, text="Play Tracks", command=self.play_playlist)
        play_tracks_btn.grid(row=1, column=0, padx=10, pady=10)

        clear_tracks_btn = tk.Button(window, text="Clear All Tracks", command=self.reset_playlist)
        clear_tracks_btn.grid(row=2, column=0, padx=10, pady=10)

        self.list_txt = tkst.ScrolledText(window, width=48, height=12, wrap="none")
        self.list_txt.grid(row=2, column=2, columnspan=3, sticky="W", padx=10, pady=10)

        self.image_lb = tk.Label(window)
        self.image_lb.grid(row=2, column=3, padx=10, pady=10)

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

    def display_all_tracks(self):
        all_tracks = lib.list_all()
        set_text(self.list_txt, all_tracks)

    def display_image(self, image_path):
        try:
            img = Image.open(image_path)
            resize_img = img.resize((200, 150), Image.ANTIALIAS)
            converted_img = ImageTk.PhotoImage(resize_img)
            self.image_lb.config(image=converted_img)
            self.image_lb.image = converted_img
        except Exception as e:
            self.image_lb.config(image='', text=f"Error loading image: {e}")


if __name__ == "__main__":
    window = tk.Tk()
    CreateTrack(window)
    window.mainloop()
