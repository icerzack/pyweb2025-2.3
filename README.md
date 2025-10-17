# Glossary API (FastAPI)


- CRUD: список, получение по `keyword`, создание, обновление, удаление
- Валидация схем через Pydantic v2
- Документация: `/docs`, `/redoc`

## Запуск в Docker
```bash
docker compose up -d --build
```
- При старте выполняются миграции: `alembic upgrade head` (если структура уже есть — `alembic stamp head`).
- База: `./data/app.db` (пробрасывается как том).
- API: `http://localhost:8000`

## Примеры запросов
```bash
# список
curl http://localhost:8000/api/v1/terms
# создать
curl -X POST http://localhost:8000/api/v1/terms \
  -H 'Content-Type: application/json' \
  -d '{"keyword":"FastAPI","description":"Modern, fast web framework for Python."}'
# получить
curl http://localhost:8000/api/v1/terms/FastAPI
# обновить
curl -X PUT http://localhost:8000/api/v1/terms/FastAPI \
  -H 'Content-Type: application/json' \
  -d '{"description":"High-performance Python web framework for building APIs."}'
# удалить
curl -i -X DELETE http://localhost:8000/api/v1/terms/FastAPI
```

## Локальный запуск
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```