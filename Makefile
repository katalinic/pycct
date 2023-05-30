check:
	black src examples tests
	ruff src examples tests --fix
	mypy src --strict

test:
	pytest tests/ examples/ --durations 5