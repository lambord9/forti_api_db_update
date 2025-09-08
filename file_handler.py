import os
import logging
from config import UPDATES_PATH

logger = logging.getLogger(__name__)

def get_update_files(prefix: str) -> list[str]:
    """Получает список файлов обновлений с заданным префиксом"""
    try:
        files = [f for f in os.listdir(UPDATES_PATH) if f.startswith(prefix)]
        logger.info(f"Найдено {len(files)} файлов с префиксом {prefix}")
        return files
    except Exception as e:
        logger.error(f"Ошибка при получении списка файлов: {str(e)}")
        return []
    
def read_update_files(filename: str) -> bytes:
    """Читает содержимое файла обновления"""
    try:
        with open(os.path.join(UPDATES_PATH, filename), 'rb') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Ошибка при чтении файла {filename}: {str(e)}")
        raise
    