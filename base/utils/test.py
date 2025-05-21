from fastapi import FastAPI

app = FastAPI(
    title="My Custom API",
    description="This is a custom Swagger UI for my API.",
    version="1.0.0"
)


@app.get("/")
def read_root():
    return {"message": "Welcome to My Custom API"}
