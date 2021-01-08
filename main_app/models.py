from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from pytils.translit import slugify
from time import time


def gen_slug(slug):
    new_slug = slugify(slug)
    return new_slug


class Vacancy(models.Model):

    title = models.CharField('Название вакансии', max_length=100)
    slug = models.SlugField(max_length=100)
    specialty = models.ForeignKey(
        'Specialty', related_name='vacancies', verbose_name='Специализация', on_delete=models.CASCADE
    )
    company = models.ForeignKey(
        'Company', related_name='vacancies', verbose_name='Компания', on_delete=models.CASCADE
    )
    skills = models.CharField('Навыки', max_length=100)
    description = models.TextField('Текст')
    salary_min = models.PositiveIntegerField('Зарплата от')
    salary_max = models.PositiveIntegerField('Зарплата до')
    published_at = models.DateField('Опубликовано', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("detail_vacancy_url", kwargs={'slug': self.slug})


class Specialty(models.Model):
    SPECIALTY_CHOICES = [
        (None, 'Выбор специальности'),
        ('frontend', 'Фронтенд'),
        ('backend', 'Бэкенд'),
        ('gamedev', 'Геймдев'),
        ('devops', 'Девопс'),
        ('design', 'Дизайн'),
        ('products', 'Продукты'),
        ('management', 'Менеджмент'),
        ('testing', 'Тестирование'),
    ]

    CODE_CHOICES = [
        (None, 'Выбор кода специальности'),
        ('frontend', 'frontend'),
        ('backend', 'backend'),
        ('gamedev', 'gamedev'),
        ('devops', 'devops'),
        ('design', 'design'),
        ('products', 'products'),
        ('management', 'management'),
        ('testing', 'testing'),
    ]

    code = models.CharField('Код', max_length=100, choices=CODE_CHOICES)
    title = models.CharField('Название специальности', max_length=100, choices=SPECIALTY_CHOICES)
    pictures = models.ImageField('Картинка', upload_to='specialty/')

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'

    def __str__(self):
        return self.code


class Company(models.Model):
    title = models.CharField('Название компании', max_length=100)
    slug = models.SlugField(max_length=100)
    location = models.CharField('Город', max_length=100)
    logo = models.ImageField('Логотип', upload_to='company_logo/', blank=True)
    description = models.TextField('Текст')
    employee_count = models.PositiveSmallIntegerField('Количество сотрудников')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("detail_company_url", kwargs={'slug': self.slug})


class Resume(models.Model):
    READY_TO_WORK_CHOICES = [
        ('NOT', 'Не ищу работу'),
        ('OPEN', 'Открыт к предложениям'),
        ('LOOK', 'Ищу работу'),
    ]
    GRADE_CHOICES = [
        ('IN', 'Стажер (intern)'),
        ('JR', 'Младший (junior)'),
        ('ML', 'Средний (middle)'),
        ('SR', 'Старший (senior)'),
        ('LD', 'Ведущий (Lead)'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField('Имя', max_length=100)
    slug = models.SlugField(max_length=100)
    surname = models.CharField('Фамилия', max_length=100)
    status = models.CharField('Готовность к работе', max_length=100, choices=READY_TO_WORK_CHOICES, default='NOT')
    grade = models.CharField('Квалификация', max_length=100, choices=GRADE_CHOICES, default='IN')
    salary = models.PositiveIntegerField('Вознаграждение')
    specialty = models.ForeignKey(Specialty, on_delete=models.DO_NOTHING, verbose_name='Специализация', default='frontend')
    education = models.TextField('Образование')
    experience = models.TextField('Опыт работы')
    portfolio = models.CharField('Ссылка на портфолио', max_length=250, blank=True)

    class Meta:
        verbose_name = 'Портфолио'
        verbose_name_plural = 'Портфолио'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(time()).split('.')[0] + str(time()).split('.')[1] + str(self.user.id)
        super().save(*args, **kwargs)


class Application(models.Model):
    username = models.CharField('Имя', max_length=150)
    phone = models.PositiveBigIntegerField('Номер телефона')
    letter = models.TextField('Сопроводительное письмо')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'

    def __str__(self):
        return self.username
