from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    sqlalchemy_database_url: str = (
        "postgresql+psycopg2://user:password@$localhost:5432/postgres"
    )
    secret_key: str = "secret"
    algorithm: str = "HS256"
    mail_username: str = "username"
    mail_password: str = "password"
    mail_from: str = "username@example.com"
    mail_port: int = 465
    mail_server: str = "smtp.example.com"
    redis_host: str = "localhost"
    redis_port: int = 6379
    cloudinary_name: str = "cloudinary_name"
    cloudinary_api_key: int = 21345195871934
    cloudinary_api_secret: str = "api_secret"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


# class Settings(BaseSettings):
#     sqlalchemy_database_url: str = Field(
#         "postgresql+psycopg2://user:password@$localhost:5432/postgres",
#         env="SQLALCHEMY_DATABASE_URL",
#     )
#     secret_key: str = Field("secret", env="SECRET_KEY")
#     algorithm: str = Field("HS256", env="ALGORITHM")
#     mail_username: str = Field("username", env="MAIL_USERNAME")
#     mail_password: str = Field("password", env="MAIL_PASSWORD")
#     mail_from: str = Field("username@example.com", env="MAIL_FROM")
#     mail_port: int = Field(465, env="MAIL_PORT")
#     mail_server: str = Field("smtp.example.com", env="MAIL_SERVER")
#     redis_host: str = Field("localhost", env="REDIS_HOST")
#     redis_port: int = Field(6379, env="REDIS_PORT")
#     cloudinary_name: str = Field("cloudinary_name", env="CLOUDINARY_NAME")
#     cloudinary_api_key: int = Field(21345195871934, env="CLOUDINARY_API_KEY")
#     cloudinary_api_secret: str = Field("api_secret", env="CLOUDINARY_API_SECRET")

#     class Config:
#         env_file = ".env"
#         env_file_encoding = "utf-8"


settings = Settings()
