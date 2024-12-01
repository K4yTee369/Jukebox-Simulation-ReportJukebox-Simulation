import tkinter as tk
import font_manager as fonts


from view_tracks import TrackViewer

from create_tracks_list import CreateTrack

from update_tracks import UpdateTrack


def view_tracks_clicked():
    status_lbl.configure(text="View Tracks button was clicked!")
    TrackViewer(tk.Toplevel(window))

def create_tracks_clicked():
    status_lbl.configure(text="Create Tracks button was clicked!")
    CreateTrack(tk.Toplevel(window))
    
def update_tracks_clicked():
    status_lbl.configure(text="Update Tracks button was clicked!")
    UpdateTrack(tk.Toplevel(window))



window = tk.Tk() #Creates the main application window using the Tkinter Tk class.
window.geometry("520x150") #Sets the dimensions of the main window to 520 pixels wide and 150 pixels high.
window.title("JukeBox") #Sets the title of the main window to "JukeBox".
window.configure(bg="gray") #Configures the background color of the main window to gray.

fonts.configure()

header_lbl = tk.Label(window, text="Select an option by clicking one of the buttons below")
header_lbl.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

view_tracks_btn = tk.Button(window, text="View Tracks", command=view_tracks_clicked)
view_tracks_btn.grid(row=1, column=0, padx=10, pady=10)

create_track_list_btn = tk.Button(window, text="Create Track List", command=create_tracks_clicked)
create_track_list_btn.grid(row=1, column=1, padx=10, pady=10)

update_tracks_btn = tk.Button(window, text="Update Tracks", command=update_tracks_clicked)
update_tracks_btn.grid(row=1, column=2, padx=10, pady=10)

status_lbl = tk.Label(window, bg='gray', text="", font=("Helvetica", 10))
status_lbl.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

window.mainloop()
