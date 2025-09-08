import questionary
import logging
from typing import Dict

logger = logging.getLogger(__name__)

async def get_user_selection() -> tuple[str, str]:
    """Получает выбор пользователя для типа устройств и версии"""
    try:
        device_type = await questionary.select(
            "What device type you want to update?",
            choices=["all", "critical", "non-critical"]
        ).ask_async()
        if device_type is None:
                logger.error("Выбор типа устройства не сделан (None)")
                raise ValueError("Тип устройства не выбран")
        logger.info(f"Выбран тип устройства: {device_type}")

        firmware_version = await questionary.select(
            "What version of device software do you want to update?",
            choices=["all", "6.4", "7.0"]
        ).ask_async()
        if firmware_version is None:
                logger.error("Выбор версии прошивки не сделан (None)")
                raise ValueError("Версия прошивки не выбрана")
        logger.info(f"Выбрана версия прошивки: {firmware_version}")

        return device_type, firmware_version
    except Exception as e:
        logger.error(f"Ошибка при получении выбора пользователя: {str(e)}")
        raise

async def select_update_files(nids_files: list[str], apdb_files: list[str],
                        firmware_version: str) -> Dict[str, str]:
    """Позволяет пользователю выбрать файлы обновлений"""
    update_files = {}

    try:
        if not firmware_version or firmware_version == "None":
            logger.error("Некорректная версия прошивки: None")
            raise ValueError("Версия прошивки не указана")
        
        def filter_and_sort_files(files: list[str], prefix: str, version, str = None) -> list[str]:
            if version:
                filtered = [f for f in files if f.startswith(f"{prefix}_OS{version}")]
            else:
                filtered = [f for f in files if f.startswith(f"{prefix}")]
            return sorted(filtered, reverse=True)
        
        if firmware_version == "all":
            nids_files_6_4 = filter_and_sort_files(nids_files, "nids", "6.4")
            update_files["nids_OS6.4"] = await questionary.select(
                "Select IPS file for 6.4:",
                choices=nids_files_6_4
            ).ask_async()

            nids_files_7_0 = filter_and_sort_files(nids_files, "nids", "7.0")
            update_files["nids_OS7.0"] = await questionary.select(
                "Select IPS file for 7.0:",
                choices=nids_files_7_0
            ).ask_async()

            apdb_files_6_4 = filter_and_sort_files(apdb_files, "apdb", "6.4")
            update_files["apdb_OS6.4"] = await questionary.select(
                "Select APPCTRL file for 6.4:",
                choices=apdb_files_6_4
            ).ask_async()
            
            apdb_files_7_0 = filter_and_sort_files(apdb_files, "apdb", "7.0")
            update_files["apdb_OS7.0"] = await questionary.select(
                "Select APPCTRL file for 7.0:",
                choices=apdb_files_7_0
            ).ask_async()
        else:
            version = firmware_version
            nids_files_version = filter_and_sort_files(nids_files, "nids", version)
            update_files[f"nids_OS{version}"] = await questionary.select(
                f"Select IPS file for {version}:",
                choices=nids_files_version
            ).ask_async()
            
            apdb_files_version = filter_and_sort_files(apdb_files, "apdb", version)
            update_files[f"apdb_OS{version}"] = await questionary.select(
                f"Select APPCTRL file for {version}:",
                choices=apdb_files_version
            ).ask_async()

        logger.info(f"Выбраны файлы обновлений: {update_files}")
        return update_files
    except Exception as e:
        logger.error(f"Ошибка при выборе файлов обновлений: {str(e)}")
        raise
