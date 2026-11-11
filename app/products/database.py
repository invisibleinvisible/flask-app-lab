
from pathlib import Path
from tinydb import TinyDB

# Коренева папка проєкту
BASE_DIR = Path(__file__).resolve().parents[2]

# Папка для зберігання даних
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Шлях до JSON-файлу
DATABASE_PATH = DATA_DIR / "products.json"

# Ініціалізація TinyDB
db = TinyDB(str(DATABASE_PATH))

# Таблиця товарів
products_table = db.table("products")
