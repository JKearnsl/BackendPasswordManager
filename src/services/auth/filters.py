from functools import wraps

from src.exceptions import AccessDenied
from src.models.enums.role import UserRole


def role_filter(*roles: UserRole):
    """
    Role Filter decorator for ApplicationServices
    It is necessary that the class of the method being decorated has a field '_current_user'

    :param roles: user role
    :return: decorator
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):

            service_class: object = args[0]
            current_user = service_class.__getattribute__('_current_user')
            if not current_user:
                raise ValueError('AuthMiddleware not found')

            if current_user.role in roles:
                return await func(*args, **kwargs)
            else:
                raise AccessDenied('User has no access')

        return wrapper

    return decorator
