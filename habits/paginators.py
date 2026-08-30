from rest_framework.pagination import PageNumberPagination


class HabitPaginator(PageNumberPagination):
    """Пагинатор для привычек"""
    page_size = 5  # Количество привычек на странице
    page_size_query_param = 'page_size'  # Параметр для изменения размера страницы
    max_page_size = 20  # Максимальное количество привычек на странице