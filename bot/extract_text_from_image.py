from PIL import Image
import pytesseract

def extract_text_from_image():
    image = Image.open("bot/files/photo.png")
    
    text = pytesseract.image_to_string(image, lang='rus')
    
    return text