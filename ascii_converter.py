from PIL import Image

# ASCII characters from dark to light
ASCII_CHARS = "@%#*+=-:. "

def image_to_ascii(image_path, width=80):
    try:
        # Open image
        image = Image.open(image_path).convert('L')  # Convert to grayscale
        
        # Calculate height to maintain aspect ratio
        aspect_ratio = image.height / image.width
        height = int(aspect_ratio * width * 0.55)  # 0.55 adjusts for character spacing
        
        # Resize image
        image = image.resize((width, height))
        
        # Convert pixels to ASCII
        pixels = image.getdata()
        ascii_str = ""
        for pixel_value in pixels:
            ascii_str += ASCII_CHARS[pixel_value * len(ASCII_CHARS) // 256]
        
        # Format into lines
        ascii_img = ""
        for i in range(0, len(ascii_str), width):
            ascii_img += ascii_str[i:i+width] + "\n"
        
        return ascii_img
    except Exception as e:
        print(f"Error: {e}")
        return ""

if __name__ == "__main__":
    ascii_art = image_to_ascii("assets/profile.jpg", width=80)
    print("\nYour ASCII Art:\n")
    print(ascii_art)
    print("\nCopy this and paste it into generate_readme.py's ASCII_ART variable!")