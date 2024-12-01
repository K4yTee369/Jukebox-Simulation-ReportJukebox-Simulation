import csv
from library_item import LibraryItem

CSV_FILE = 'track_library.csv'

library = {}

def load_library():
    global library
    library = {}
    try:
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')  # Use ';' as the delimiter
            next(reader)  
            for row in reader:
                key, name, artist, rating, play_count = row
                item = LibraryItem(name, artist, int(rating), int(play_count))
                library[key] = item
    except FileNotFoundError:
        pass

def save_library():
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')  # Use ';' as the delimiter
        writer.writerow(['Key', 'Name', 'Artist', 'Rating', 'Play Count'])  # Write header row
        for key, item in library.items():
            writer.writerow([key, item.name, item.artist, item.rating, item.play_count])

load_library()


def list_all():
    output = ""
    for key in library:
        item = library[key]
        output += f"{key} {item.info()}\n"
    return output

def get_name(key):
    try:
        item = library[key]
        return item.name
    except KeyError:
        return None

def get_artist(key):
    try:
        item = library[key]
        return item.artist
    except KeyError:
        return None

def get_rating(key):
    try:
        item = library[key]
        return item.rating
    except KeyError:
        return -1

def set_rating(key, rating):
    try:
        item = library[key]
        item.rating = rating
        save_library()  
    except KeyError:
        return

def get_play_count(key):
    try:
        item = library[key]
        return item.play_count
    except KeyError:
        return -1

def increment_play_count(key):
    try:
        item = library[key]
        item.play_count += 1
        save_library()  
    except KeyError:
        return

def add_track(key, name, artist, rating=0, play_count=0):
    if key not in library:
        item = LibraryItem(name, artist, rating)
        item.play_count = play_count
        library[key] = item
        save_library() 
    else:
        raise ValueError("Track with this key already exists.")
    
def search_library(query):
    """Search for tracks or artists by name."""
    query = query.lower()
    results = []
    for key, item in library.items():
        if query in item.name.lower() or query in item.artist.lower():
            results.append(f"{key} {item.info()}")
    return "\n".join(results) if results else "No matches found."


