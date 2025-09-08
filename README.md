# Автоматизированное обновление баз ips appctrl для Fortigate по api.
<img width="480" height="153" alt="image" src="https://github.com/user-attachments/assets/06d383ac-69ed-47ac-ad12-49929c3d118b" />

Создать виртуальное окружение
```
python3 -m venv .venv
```
Установить зависимости 
```
pip3 install -r requirements.txt
```
В PostgreSQL создать БД **devices**, в ней создать таблицу  по следующей схеме
```
CREATE TABLE devices (
    id SERIAL PRIMARY KEY,
    device VARCHAR(255),
    ip VARCHAR(20),
    firmware VARCHAR(20),
    key VARCHAR(255),
    type VARCHAR(20),
    apdb VARCHAR(50),
    nids VARCHAR(50),
    device_type VARCHAR(20)
);
```
Заполнить соответствующими данными (пример):
<img width="1154" height="104" alt="image" src="https://github.com/user-attachments/assets/9f2aec5e-c845-4d75-b40f-7e446dce7171" />

В папку updates положить соответствующие файлы обновлений для баз ips и appctrl
Запуск с помощью 
```
python3 main.py
```
