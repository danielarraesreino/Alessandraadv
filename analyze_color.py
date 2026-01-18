from collections import Counter
from PIL import Image
import sys

def get_dominant_color(image_path):
    try:
        img = Image.open(image_path)
        img = img.resize((150, 150))  # Resize for speed
        pixels = img.getdata()
        # Filter out whites and very dark colors to find the accent
        pixels = [p for p in pixels if not (p[0] > 240 and p[1] > 240 and p[2] > 240) and not (p[0] < 20 and p[1] < 20 and p[2] < 20)]
        counts = Counter(pixels)
        if not counts:
            return "No dominant color found (image might be all white/black)"
        
        most_common = counts.most_common(5)
        print(f"Top 5 colors in {image_path}:")
        for count in most_common:
            rgb = count[0]
            hex_color = '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
            print(f"RGB: {rgb} - Hex: {hex_color} - Count: {count[1]}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_dominant_color("Captura de tela de 2026-01-17 02-27-58.png")
