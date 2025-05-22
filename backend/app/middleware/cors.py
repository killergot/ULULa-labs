from fastapi.middleware.cors import CORSMiddleware

def get_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://127.0.0.1:5173",
            "http://localhost:5173",# Только ваш фронтенд
            "http://localhost",
            "https://localhost",
            "https://127.0.0.1:5173",
            "http://127.0.0.1:5173"

        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE","PATCH"],  # Ограничить по необходимости
        allow_headers=["Authorization",
                       "Content-Type",
                       "accept"],  # Только нужные
    )