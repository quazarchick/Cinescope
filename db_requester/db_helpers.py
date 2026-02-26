from sqlalchemy.orm import Session
from db_models.user import UserDB
from db_models.movie import MoviesDB


class DBHelper:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        """Класс с методами для работы с БД в тестах"""

    def create_test_user(self, user_data: dict) -> UserDB:
        """Создаем тестового пользователя"""
        user = UserDB(**user_data)
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def get_user_by_id(self, user_id: str):
        """Получает пользователя по ID"""
        return self.db_session.query(UserDB).filter(UserDB.id == user_id).first()

    def get_user_by_email(self, email: str):
        """Получить пользователя по email"""
        return self.db_session.query(UserDB).filter(UserDB.email == email).first()

    def get_movie_by_name(self, name: str):
        """Получает фильм по названию"""
        return self.db_session.query(MoviesDB).filter(MoviesDB.name == name).first()

    def user_exists_by_email(self, email: str) -> bool:
        """Проверяет существование пользователя по email"""
        return self.db_session.query(UserDB).filter(UserDB.email == email).count() > 0

    def delete_user(self, user: UserDB):
        """Удаляет пользователя"""
        self.db_session.delete(user)
        self.db_session.commit()

    def cleanup_test_data(self, objects_to_delete: list):
        """Очищает тестовые данные"""
        for obj in objects_to_delete:
            if obj:
                self.db_session.delete(obj)
        self.db_session.commit()

    def get_movie_by_id(self, movie_id: str):
        """Получает фильм по ID"""
        return self.db_session.query(MoviesDB).filter(MoviesDB.id == movie_id).first()

    def create_test_movie(self, movie_data: dict) -> MoviesDB:
        movie = MoviesDB(**movie_data)
        self.db_session.add(movie)
        self.db_session.commit()
        self.db_session.refresh(movie)
        return movie


