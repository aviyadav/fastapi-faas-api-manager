# FastAPI FAAS API Manager



```
uv add fastapi sqlalchemy psycopg2-binary pydantic uvicorn
```

```
uv run uvicorn main:app --port 8090
```

```
payload:

{
    "path": "/greet2",
    "method": "GET",
    "code": "def handler():\n    greeting = 'Wow! I invented Lambdas XDDD!'\n    return {\"greeting\": greeting}"
}
```
