from typing import Optional
from constants.roles import Roles
from pydantic import BaseModel, Field, field_validator
import datetime


class TestUser(BaseModel):
    email: str = Field(..., pattern="@", description="E-mail адрес")
    fullName: str
    password: str
    passwordRepeat: str = Field(
        ..., min_length=1, max_length=20, description="Пароли должны совпадать"
    )
    roles: list[Roles] = [Roles.USER]
    banned: Optional[bool] = None
    verified: Optional[bool] = None

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value


class RegisterUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    fullName: str
    verified: bool
    banned: Optional[bool] = None
    roles: list[Roles]
    createdAt: str
    password: Optional[str] = None

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени")
        return value


class MovieBase(BaseModel):
    name: str
    price: int = Field(..., ge=1, le=1000)
    description: str
    genreId: int = Field(..., ge=1, le=10)


class GenreResponse(BaseModel):
    name: str


class CreateMovieRequest(MovieBase):
    imageUrl: str
    location: str
    published: bool


class EditMovieRequest(BaseModel):
    name: Optional[str] = None
    price: int | None = Field(default=None, ge=1, le=1000)
    description: Optional[str] = None
    genreId: int | None = Field(default=None, ge=1, le=10)
    imageUrl: Optional[str] = None
    location: Optional[str] = None
    published: Optional[bool] = None


class CreateMovieResponse(MovieBase):
    id: int
    imageUrl: Optional[str] = None
    location: str
    published: bool
    genre: GenreResponse
    createdAt: datetime.datetime
    rating: int


class UserReviewResponse(BaseModel):
    fullName: str


class ReviewResponse(BaseModel):
    userId: str
    rating: int
    text: str
    createdAt: datetime.datetime
    user: UserReviewResponse


class GetMovieResponse(CreateMovieResponse):
    reviews: list[ReviewResponse]


class GetMoviesResponse(BaseModel):
    movies: list[CreateMovieResponse]
    count: int
    page: int
    pageSize: int
    pageCount: int
