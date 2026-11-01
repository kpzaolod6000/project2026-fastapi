## mypy

### install
```
pip install mypy
```

### testing
```
mypy .
```

## FASTAPI
```
source bin/activate
```
```
pip install "fastapi[standard]"
```

Modo desarrollo
```
fastapi dev main.py
```

Con uvicorn
```
uvicorn main:app --reload --port 9000
```