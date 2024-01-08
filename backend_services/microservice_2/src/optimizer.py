from PIL import Image
import io

def compress_image_bytes(image_bytes, format='JPEG', quality=85):
    # BytesIO-Objekt aus den Bild-Bytes erstellen
    image_stream = io.BytesIO(image_bytes)
    
    # Bild aus BytesIO-Objekt laden
    with Image.open(image_stream) as img:
        # Konvertieren des Bildes in RGB, falls es RGBA oder P ist
        if img.mode in ["RGBA", "P"]:
            img = img.convert("RGB")

        # BytesIO-Objekt für das komprimierte Bild erstellen
        output_stream = io.BytesIO()
        
        # Bild komprimieren und im BytesIO-Objekt speichern
        img.save(output_stream, format=format, quality=quality)

        # Komprimierte Bildbytes zurückgeben
        return output_stream.getvalue()
