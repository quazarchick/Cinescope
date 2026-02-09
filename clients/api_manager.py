from clients.auth_api import AuthAPI
from clients.user_api import UserAPI

class ApiManager:
    """
    Класс для управления API-классами с единой HTTP-сессией.
    """
    def __init__(self, session):
        """
        Инициализация ApiManager.
        :param session: HTTP-сессия, используемая всеми API-классами.
        """
        self.session = session
        self.auth_api = AuthAPI(session)
        self.user_api = UserAPI(session)

'''- **Конструктор `ApiManager`**:
    - Принимает объект `session` (HTTP-сессия).
    - Создает экземпляры **AuthAPI** и **UserAPI**, передавая им единую сессию.
    - Иными словами Конструктор принимает **session** - объект сессии, который будет передаваться в каждый API класс.'''