from django.db import models


class AnalyticGraph(models.Model):
    """
        Модель для зберігання інформації про графіки аналітики.

        Атрибути:
            name: Унікальна назва графіка
            image_path: Шлях до зображення графіка
            created_at: Дата та час створення графіка
    """
    name = models.CharField(max_length=100, unique=True)
    image_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
            Повертає рядкове представлення об'єкта графіка.

            Returns:
                str: Назва графіка
        """
        return str(self.name)

    @property
    def templates_name(self):
        """
            Форматує назву графіка для відображення в шаблонах.

            Замінює підкреслення на пробіли та робить кожне слово з великої літери.

            Returns:
                str: Відформатована назва графіка
        """
        return " ".join(self.name.split("_")).title()

    @property
    def image_url(self):
        """
            Формує повний URL-шлях до зображення графіка.

            Returns:
                str: URL-адреса зображення графіка
        """
        from django.conf import settings

        return f"{settings.MEDIA_URL}{self.image_path}"
