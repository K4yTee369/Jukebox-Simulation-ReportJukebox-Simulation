image_path = "image"

class Image4Song:
    def __init__(self):
        self.image_map = {
            "1": "Image4Song/song1.jpg",
            "2": "Image4Song/song2.jpg",
            "3": "Image4Song/song3.jpg",
            "4": "Image4Song/song4.jpg",
            "5": "Image4Song/song5.jpg"
        }

    def get_image_path(self, track_id):
        """Retrieve the image path for a given track ID."""
        return self.image_map.get(track_id, None)