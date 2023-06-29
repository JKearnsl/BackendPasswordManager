## Backend менеджера паролей

### Описание

Backend менеджера паролей, реализованный на `Python 3.11` с использованием FastAPI является практическим заданием 
компании [НИИ "Спецвузавтоматика"](https://niisva.dev/).

Клиентская часть приложения [DesktopPasswordManager](https://github.com/JKearnsl/DesktopPasswordManager).


### Запуск [Локально]

1. Скачайте и установите [Python 3.11](https://www.python.org/downloads/).
2. Клонируйте репозиторий и перейдите в корневую директорию проекта
3. Создайте виртуальное окружение
```bash
python -m venv venv
source venv/bin/activate
```
4. Установите зависимости
```bash
pip install -r requirements.txt
```
5. Создайте конфигурационный файл `config.ini` на основе `config.ini.example`
6. Запустите веб-сервер `uvicorn`:
```bash
uvicorn src.app:app --proxy-headers --host 0.0.0.0 --port 8000
```

### Запуск [DockerFile]

```bash
docker build -t password-manager-backend .
docker run -d --name password-manager-backend -p 8000:80 password-manager-backend
```

### Запуск [DockerCompose]

```bash
docker-compose build
docker-compose up -d
```

### Использование Redis

По-умолчанию, приложение использует хранилище для хранения пользовательских сессий, настройка которого находится в 
конфигурационном файле:

https://github.com/JKearnsl/BackendPasswordManager/blob/418c7e59ccb561c8b5771c99e17095114bfc8dd5/config.ini.example#L17-L22

Если поле `is_used` по отношению к `redis` установлено в `0`, то приложение будет хранить данные в оперативной памяти, 
из-за чего после перезапуска приложения все пользовательские сессии будут аннулированы.

Если поле `is_used` по отношению к `redis` установлено в `1`, то приложение будет использовать предоставленные данные 
для подключения к `redis`.

### РСУБД

По-умолчанию, приложение использует `sqlite` базу данных, однако при необходимости можно использовать любую другую 
реляционную СУБД, поддерживаемую `SQLAlchemy`.

### JWT

По-умолчанию, приложение использует `HS256` алгоритм для подписи `JWT` токенов. Ключи подписи хранятся 
в конфигурационном файле:

https://github.com/JKearnsl/BackendPasswordManager/blob/418c7e59ccb561c8b5771c99e17095114bfc8dd5/config.ini.example#L13-L15

### DEBUG MODE

По-умолчанию, приложение запускается в режиме `DEBUG TRUE` - это означает, что:
- Корневой путь является `/`, документация доступна по `/api/docs` и `/api/redoc`
- 500 ошибки возвращают полный стек трейса 

При `DEBUG FALSE`:
- Корневой путь является `/api/v1`, документация доступна по `/docs` и `/redoc` соответственно, относительно корневого пути
- 500 ошибки возвращают только сообщение об ошибке

Сменить режим можно, установив переменную среды `DEBUG` в `0` или `1` соответственно.

