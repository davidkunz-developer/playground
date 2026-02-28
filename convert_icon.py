from PIL import Image
import os

source_path = r"c:\Users\Dkunz\Documents\Projekty\playground\ia_icon.png"
target_path = r"c:\Users\Dkunz\Documents\Projekty\playground\icon.ico"

try:
    img = Image.open(source_path).convert("RGBA")
    # Standard icon sizes
    icon_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save(target_path, format='ICO', sizes=icon_sizes)
    print(f"Ikonka byla úspěšně vytvořena s průhledností: {target_path}")
except Exception as e:
    print(f"Chyba při tvorbě ikonky: {e}")
