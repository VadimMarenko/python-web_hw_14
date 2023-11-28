from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    sqlalchemy_database_url: str
    secret_key: str
    algorithm: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    redis_host: str
    redis_port: int
    cloudinary_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str

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

#     class Config:
#         # env_file = ".env"
#         env_file_encoding = "utf-8"
#         # extra = "allow"


settings = Settings()
