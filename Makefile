.PHONY: run
run:
	python src/manage.py runserver


.PHONY: check
check:
	python -m ruff . && python -m black --check . && python -m isort --check .

.PHONY: fix
fix:
	python -m ruff --fix . && python -m black . && python -m isort .

.PHONY: worker
worker:
	celery -A config worker -l INFO
