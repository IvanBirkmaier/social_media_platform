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


def resize_image(image_bytes: bytes, target_width: int = 640, target_height: int = 480) -> bytes:
    """
    Verkleinert ein Bild auf die Zielgröße. Unterstützt JPEG- und PNG-Formate.

    :param image_bytes: Die Bytes des ursprünglichen Bildes.
    :param target_width: Die Zielbreite des Bildes.
    :param target_height: Die Zielhöhe des Bildes.
    :return: Die Bytes des verkleinerten Bildes.
    """
    with Image.open(io.BytesIO(image_bytes)) as img:
        # Bild an die Zielgröße anpassen
        img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
        # Bild in Bytes konvertieren, dabei das ursprüngliche Format beibehalten
        img_byte_arr = io.BytesIO()
        img_format = img.format if img.format in ['JPEG', 'PNG'] else 'JPEG'
        img.save(img_byte_arr, format=img_format)
        print("Bild erfolgreich verkleinert und gespeichert")
        return img_byte_arr.getvalue()