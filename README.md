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

## Документация API
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

Сборка статической HTML-документации (через Docker):
```bash
curl -s http://localhost:8000/openapi.json > openapi.json
docker run --rm -v $(pwd):/work -w /work redocly/cli:latest \
  build-docs openapi.json -o docs.html
```
Файл `docs.html` можно открыть локально или отдавать как статический.

## Локальный запуск
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## gRPC сервис

Сервис gRPC реализует те же CRUD-операции для терминов и использует ту же БД.

### Запуск в Docker
```bash
docker compose up -d --build grpc
docker compose logs --tail=200 grpc
```
Сервис слушает на `localhost:50051`.

### Быстрые проверки через клиент внутри контейнера
```bash
# создать
docker compose exec -T grpc python grpc_service/client_example.py create http "Hypertext Transfer Protocol"

# список
docker compose exec -T grpc python grpc_service/client_example.py list

# получить
docker compose exec -T grpc python grpc_service/client_example.py get http

# обновить
docker compose exec -T grpc python grpc_service/client_example.py update http "HTTP is an application-layer protocol"

# удалить
docker compose exec -T grpc python grpc_service/client_example.py delete http
```

### Локальный запуск gRPC
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# применить миграции
PYTHONPATH=./ alembic upgrade head || PYTHONPATH=./ alembic stamp head

# сгенерировать protobuf stubs
python grpc_service/compile_protos.py

# запустить сервер
export DATABASE_URL=sqlite:///./data/app.db
export GRPC_HOST=0.0.0.0
export GRPC_PORT=50051
python grpc_service/server.py
```

### Примеры с grpcurl (опционально)
```bash
# список сервисов
grpcurl -plaintext localhost:50051 list

# методы TermsService
grpcurl -plaintext localhost:50051 list glossary.v1.TermsService

# создать
grpcurl -plaintext -d '{"keyword":"dns","description":"Domain Name System"}' \
  localhost:50051 glossary.v1.TermsService.CreateTerm

# список
grpcurl -plaintext localhost:50051 glossary.v1.TermsService.ListTerms

# получить
grpcurl -plaintext -d '{"keyword":"dns"}' \
  localhost:50051 glossary.v1.TermsService.GetTerm

# обновить
grpcurl -plaintext -d '{"keyword":"dns","description":"DNS resolves names to IPs"}' \
  localhost:50051 glossary.v1.TermsService.UpdateTerm

# удалить
grpcurl -plaintext -d '{"keyword":"dns"}' \
  localhost:50051 glossary.v1.TermsService.DeleteTerm
```

Примечания:
- gRPC и REST используют одну и ту же БД `./data/app.db`.
- В Docker-compose для gRPC автоматически выполняются миграции и генерация protobuf.