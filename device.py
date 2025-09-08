import asyncio
import requests
import json
import base64
from urllib3.exceptions import InsecureRequestWarning
import logging
from requests.exceptions import SSLError, ConnectTimeout
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logger = logging.getLogger(__name__)

class Device:
    def __init__(self, id, device, ip, firmware, key, type, apdb, nids):
        self.id = id
        self.device = device
        self.ip = ip
        self.firmware = firmware
        self.key = key
        self.type = type
        self.apdb = apdb
        self.nids = nids
    
    def __str__(self):
        return f'{self.id} {self.device} {self.ip} {self.firmware} {self.key} {self.type} {self.apdb} {self.nids}'

    async def send_update(self, file_name, file_data, db_name, timeout=600):
        url = f"https://{self.ip}/api/v2/monitor/license/database/upgrade"
        http_url =f"http://{self.ip}/api/v2/monitor/license/database/upgrade"
        headers = {
                    "Accept": "*/*",
                    "Authorization": f"Bearer {self.key}",
                    "Content-Type": "application/json" 
                    }
        payload = {
                    "db_name": db_name,
                    "confirm_not_signed": False,
                    "confirm_not_ga_certified": False,
                    "filename": file_name,
                    "file_content": base64.b64encode(file_data).decode('ascii')
                    }
        
        try:
            response = await asyncio.wait_for(
                asyncio.to_thread(
                requests.post, 
                url, 
                data=json.dumps(payload),
                headers=headers,
                verify=False
            ),
            timeout=timeout
        )
            print(response)
            if response.status_code == 200:
                logger.info(f"Устройство {self.device} ({self.ip}) {db_name}: обновление успешно!")
                self.updated = True
            else:
                logger.error(f"Ошибка обновления {db_name} на устройстве {self.device} ({self.ip}): "
                           f"Статус {response.status_code}, ответ: {response.text}")
        except ConnectTimeout as e :
            logger.info(f"Ошибка при обновлении по HTTPS устройства {self.device} ({self.ip}), пробую HTTP")
            await asyncio.sleep(2)
            response = await asyncio.wait_for(
                asyncio.to_thread(
                    requests.post, 
                    http_url, 
                    data=json.dumps(payload),
                    headers=headers,
                    verify=False
                ),
                timeout=timeout
            )
            if response.status_code == 200:
                logger.info(f"Устройство {self.device} ({self.ip}) {db_name}: обновление успешно по HTTP!")
                self.updated = True
            else:
                logger.error(f"Ошибка обновления {db_name} по HTTP на устройстве {self.device} ({self.ip}): "
                                f"Статус {response.status_code}, ответ: {response.text}")
  
        except Exception as e:
            logger.info(f"Исключение при обновлении {db_name} на устройстве {self.device} ({self.ip}): {str(e)}")