from fastapi.middleware.cors import CORSMiddleware

def get_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Разрешить все домены
        allow_credentials=True,
        allow_methods=["*"],  # Разрешить все методы
        allow_headers=["*"],  # Разрешить все заголовки
    )