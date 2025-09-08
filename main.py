import asyncio
from typing import List, Dict
from db_handler import fetch_devices_by_type_and_version
from device import Device
import logging
from file_handler import get_update_files, read_update_files
from ui import get_user_selection, select_update_files
# import warnings
# warnings.filterwarnings("ignore")

logging.basicConfig(
    filename='update.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def get_devices(device_type: str, firmware_version: str) -> List[Device]:
    """Получает список устройств из БД и создает объекты Device"""
    try:
        devices_data = await fetch_devices_by_type_and_version(device_type, firmware_version)
        logger.info(f"Получено {len(devices_data)} устройств из БД")
        return [Device(**device) for device in devices_data]
    except Exception as e:
        logger.error(f"Ошибка при получении устройств из БД: {str(e)}")
        raise
async def update_device(device: Device, files: dict[str, str], db_type: str):
    """Обновляет одно устройство"""
    firmware = "6.4" if "6.4" in device.firmware else "7.0"
    file_name = f"{db_type}_OS{firmware}"

    db_name_map = {
        "nids": "ips",
        "apdb": "appctrl"
    }
    db_name = db_name_map.get(db_type, db_type)

    if file_name in files:
        file_data = read_update_files(files[file_name])
        logger.info(f"Начинается обновление {db_type} на устройстве {device.device} ({device.ip})")
        await device.send_update(files[file_name], file_data, db_name)

async def main():
    logger.info("Запуск скрипта обновления")
    try:
        """Получение выбора пользователя"""
        type, firmware_version = await get_user_selection()
        type_filter = "%" if type == "all" else type
        version_filter = "%" if firmware_version == "all" else firmware_version

        """Получение и выбор файлов обновлений"""
        nids_files = get_update_files("nids_OS")
        apdb_files = get_update_files("apdb_OS")
        update_files = await select_update_files(nids_files, apdb_files, firmware_version)

        """Получение устройств и обновление"""
        devices = await get_devices(type_filter, version_filter)
        logger.info(f"Найдено устройств для обновления: {len(devices)}")

        tasks = []
        for device in devices:
            if any(key.startswith("nids") for key in update_files):
                tasks.append(update_device(device, update_files, "nids"))
            if any(key.startswith("apdb") for key in update_files):
                tasks.append(update_device(device, update_files, "apdb"))

        if not tasks:
            logger.warning("Не найдено задач для обновления устройств")
        
        await asyncio.gather(*tasks)
        logger.info("Обновление всех устройств завершено")
    
    except Exception as e:
        logger.error(f"Ошибка при выполнении скрипта: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())