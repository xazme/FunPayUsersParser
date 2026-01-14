# Зачем этот проект
Этот репозиторий создан как демонстрация:
- умения работать с `asyncio` и конкурентными задачами  
- использования `httpx.AsyncClient`  
- применения `selectolax` для быстрого HTML‑парсинга  
- структурирования данных через Pydantic  
- построения небольшого, но аккуратного асинхронного пайплайна 
# FunPay User Parser
Асинхронный парсер профилей пользователей FunPay, построенный на базе `httpx`, `asyncio` и сверхбыстрого HTML‑парсера `selectolax`.  
Проект демонстрирует подход к конкурентным HTTP‑запросам, ограничению параллелизма и извлечению структурированных данных из HTML.
# Возможности
- Асинхронные запросы к FunPay с использованием `httpx.AsyncClient`
- Ограничение параллелизма через `asyncio.Semaphore`
- Парсинг HTML с помощью `selectolax` (быстрее BeautifulSoup в разы)
- Извлечение ключевых данных профиля:
  - имя пользователя
  - статус поддержки (support)
  - статус блокировки (banned)
  - время последнего онлайна
- Структурирование результата через Pydantic‑модель `UserResponseDTO`
- Логирование процесса
# Установка
```bash
uv sync
```
# Принцип работы
Парсер отправляет конкурентные HTTP‑запросы к страницам вида:
```
https://funpay.com/users/<id>/
```
Количество одновременных запросов регулируется параметром `semaphores_count`, а задержка между запросами — `requests_delay`.
Каждый HTML‑ответ разбирается через `selectolax`, после чего данные приводятся к Pydantic‑модели.
# Пример использования
```python
import asyncio
from src import FunPayUserParser
from src.config import setup_logger

async def main():
    setup_logger()

    parser = FunPayUserParser(
        semaphores_count=2,
        requests_delay=0.9,
    )

    await parser.get_all_users_by_range(
        from_index=1,
        to_index=10,
        step=1,
    )

if __name__ == "__main__":
    asyncio.run(main())
```
# Основные параметры

| Параметр            | Тип     | Описание |
|--------------------|---------|----------|
| `semaphores_count` | `int`   | Максимальное число одновременных запросов |
| `requests_delay`   | `float` | Задержка между запросами (anti‑DDOS) |
| `from_index`       | `int`   | Начальный ID пользователя |
| `to_index`         | `int`   | Конечный ID пользователя |
| `step`             | `int`   | Шаг перебора ID |


# Структура ответа
Каждый пользователь представлен моделью:
```python
class UserResponseDTO(BaseModel):
    name: str | None
    last_online: str | None
    is_banned: bool
    is_support: bool
```