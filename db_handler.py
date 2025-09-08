import asyncpg
from config import DATABASE_URL

async def fetch_devices_by_type_and_version(type: str, firmware_version: str):
    """
    Получает устройства из базы данных по типу и версии прошивки.
    :param: device_type: Тип устройства ('critical' или 'non-critical').
    :param: firmware_version: Версия прошивки ('6.4' или '7.0').
    :return: Список устройств в виде словарей.
    """
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        query = """
            SELECT id, device, ip, firmware, key, apdb, nids, type
            FROM devices
            WHERE type LIKE $1 AND firmware LIKE $2
        """
        rows = await conn.fetch(query, type, firmware_version)
        return [dict(row) for row in rows]
    finally:
        await conn.close()

