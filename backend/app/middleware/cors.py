from fastapi.middleware.cors import CORSMiddleware

def get_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            'http://185.95.159.198/',
            'https://185.95.159.198/'
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE","PATCH"],  # Ограничить по необходимости
        allow_headers=["Authorization",
                       "Content-Type",
                       "accept"],  # Только нужные
    )