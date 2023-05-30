add-migrations:
	 alembic revision --autogenerate

migrate:
	alembic upgrade head

start:
	uvicorn app.main:app --reload
