import gdown
import os

# Télécharger le modèle depuis Google Drive
if not os.path.exists('model/best.pt'):
    os.makedirs('model', exist_ok=True)
    url = 'https://drive.google.com/uc?id=1VZ0FYrnueUsG4MRoOW5JDsZ_MMrL8L-M'
    gdown.download(url, 'model/best.pt', quiet=False)
