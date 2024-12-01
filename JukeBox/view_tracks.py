import tkinter as tk # imports the tkinter library, which is used to create the GUI
import tkinter.scrolledtext as tkst # scrolledText is a widget that adds a scrollable text area


import track_library as lib #imports track_library, assumed to provide track-related functions as lib for easier reference.
import font_manager as fonts #imports font_manager, assumed to handle font settings as fonts for easier access.


def set_text(text_area, content): # inserts content into the text_area 
    text_area.delete("1.0", tk.END) # first the existing content is deleted
    text_area.insert(1.0, content) # then the new content is inserted


class TrackViewer:
    def __init__(self, window):
        window.geometry("750x400") #Sets the window dimensions to 750 pixels wide and 400 pixels tall.
        window.title("View Tracks") #Sets the title of the window to "View Tracks".

        # Creates a button labeled "List All Tracks". When clicked, it calls the list_tracks_clicked method.
        list_tracks_btn = tk.Button(window, text="List All Tracks", command=self.list_tracks_clicked)
        list_tracks_btn.grid(row=0, column=0, padx=10, pady=10)

        # Creates a label with the text "Search by Name/Artist".
        search_lbl = tk.Label(window, text="Search by Name/Artist")
        search_lbl.grid(row=0, column=1, padx=10, pady=10)

        self.search_txt = tk.Entry(window, width=20) #Creates a text entry field (Entry) with a width of 20 characters for entering search queries.
        self.search_txt.grid(row=0, column=2, padx=10, pady=10)

        #Creates a "Search" button that calls search_tracks_clicked when clicked.
        search_btn = tk.Button(window, text="Search", command=self.search_tracks_clicked)
        search_btn.grid(row=0, column=3, padx=10, pady=10)

        # Creates a scrollable text area with 60 character width, 12 lines height, and no word wrapping.
        self.list_txt = tkst.ScrolledText(window, width=60, height=12, wrap="none")
        self.list_txt.grid(row=1, column=0, columnspan=4, sticky="W", padx=10, pady=10)

        #Creates a label for displaying status messages, using the "Helvetica" font at size 10.
        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=2, column=0, columnspan=4, sticky="W", padx=10, pady=10)
        
        self.list_tracks_clicked()



    def view_tracks_clicked(self): #defines a method called view_tracks_clicked
        key = self.input_txt.get() #retrieves the text entered by the user in the input text box (self.input_txt)
        name = lib.get_name(key) #calls the get_name function from the track_library module
        #checks if a valid track name was returned
        if name is not None: #if name is None, it indicates that the track does not exist
            #Retrieves the artist, rating, and play count for the track.
            artist = lib.get_artist(key) 
            rating = lib.get_rating(key) 
            play_count = lib.get_play_count(key)
            track_details = f"{name}\n{artist}\nrating: {rating}\nplays: {play_count}" #creates a formatted string containing the track details, including the name, artist, rating, and play count, each on a new line.
            set_text(self.track_txt, track_details) #calls the set_text function to display the track details in the self.track_txt text area.
        else:
            set_text(self.track_txt, f"Track {key} not found") #inform the user that the specified track number was not found.
        self.status_lbl.configure(text="View Track button was clicked!") #updates the status label to indicate that the "View Track" button was clicked.

    def list_tracks_clicked(self): #defines the method list_tracks_clicked
        track_list = lib.list_all() #calls the list_all function from the track_library module to retrieve a list of all available tracks.
        set_text(self.list_txt, track_list) #calls the set_text function to display the list of tracks in the self.list_txt scrollable text area.
        self.status_lbl.configure(text="List Tracks button was clicked!") #updates the status label to indicate that the "List Tracks" button was clicked.
        
    def search_tracks_clicked(self):
        query = self.search_txt.get() #Gets the search query from the input field.
        #Displays an error if the query is empty.
        if not query.strip(): 
            self.status_lbl.configure(text="Please enter a search query.")
            return
        results = lib.search_library(query) #Searches the library for tracks matching the query.
        #Displays the search results and updates the status label.
        set_text(self.list_txt, results)
        self.status_lbl.configure(text="Search completed.")

if __name__ == "__main__":  # only runs when this file is run as a standalone
    window = tk.Tk()        # create a TK object
    fonts.configure()       # configure the fonts
    TrackViewer(window)     # open the TrackViewer GUI
    window.mainloop()       # run the window main loop, reacting to button presses, etc
