import cv2
import numpy as np
import random
import base64
import re
import sys

class AbstractSpectreDrawer:
    hex_colors = "" 
    def __init__(self, random_func=random.randint, canvas_size=10,hexcolors=""):
        self.random_func = random_func
        self.canvas_size = canvas_size
        self.hex_colors = hexcolors
    def get_random_color(self):
        color = [self.random_func(0, 255) for _ in range(3)]
        return color
    def draw_abstract_spectre(self, text):
        num_characters = len(text)
        points_per_char = [int(np.ceil(ord(char) / 200) * 10) for char in text]
        canvas = np.zeros((self.canvas_size, self.canvas_size, 4), dtype=np.uint8) 
        for i in range(num_characters):
            num_points = points_per_char[i]
            color = self.get_random_color()
            for j in range(num_points):
                x = self.random_func(0, self.canvas_size - 1)
                y = self.random_func(0, self.canvas_size - 1)
                if color == [0, 0, 0]: 
                    canvas[y, x] = [0, 0, 0, 0]  
                else:
                    canvas[y, x] = [*color, 255] 
        blurred_canvas = cv2.GaussianBlur(canvas, (5, 5), 0) 
        return blurred_canvas
    def draw_and_get_base64(self, text):
        if re.match("^[a-zA-Z0-9]+$", text):        
            canvas_image = self.draw_abstract_spectre(text.join([str(random.randint(0, 9)) for _ in range(10)]))
            _, buffer = cv2.imencode('.png', canvas_image)
            base64_image = base64.b64encode(buffer).decode()
            return base64_image
        else:
            return ""
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python draw_spectre.py <text>")
    else:
        text = sys.argv[1]
        drawer = AbstractSpectreDrawer()
        base64_image = drawer.draw_and_get_base64(text)
        print(base64_image)
