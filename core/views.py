
from django.shortcuts import render

# Create your views here.

# Импорт настроек.
from django.conf import settings
# Импорт моделей вью.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# Импорт моделей ядра.
from .models import Organization, Subdivision, Position, Employee, Placement, \
    EmployeeExcelImport, Category, EmployeesGroup, EmployeesGroupObjectPermission, GroupsGenerator
# Импорт модели фильтров.
from .filters import CategoryFilter, EmployeeExcelImportFilter, \
    OrganizationFilter, SubdivisionFilter, PositionFilter, GroupFilter, EmployeeFilter, GroupsEmployeeFilter
# Импорт форм.
from .forms import CategoryForm, EmployeeExcelImportForm, GroupForm, GroupsGeneratorForm, \
    EmployeesGroupObjectPermissionForm, EmployeeForm, PlacementForm, \
    OrganizationForm, SubdivisionForm, PositionForm
# Импорт пандас.
import pandas as pd
# Импорт рендера, перенаправления, генерации адреса и других урл функций.
from django.shortcuts import render, redirect, reverse, get_object_or_404
# Импорт простого ответа.
from django.http import HttpResponse, HttpResponseServerError, HttpResponseForbidden
# Проверка прав доступа для классов.
from guardian.mixins import PermissionListMixin
from guardian.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin as GPermissionRequiredMixin
# Импорт декораторов проверки прав.
from django.contrib.auth.decorators import permission_required, login_required
# Импорт моделей
from materials.models import Material, File
from courses.models import Course
from testing.models import Test
from events.models import Event
from learning_path.models import Result
from django.contrib.contenttypes.models import ContentType
# Импорт пагинатора
from django.core.paginator import Paginator
# Импорт времени с учетом таймзоны.
from django.utils import timezone
from django.db.models import OuterRef, Subquery, Prefetch
from django.db.models import F
from django.db.models import Case, When, Value, CharField
from django.db.models.functions import Concat
from django.contrib.postgres.aggregates import StringAgg
# Вью сет и сериализатор
from rest_framework import viewsets
from .serializers import EmployeeSerializer, OrganizationSerializer, SubdivisionSerializer, PositionSerializer, \
    PlacementSerializer
# Аутентификация ключами.
from rest_framework_api_key.permissions import HasAPIKey
# Импортируем функцию get_random_string для генерации пароля.
from django.utils.crypto import get_random_string
# Импортируем функцию make_password из модуля auth.hashers. Используется для хеширования паролей.
from django.contrib.auth.hashers import make_password
# Миксины.
from .mixins import PreviousPageSetMixinL1, PreviousPageGetMixinL1, PreviousPageSetMixinL2, PreviousPageGetMixinL2, \
    PreviousPageSetMixinL0, PreviousPageGetMixinL0
from reviews.models import Review
from core.models import EmployeesGroupObjectPermission
from reviews.filters import ObjectsReviewFilter
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from core.filters import EmployeesGroupObjectPermissionFilter
from django.db.models import OuterRef, Subquery
from django.core.paginator import Paginator
from django.contrib.auth.models import Permission

# Импортируем логи
import logging
# Создаем логгер с именем 'project'
logger = logging.getLogger('project')

# Вью сет сотрудника.
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all().order_by('last_name')
    serializer_class = EmployeeSerializer
    permission_classes = [HasAPIKey]

    # Получение списка сотрудников.
    def get_queryset(self):
        queryset = super().get_queryset()
        logger.info("HTTP-метод: %s", self.request.method)  # Тип HTTP-запроса.
        logger.info("Заголовки: %s", self.request.headers)  # HTTP-заголовки.
        logger.info("Параметры запроса: %s", self.request.query_params)  # Параметры в строке запроса.
        logger.info("Получаем список сотрудников: %s", queryset)  # Отладочное сообщение.
        return queryset

    # Получение конкретного объекта.
    def get_object(self):
        obj = super().get_object()
        logger.info("HTTP-метод: %s", self.request.method)  # Тип HTTP-запроса.
        logger.info("Заголовки: %s", self.request.headers)  # HTTP-заголовки.
        logger.info("Получаем детали сотрудника с ID %s: %s", obj.pk, obj)  # Отладочное сообщение.
        return obj

    # Операции при создании.
    def perform_create(self, serializer):
        logger.info("Создаем сотрудника через ViewSet")
        logger.info("HTTP-метод: %s", self.request.method)  # Метод HTTP.
        logger.info("Заголовки: %s", self.request.headers)  # Заголовки запроса.
        logger.info("Данные в запросе: %s", self.request.data)  # Тело запроса.
        serializer.save()

    # Операции при обновлении.
    def perform_update(self, serializer):
        logger.info("Обновляем сотрудника через ViewSet")
        logger.info("HTTP-метод: %s", self.request.method)  # Метод HTTP.
        logger.info("Заголовки: %s", self.request.headers)  # Заголовки запроса.
        logger.info("Данные для обновления: %s", self.request.data)  # Тело запроса.
        serializer.save()

    # Операции при удалении.
    def perform_destroy(self, instance):
        logger.info("Удаляем сотрудника через ViewSet")
        logger.info("HTTP-метод: %s", self.request.method)  # Метод HTTP.
        logger.info("Заголовки: %s", self.request.headers)  # Заголовки запроса.
        instance.delete()

# Вью сет организации.
class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all().order_by('legal_name')
    serializer_class = OrganizationSerializer
    permission_classes = [HasAPIKey]

    # Получение списка организаций.
    def get_queryset(self):
        queryset = super().get_queryset()
        logger.info("HTTP-метод: %s", self.request.method)  # Тип HTTP-запроса.
        logger.info("Заголовки: %s", self.request.headers)  # HTTP-заголовки.
        logger.info("Параметры запроса: %s", self.request.query_params)  # Параметры в строке запроса.
        logger.info("Получаем список организаций: %s", queryset)  # Отладочное сообщение.
        return queryset

    # Получение конкретного объекта.
    def get_object(self):
        obj = super().get_object()
        logger.info("HTTP-метод: %s", self.request.method)  # Тип HTTP-запроса.
        logger.info("Заголовки: %s", self.request.headers)  # HTTP-заголовки.
        logger.info("Получаем детали организации: %s", obj)  # Отладочное сообщение.
        return obj

    # Операции при создании.
    def perform_create(self, serializer):
        logger.info("Создаем организацию через ViewSet")
        logger.info("HTTP-метод: %s", self.request.method)  # Метод HTTP.
        logger.info("Заголовки: %s", self.request.headers)  # HTTP-заголовки.
        logger.info("Данные в запросе: %s", self.request.data)  # Тело запроса.
        serializer.save()

    # Операции при обновлении.
    def perform_update(self, serializer):
        logger.info("Обновляем организацию через ViewSet")
        logger.info("HTTP-метод: %s", self.request.method)  # Метод HTTP.
        logger.info("Заголовки: %s", self.request.headers)  # HTTP-заголовки.
        logger.info("Данные для обновления: %s", self.request.data)  # Тело запроса.
        serializer.save()

    # Операции при удалении.
    def perform_destroy(self, instance):
        logger.info("Удаляем организацию через ViewSet")
        logger.info("HTTP-метод: %s", self.request.method)  # Метод HTTP.
        logger.info("Заголовки: %s", self.request.headers)  # HTTP-заголовки.
        instance.delete()

# Вью сет подразделения.
class SubdivisionViewSet(viewsets.ModelViewSet):
    queryset = Subdivision.objects.all().order_by('name')
    serializer_class = SubdivisionSerializer
    permission_classes = [HasAPIKey]

    # Получение списка подразделений.
    def get_queryset(self):
        queryset = super().get_queryset()
        logger.info("HTTP-метод: %s", self.request.method)  # Тип HTTP-запроса.
        logger.info("Заголовки: %s", self.request.headers)  # HTTP-заголовки.
        logger.info("Параметры запроса: %s", self.request.query_params)  # Параметры в строке запроса.
        logger.info("Получаем список подразделений: %s", queryset)  # Отладочное сообщение.
        return queryset

    # Получение конкретного объекта.
    def get_object(self):
        obj = super().get_object()
        logger.info("HTTP-метод: %s", self.request.method)  # Тип HTTP-запроса.
        logger.info("Заголовки: %s", self.request.headers)  # HTTP-заголовки.
        logger.info("Получаем детали подразделения: %s", obj)  # Отладочное сообщение.
        return obj

    # Операции при создании.
    def perform_create(self, serializer):
        logger.info("Создаем подразделение через ViewSet")
        logger.info("HTTP-метод: %s", self.request.method)  # Метод HTTP.
        logger.info("Заголовки: %s", self.request.headers)  # HTTP-заголовки.
        logger.info("Данные в запросе: %s", self.request.data)  # Тело запроса.
        serializer.save()

    # Операции при обновлении.
    def perform_update(self, serializer):
        logger.info("Обновляем подразделение через ViewSet")
        logger.info("HTTP-метод: %s", self.request.method)  # Метод HTTP.
        logger.info("Заголовки: %s", self.request.headers)  # HTTP-заголовки.
        logger.info("Данные для обновления: %s", self.request.data)  # Тело запроса.
        serializer.save()

    # Операции при удалении.
    def perform_destroy(self, instance):
        logger.info("Удаляем подразделение через ViewSet")
        logger.info("HTTP-метод: %s", self.request.method)  # Метод HTTP.
        logger.info("Заголовки: %s", self.request.headers)  # HTTP-заголовки.
        instance.delete()

# Вью сет должности.
class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all().order_by('name')
    serializer_class = PositionSerializer
    permission_classes = [HasAPIKey]

    # Получение списка должностей.
    def get_queryset(self):
        queryset = super().get_queryset()
        logger.info("HTTP-метод: %s", self.request.method)  # Тип HTTP-запроса.
        logger.info("Заголовки: %s", self.request.headers)  # HTTP-заголовки.
        logger.info("Параметры запроса: %s", self.request.query_params)  # Параметры в строке запроса.
        logger.info("Получаем список должностей: %s", queryset)  # Отладочное сообщение.
        return queryset

    # Получение конкретного объекта.
    def get_object(self):
        obj = super().get_object()
        logger.info("HTTP-метод: %s", self.request.method)  # Тип HTTP-запроса.
        logger.info("Заголовки: %s", self.request.headers)  # HTTP-заголовки.
        logger.info("Получаем детали должности: %s", obj)  # Отладочное сообщение.
        return obj

    # Операции при создании.
    def perform_create(self, serializer):
        logger.info("Создаем должность через ViewSet")
        logger.info("HTTP-метод: %s", self.request.method)  # Метод HTTP.
        logger.info("Заголовки: %s", self.request.headers)  # HTTP-заголовки.
        logger.info("Данные в запросе: %s", self.request.data)  # Тело запроса.
        serializer.save()

    # Операции при обновлении.
    def perform_update(self, serializer):
        logger.info("Обновляем должность через ViewSet")
        logger.info("HTTP-метод: %s", self.request.method)  # Метод HTTP.
        logger.info("Заголовки: %s", self.request.headers)  # HTTP-заголовки.
        logger.info("Данные для обновления: %s", self.request.data)  # Тело запроса.
        serializer.save()

    # Операции при удалении.
    def perform_destroy(self, instance):
        logger.info("Удаляем должность через ViewSet")
        logger.info("HTTP-метод: %s", self.request.method)  # Метод HTTP.
        logger.info("Заголовки: %s", self.request.headers)  # HTTP-заголовки.
        instance.delete()

# Вью сет назначения должности.
class PlacementViewSet(viewsets.ModelViewSet):
    queryset = Placement.objects.all().order_by('employee')
    serializer_class = PlacementSerializer
    permission_classes = [HasAPIKey]

    # Получение списка назначений.
    def get_queryset(self):
        queryset = super().get_queryset()
        logger.info("HTTP-метод: %s", self.request.method)  # Тип HTTP-запроса.
        logger.info("Заголовки: %s", self.request.headers)  # HTTP-заголовки.
        logger.info("Параметры запроса: %s", self.request.query_params)  # Параметры в строке запроса.
        logger.info("Получаем список назначений: %s", queryset)  # Отладочное сообщение.
        return queryset

    # Получение конкретного объекта.
    def get_object(self):
        obj = super().get_object()
        logger.info("HTTP-метод: %s", self.request.method)  # Тип HTTP-запроса.
        logger.info("Заголовки: %s", self.request.headers)  # HTTP-заголовки.
        logger.info("Получаем детали назначения: %s", obj)  # Отладочное сообщение.
        return obj

    # Операции при создании.
    def perform_create(self, serializer):
        logger.info("Создаем назначение через ViewSet")
        logger.info("HTTP-метод: %s", self.request.method)  # Метод HTTP.
        logger.info("Заголовки: %s", self.request.headers)  # HTTP-заголовки.
        logger.info("Данные в запросе: %s", self.request.data)  # Тело запроса.
        serializer.save()

    # Операции при обновлении.
    def perform_update(self, serializer):
        logger.info("Обновляем назначение через ViewSet")
        logger.info("HTTP-метод: %s", self.request.method)  # Метод HTTP.
        logger.info("Заголовки: %s", self.request.headers)  # HTTP-заголовки.
        logger.info("Данные для обновления: %s", self.request.data)  # Тело запроса.
        serializer.save()

    # Операции при удалении.
    def perform_destroy(self, instance):
        logger.info("Удаляем назначение через ViewSet")
        logger.info("HTTP-метод: %s", self.request.method)  # Метод HTTP.
        logger.info("Заголовки: %s", self.request.headers)  # HTTP-заголовки.
        instance.delete()

# Список сотрудников.
class EmployeesView(PreviousPageSetMixinL1, PermissionListMixin, ListView):
    # Права доступа
    permission_required = 'core.view_employee'
    # Модель.
    model = Employee
    # Поле сортировки.
    ordering = 'last_name'
    # Шаблон.
    template_name = 'employees.html'
    # Количество объектов на странице
    paginate_by = 6

    # Переопределяем выборку вью.
    def get_queryset(self):
        # Забираем изначальную выборку вью.
        queryset = super().get_queryset().prefetch_related(
            'placements',
            'placements__employee',
            'placements__position__subdivision',
            'placements__position__subdivision__organization',
            'placements__position',
        )
        # Добавляем модель фильтрации в выборку вью.
        self.filterset = EmployeeFilter(self.request.GET, queryset, request=self.request)
        # Возвращаем вью новую выборку.
        return self.filterset.qs

    # Добавляем во вью переменные.
    def get_context_data(self, **kwargs):
        # Забираем изначальный набор переменных.
        context = super().get_context_data(**kwargs)
        # Добавляем фильтрсет.
        context['filterset'] = self.filterset
        # Возвращаем новый набор переменных.
        return context

# Объект сотрудника.
class EmployeeView(PreviousPageGetMixinL1, PermissionRequiredMixin, DetailView):
    # Права доступа.
    permission_required = 'core.view_employee'
    accept_global_perms = True
    # Модель.
    model = Employee
    # Шаблон.
    template_name = 'employee.html'

    # Переопределеяем переменные вью.
    def get_context_data(self, **kwargs):
        # забираем изначальный набор переменных
        context = super().get_context_data(**kwargs)
        # Забираем назначения пользователя.
        object_list = self.object.placements.all().order_by('start_date')
        qs_count = object_list.count()
        # Если назначения есть.
        if object_list.exists():
            # Добавляем пагинатор
            paginator = Paginator(object_list, 6)
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        # Если нет...
        else:
            # Задаем пустую переменную для проверки в шаблоне.
            page_obj = None
        # Добавляем во вью.
        context['object_list'] = object_list
        context['page_obj'] = page_obj
        context['qs_count'] = qs_count
        # Возвращаем новый набор переменных в контролер.
        return context

# Копируем адреса.
@permission_required('core.view_employee')
def copy_emails(request, pk):
    # Забираем группу.
    group = EmployeesGroup.objects.get(pk=pk)
    # Забираем список.
    employees_emails = group.user_set.exclude(email='').values_list('email', flat=True)
    if employees_emails:
        # Преобразуем в строку.
        employees_emails_str = '; '.join(employees_emails)
    # Уходим.
    back_button_url = reverse('core:group', kwargs={'pk': pk})
    back_button = f"<a href='{back_button_url}'>Назад</a>"
    return HttpResponse(f"Адреса: {employees_emails_str}. {back_button}")

# Создание сотрудника.
class EmployeeCreateView(GPermissionRequiredMixin, CreateView):
    # Права доступа.
    permission_required = 'core.add_employee'
    # Форма.
    form_class = EmployeeForm
    # Модель.
    model = Employee
    # Шаблон.
    template_name = 'employee_edit.html'

    # Заполнение полей данными.
    def get_initial(self):
        # Забираем изначальный набор.
        initial = super().get_initial()
        # Добавляем создателя: юзера отправившего запрос.
        initial["creator"] = self.request.user
        # Возвращаем значения в форму.
        return initial

    # Перенаправление после валидации формы.
    def get_success_url(self):
        # Направляем по адресу объекта.
        return reverse('core:employee', kwargs={'pk': self.object.pk})

# Копируем пароль пользователя.
@permission_required('core.change_employee')
def update_password(request, pk):
    # Получаем пользователя.
    user = Employee.objects.get(pk=pk)
    # Генерируем случайный пароль.
    random_password = get_random_string(length=8)
    # Копируем незашифрованный пароль в буфер обмена устанавливаем.
    user.set_password(random_password)
    user.save()
    back_button_url = reverse('core:employee', kwargs={'pk': pk})
    back_button = f"<a href='{back_button_url}'>Назад</a>"
    return HttpResponse(f"Обновленные данные: {user.username} - {random_password}. {back_button}")

# Изменение сотрудника.
class EmployeeUpdateView(PermissionRequiredMixin, UpdateView):
    # Права доступа.
    permission_required = 'core.change_employee'
    accept_global_perms = True
    # Форма.
    form_class = EmployeeForm
    # Модель.
    model = Employee
    # Шаблон.
    template_name = 'employee_edit.html'

    # Заполнение полей данными.
    def get_initial(self):
        # Забираем изначальный набор.
        initial = super().get_initial()
        # Добавляем создателя: юзера отправившего запрос.
        initial["creator"] = self.request.user
        # Возвращаем значения в форму.
        return initial

    # Перенаправление после валидации формы.
    def get_success_url(self):
        # Направляем по адресу объекта.
        return reverse('core:employee', kwargs={'pk': self.object.pk})

# Удаление сотрудника.
class EmployeeDeleteView(PermissionRequiredMixin, DeleteView):
    # Права доступа.
    permission_required = 'core.delete_employee'
    accept_global_perms = True
    # Модель.
    model = Employee
    # Шаблон.
    template_name = 'employee_delete.html'

    # Перенаправление после валидации формы.
    def get_success_url(self):
        # Направляем по адресу объектов.
        return reverse('core:employees')

# Список организаций.
class OrganizationsView(PreviousPageSetMixinL1, PermissionListMixin, ListView):
    # Права доступа
    permission_required = 'core.view_organization'
    # Модель.
    model = Organization
    # Поле сортировки.
    ordering = 'legal_name'
    # Шаблон.
    template_name = 'organizations.html'
    # Количество объектов на странице
    paginate_by = 6

    # Переопределяем выборку вью.
    def get_queryset(self):
        # Забираем изначальную выборку вью.
        queryset = super().get_queryset()
        # Добавляем модель фильтрации в выборку вью.
        self.filterset = OrganizationFilter(self.request.GET, queryset, request=self.request)
        # Возвращаем вью новую выборку.
        return self.filterset.qs

    # Добавляем во вью переменные.
    def get_context_data(self, **kwargs):
        # Забираем изначальный набор переменных.
        context = super().get_context_data(**kwargs)
        # Добавляем фильтрсет.
        context['filterset'] = self.filterset
        # Возвращаем новый набор переменных.
        return context

# Объект организации.
class OrganizationView(PreviousPageGetMixinL1, PermissionRequiredMixin, DetailView):
    # Права доступа.
    permission_required = 'core.view_organization'
    accept_global_perms = True
    # Модель.
    model = Organization
    # Шаблон.
    template_name = 'organization.html'

# Создание организации.
class OrganizationCreateView(GPermissionRequiredMixin, CreateView):
    # Права доступа.
    permission_required = 'core.add_organization'
    # Форма.
    form_class = OrganizationForm
    # Модель.
    model = Organization
    # Шаблон.
    template_name = 'organization_edit.html'

    # Заполнение полей данными.
    def get_initial(self):
        # Забираем изначальный набор.
        initial = super().get_initial()
        # Добавляем создателя: юзера отправившего запрос.
        initial["creator"] = self.request.user
        # Возвращаем значения в форму.
        return initial

    # Перенаправление после валидации формы.
    def get_success_url(self):
        # Направляем по адресу объекта.
        return reverse('core:organization', kwargs={'pk': self.object.pk})

# Изменение организации.
class OrganizationUpdateView(PermissionRequiredMixin, UpdateView):
    # Права доступа.
    permission_required = 'core.change_organization'
    accept_global_perms = True
    # Форма.
    form_class = OrganizationForm
    # Модель.
    model = Organization
    # Шаблон.
    template_name = 'organization_edit.html'

    # Заполнение полей данными.
    def get_initial(self):
        # Забираем изначальный набор.
        initial = super().get_initial()
        # Добавляем создателя: юзера отправившего запрос.
        initial["creator"] = self.request.user
        # Возвращаем значения в форму.
        return initial

    # Перенаправление после валидации формы.
    def get_success_url(self):
        # Направляем по адресу объекта.
        return reverse('core:organization', kwargs={'pk': self.object.pk})

# Удаление организации.
class OrganizationDeleteView(PermissionRequiredMixin, DeleteView):
    # Права доступа.
    permission_required = 'core.delete_organization'
    accept_global_perms = True
    # Модель.
    model = Organization
    # Шаблон.
    template_name = 'organization_delete.html'

    # Перенаправление после валидации формы.
    def get_success_url(self):
        # Направляем по адресу объектов.
        return reverse('core:organizations')

# Список подразделений.
class SubdivisionsView(PreviousPageSetMixinL1, PermissionListMixin, ListView):
    # Права доступа
    permission_required = 'core.view_subdivision'
    # Модель.
    model = Subdivision
    # Поле сортировки.
    ordering = 'name'
    # Шаблон.
    template_name = 'subdivisions.html'
    # Количество объектов на странице
    paginate_by = 6

    # Переопределяем выборку вью.
    def get_queryset(self):
        # Забираем изначальную выборку вью.
        queryset = super().get_queryset().prefetch_related(
            'organization',
        )
        # Добавляем модель фильтрации в выборку вью.
        self.filterset = SubdivisionFilter(self.request.GET, queryset, request=self.request)
        # Возвращаем вью новую выборку.
        return self.filterset.qs

    # Добавляем во вью переменные.
    def get_context_data(self, **kwargs):
        # Забираем изначальный набор переменных.
        context = super().get_context_data(**kwargs)
        # Добавляем фильтрсет.
        context['filterset'] = self.filterset
        # Возвращаем новый набор переменных.
        return context

# Объект подразделения.
class SubdivisionView(PreviousPageGetMixinL1, PermissionRequiredMixin, DetailView):
    # Права доступа.
    permission_required = 'core.view_subdivision'
    accept_global_perms = True
    # Модель.
    model = Subdivision
    # Шаблон.
    template_name = 'subdivision.html'

# Создание подразделения.
class SubdivisionCreateView(GPermissionRequiredMixin, CreateView):
    # Права доступа.
    permission_required = 'core.add_subdivision'
    # Форма.
    form_class = SubdivisionForm
    # Модель.
    model = Subdivision
    # Шаблон.
    template_name = 'subdivision_edit.html'

    # Заполнение полей данными.
    def get_initial(self):
        # Забираем изначальный набор.
        initial = super().get_initial()
        # Добавляем создателя: юзера отправившего запрос.
        initial["creator"] = self.request.user
        # Возвращаем значения в форму.
        return initial

    # Перенаправление после валидации формы.
    def get_success_url(self):
        # Направляем по адресу объекта.
        return reverse('core:subdivision', kwargs={'pk': self.object.pk})

# Изменение подразделения.
class SubdivisionUpdateView(PermissionRequiredMixin, UpdateView):
    # Права доступа.
    permission_required = 'core.change_subdivision'
    accept_global_perms = True
    # Форма.
    form_class = SubdivisionForm
    # Модель.
    model = Subdivision
    # Шаблон.
    template_name = 'subdivision_edit.html'

    # Заполнение полей данными.
    def get_initial(self):
        # Забираем изначальный набор.
        initial = super().get_initial()
        # Добавляем создателя: юзера отправившего запрос.
        initial["creator"] = self.request.user
        # Возвращаем значения в форму.
        return initial

    # Перенаправление после валидации формы.
    def get_success_url(self):
        # Направляем по адресу объекта.
        return reverse('core:subdivision', kwargs={'pk': self.object.pk})

# Удаление подразделения.
class SubdivisionDeleteView(PermissionRequiredMixin, DeleteView):
    # Права доступа.
    permission_required = 'core.delete_subdivision'
    accept_global_perms = True
    # Модель.
    model = Subdivision
    # Шаблон.
    template_name = 'subdivision_delete.html'

    # Перенаправление после валидации формы.
    def get_success_url(self):
        # Направляем по адресу объектов.
        return reverse('core:subdivisions')

# Список подразделений.
class PositionsView(PreviousPageSetMixinL1, PermissionListMixin, ListView):
    # Права доступа
    permission_required = 'core.view_position'
    # Модель.
    model = Position
    # Поле сортировки.
    ordering = 'name'
    # Шаблон.
    template_name = 'positions.html'
    # Количество объектов на странице
    paginate_by = 6

    # Переопределяем выборку вью.
    def get_queryset(self):
        # Забираем изначальную выборку вью.
        queryset = super().get_queryset()
        # Добавляем модель фильтрации в выборку вью.
        self.filterset = PositionFilter(self.request.GET, queryset, request=self.request)
        # Возвращаем вью новую выборку.
        return self.filterset.qs

    # Добавляем во вью переменные.
    def get_context_data(self, **kwargs):
        # Забираем изначальный набор переменных.
        context = super().get_context_data(**kwargs)
        # Добавляем фильтрсет.
        context['filterset'] = self.filterset
        # Возвращаем новый набор переменных.
        return context

# Объект подразделения.
class PositionView(PreviousPageGetMixinL1, PermissionRequiredMixin, DetailView):
    # Права доступа.
    permission_required = 'core.view_position'
    accept_global_perms = True
    # Модель.
    model = Position
    # Шаблон.
    template_name = 'position.html'

# Создание подразделения.
class PositionCreateView(GPermissionRequiredMixin, CreateView):
    # Права доступа.
    permission_required = 'core.add_position'
    # Форма.
    form_class = PositionForm
    # Модель.
    model = Position
    # Шаблон.
    template_name = 'position_edit.html'

    # Заполнение полей данными.
    def get_initial(self):
        # Забираем изначальный набор.
        initial = super().get_initial()
        # Добавляем создателя: юзера отправившего запрос.
        initial["creator"] = self.request.user
        # Возвращаем значения в форму.
        return initial

    # Перенаправление после валидации формы.
    def get_success_url(self):
        # Направляем по адресу объекта.
        return reverse('core:position', kwargs={'pk': self.object.pk})

# Изменение подразделения.
class PositionUpdateView(PermissionRequiredMixin, UpdateView):
    # Права доступа.
    permission_required = 'core.change_position'
    accept_global_perms = True
    # Форма.
    form_class = PositionForm
    # Модель.
    model = Position
    # Шаблон.
    template_name = 'position_edit.html'

    # Заполнение полей данными.
    def get_initial(self):
        # Забираем изначальный набор.
        initial = super().get_initial()
        # Добавляем создателя: юзера отправившего запрос.
        initial["creator"] = self.request.user
        # Возвращаем значения в форму.
        return initial

    # Перенаправление после валидации формы.
    def get_success_url(self):
        # Направляем по адресу объекта.
        return reverse('core:position', kwargs={'pk': self.object.pk})

# Удаление подразделения.
class PositionDeleteView(PermissionRequiredMixin, DeleteView):
    # Права доступа.
    permission_required = 'core.delete_position'
    accept_global_perms = True
    # Модель.
    model = Position
    # Шаблон.
    template_name = 'position_delete.html'

    # Перенаправление после валидации формы.
    def get_success_url(self):
        # Направляем по адресу объектов.
        return reverse('core:positions')

# Создание категории.
class PlacementCreateView(GPermissionRequiredMixin, CreateView):
    # Права доступа.
    permission_required = 'core.add_placement'
    # Форма.
    form_class = PlacementForm
    # Модель.
    model = Placement
    # Шаблон.
    template_name = 'placement_edit.html'

    # Заполнение полей данными.
    def get_initial(self):
        # Забираем изначальный набор.
        initial = super().get_initial()
        # Добавляем создателя: юзера отправившего запрос.
        initial["creator"] = self.request.user
        # Добавляем выбранного сотрудника.
        employee = Employee.objects.get(pk=self.kwargs.get('pk'))
        initial["employee"] = employee
        # Возвращаем значения в форму.
        return initial

    # Перенаправление после валидации формы.
    def get_success_url(self):
        # Направляем по адресу объекта.
        return reverse('core:employee', kwargs={'pk': self.object.employee.pk})

# Изменение категории.
class PlacementUpdateView(PermissionRequiredMixin, UpdateView):
    # Права доступа.
    permission_required = 'core.change_placement'
    accept_global_perms = True
    # Форма.
    form_class = PlacementForm
    # Модель.
    model = Placement
    # Шаблон.
    template_name = 'placement_edit.html'

    # Заполнение полей данными.
    def get_initial(self):
        # Забираем изначальный набор.
        initial = super().get_initial()
        # Добавляем создателя: юзера отправившего запрос.
        initial["creator"] = self.request.user
        # Добавляем выбранного сотрудника.
        initial["employee"] = self.object.employee
        # Добавляем время начала и время конца.
        if self.object.start_date:
            initial["start_date"] = self.object.start_date.strftime('%Y-%m-%d')
        if self.object.end_date:
            initial["end_date"] = self.object.end_date.strftime('%Y-%m-%d')
        # Возвращаем значения в форму.
        return initial

    # Перенаправление после валидации формы.
    def get_success_url(self):
        # Направляем по адресу объекта.
        return reverse('core:employee', kwargs={'pk': self.object.employee.pk})

# Удаление категории.
class PlacementDeleteView(PermissionRequiredMixin, DeleteView):
    # Права доступа.
    permission_required = 'core.delete_placement'
    accept_global_perms = True
    # Модель.
    model = Placement
    # Шаблон.
    template_name = 'placement_delete.html'

    # Перенаправление после валидации формы.
    def get_success_url(self):
        # Направляем по адресу объектов.
        return reverse('core:employee', kwargs={'pk': self.object.employee.pk})

# Список импортов.
class EmployeeExcelImportsView(PreviousPageSetMixinL1, PermissionRequiredMixin, ListView):
    # Права доступа
    permission_required = 'core.view_employeeexcelimport'
    accept_global_perms = True
    # Модель.
    model = EmployeeExcelImport
    # Поле сортировки.
    ordering = 'created'
    # Шаблон.
    template_name = 'employee_excel_imports.html'
    # Количество объектов на странице
    paginate_by = 6

    # Переопределяем выборку вью.
    def get_queryset(self):
        # Забираем изначальную выборку вью.
        queryset = super().get_queryset().prefetch_related(
            'categories',
        )
        # Добавляем модель фильтрации в выборку вью.
        self.filterset = EmployeeExcelImportFilter(self.request.GET, queryset, request=self.request)
        # Возвращаем вью новую выборку.
        return self.filterset.qs

    # Добавляем во вью переменные.
    def get_context_data(self, **kwargs):
        # Забираем изначальный набор переменных.
        context = super().get_context_data(**kwargs)
        # Добавляем фильтрсет.
        context['filterset'] = self.filterset
        # Возвращаем новый набор переменных.
        return context

# Вью импорта.
class EmployeeExcelImportView(PreviousPageGetMixinL1, PermissionRequiredMixin, DetailView):
    # Права доступа.
    permission_required = 'core.view_employeeexcelimport'
    accept_global_perms = True
    # Модель.
    model = EmployeeExcelImport
    # Шаблон.
    template_name = 'employee_excel_import.html'

# Вью добавления импорта
class EmployeeExcelImportCreateView(GPermissionRequiredMixin, CreateView):
    # Права доступа.
    permission_required = 'core.add_employeeexcelimport'
    # Форма.
    form_class = EmployeeExcelImportForm
    # Модель.
    model = EmployeeExcelImport
    # Шаблон.
    template_name = 'employee_excel_import_edit.html'

    # Заполнение полей данными.
    def get_initial(self):
        # Забираем изначальный набор.
        initial = super().get_initial()
        # Добавляем создателя: юзера отправившего запрос.
        initial["creator"] = self.request.user
        # Возвращаем значения в форму.
        return initial

    # Перенаправление после валидации формы.
    def get_success_url(self):
        # Направляем по адресу родительского каталога.
        return reverse('core:employee_excel_import', kwargs={'pk': self.object.pk})

# Вью обновления импорта.
class EmployeeExcelImportUpdateView(PermissionRequiredMixin, UpdateView):
    # Права доступа.
    permission_required = 'core.change_employeeexcelimport'
    accept_global_perms = True
    # Форма.
    form_class = EmployeeExcelImportForm
    # Модель.
    model = EmployeeExcelImport
    # Шаблон.
    template_name = 'employee_excel_import_edit.html'

    # Заполнение полей данными.
    def get_initial(self):
        # Забираем изначальный набор.
        initial = super().get_initial()
        # Добавляем создателя: юзера отправившего запрос.
        initial["creator"] = self.request.user
        # Возвращаем значения в форму.
        return initial

    # Перенаправление после валидации формы.
    def get_success_url(self):
        # Направляем по адресу родительского каталога.
        return reverse('core:employee_excel_import', kwargs={'pk': self.object.pk})

# Удаление категории.
class EmployeeExcelImportDeleteView(PermissionRequiredMixin, DeleteView):
    # Права доступа.
    permission_required = 'core.delete_employeeexcelimport'
    accept_global_perms = True
    # Модель.
    model = EmployeeExcelImport
    # Шаблон.
    template_name = 'employee_excel_import_delete.html'

    # Перенаправление после валидации формы.
    def get_success_url(self):
        # Направляем по адресу объектов.
        return reverse('core:employee_excel_imports')

# Импорт по MDM ID.
@permission_required('core.add_employeeexcelimport')
def start_employee_excel_import_mdm_view(request, pk):
    # Генерируем URL на основе имени маршрута 'employee_excel_import' и передавая значение pk
    back_button_url = reverse('core:employee_excel_import', kwargs={'pk': pk})
    back_button = f"<a href='{back_button_url}'>Назад</a>"

    try:
        # Загрузка и обработка Excel файла.
        excel_file = get_object_or_404(EmployeeExcelImport, pk=pk)
        date_columns = ['Дата рождения пользователя', 'Дата начала работы', 'Дата окончания работы']
        df = pd.read_excel(
            # Забираем файл.
            excel_file.upload_file.path,
            # Описываем типы обычных полей.
            dtype={
                'MDM ID организации': str,
                'MDM ID подразделения': str,
                'MDM ID родительского подразделения': str,
                'MDM ID должности': str,
                'MDM ID сотрудника': str,
                'Юридическое название организации': str,
                'ИНН организации': str,
                'Название подразделения': str,
                'Название родительского подразделения': str,
                'Название должности': str,
                'Логин пользователя': str,
                'Имя пользователя': str,
                'Фамилия пользователя': str,
                'Отчество пользователя': str,
                'Номер телефона пользователя': str,
                'Номер мобильного телефона пользователя': str,
                'Электронный адрес пользователя': str,
                'Пользователь активен': str,
                'Руководитель': str
            },
            # Описываем даты.
            parse_dates = date_columns,
            # Вставляем стандартную проверку ошибок.
            date_parser = lambda x: pd.to_datetime(x, errors='coerce')
        )

        for _, row in df.iterrows():

            # Проверка возможности добавить организацию.
            organizations_required_fields = [
                'MDM ID организации',
                'Юридическое название организации',
                'ИНН организации',
            ]

            # Если данных не хватает - бездействуем.
            if any(pd.isna(row[field]) or row[field].strip() == "" for field in organizations_required_fields):
                logger.info(f"Не хватает данных для добавления организации")

            # Если данные есть - добавляем.
            else:

                # Получение или генерация данных для Organization.
                org_mdm_id = row['MDM ID организации'].strip()
                org_defaults = {
                    'legal_name': row['Юридическое название организации'].strip(),
                    'tin': row['ИНН организации'].strip()
                }

                # Проверка, изменились ли данные.
                org, created = Organization.objects.get_or_create(mdm_id=org_mdm_id, defaults=org_defaults)
                if created:
                    logger.info(f"Добавлена организация: {org}")
                if not created:
                    needs_update = any(getattr(org, key) != value for key, value in org_defaults.items())
                    if needs_update:
                        for key, value in org_defaults.items():
                            setattr(org, key, value)
                        org.save()
                        logger.info(f"Обновлена организация: {org}")

            # Проверка возможности добавить подразделение.
            subdivisions_required_fields = [
                'MDM ID организации',
                'MDM ID подразделения',
                'Юридическое название организации',
                'ИНН организации',
                'Название подразделения',
            ]

            # Если данных не хватает - бездействуем.
            if any(pd.isna(row[field]) or (isinstance(row[field], str) and row[field].strip() == "") for field in subdivisions_required_fields):
                logger.info(f"Не хватает данных для добавления подразделения")

            # Если данные есть - добавляем.
            else:

                # Получение или генерация данных для Subdivision.
                sub_mdm_id = row['MDM ID подразделения'].strip()
                sub_defaults = {
                    'name': row['Название подразделения'].strip(),
                    'organization': org
                }

                # Проверка, изменились ли данные.
                sub, created = Subdivision.objects.get_or_create(mdm_id=sub_mdm_id, defaults=sub_defaults)
                if created:
                    logger.info(f"Добавлено подразделение: {sub}")
                if not created:
                    needs_update = any(getattr(sub, key) != value for key, value in sub_defaults.items())
                    if needs_update:
                        for key, value in sub_defaults.items():
                            setattr(sub, key, value)
                        sub.save()
                        logger.info(f"Обновлено подразделение: {sub}")

                # Установка родительского подразделения.
                parent_sub_mdm_id = row['MDM ID родительского подразделения']
                # Проверка, что parent_sub_name существует и не None или NaN.
                if parent_sub_mdm_id and not pd.isna(parent_sub_mdm_id):
                    # Создание.
                    parent_sub_mdm_id = str(parent_sub_mdm_id).strip()
                    # Попытка найти объект по заданному критерию
                    parent_sub = Subdivision.objects.filter(mdm_id=parent_sub_mdm_id).first()
                    if parent_sub:
                        sub.parent_subdivision = parent_sub
                        sub.save()
                        logger.info(f"Установлено родительское подразделение: {parent_sub}")
                    else:
                        logger.info(f"Родительское подразделение не найдено")

            # Проверка возможности добавить должность.
            positions_required_fields = [
                'MDM ID подразделения',
                'Название подразделения',
                'MDM ID должности',
                'Название должности',
            ]

            # Если данных не хватает - бездействуем.
            if any(pd.isna(row[field]) or (isinstance(row[field], str) and row[field].strip() == "") for field in positions_required_fields):
                logger.info(f"Не хватает данных для добавления должности")

            # Если данные есть - добавляем.
            else:

                # Получение или генерация данных для Position.
                pos_mdm_id = row['MDM ID должности'].strip()
                pos_defaults = {
                    'name': row['Название должности'].strip(),
                    'subdivision': sub
                }

                # Проверка, изменились ли данные.
                pos, created = Position.objects.get_or_create(mdm_id=pos_mdm_id, defaults=pos_defaults)
                if created:
                    logger.info(f"Добавлена должность: {pos}")
                if not created:
                    needs_update = any(getattr(pos, key) != value for key, value in pos_defaults.items())
                    if needs_update:
                        for key, value in pos_defaults.items():
                            setattr(pos, key, value)
                        pos.save()
                        logger.info(f"Обновлена должность: {pos}")

            # Проверка возможности добавить сотрудника.
            employees_required_fields = [
                'MDM ID организации',
                'MDM ID подразделения',
                'MDM ID должности',
                'MDM ID сотрудника',
                'Юридическое название организации',
                'ИНН организации',
                'Название подразделения',
                'Название должности',
                'Логин пользователя',
                'Имя пользователя',
                'Фамилия пользователя',
                'Отчество пользователя',
                'Электронный адрес пользователя',
                'Дата начала работы',
                'Пользователь активен',
                'Руководитель',
            ]

            # Если данных не хватает - бездействуем.
            if any(pd.isna(row[field]) or (isinstance(row[field], str) and row[field].strip() == "") for field in employees_required_fields):
                logger.info(f"Не хватает данных для добавления сотрудника")

            # Если данные есть - добавляем.
            else:

                # Получение или генерация данных для Employee.
                emp_mdm_id = row['MDM ID сотрудника'].strip()
                emp_defaults = {
                    'username': row['Логин пользователя'].strip(),
                    'first_name': row['Имя пользователя'].strip(),
                    'last_name': row['Фамилия пользователя'].strip(),
                    'fathers_name': row['Отчество пользователя'].strip(),
                    'phone': row['Номер телефона пользователя'].strip() if not pd.isna(row['Номер телефона пользователя']) else None,
                    'mobile_phone': row['Номер мобильного телефона пользователя'].strip() if not pd.isna(row['Номер мобильного телефона пользователя']) else None,
                    'email': row['Электронный адрес пользователя'].strip(),
                    'birthday': None if pd.isna(row['Дата рождения пользователя']) else row['Дата рождения пользователя'],
                    'is_active': row['Пользователь активен'].strip().lower() == 'true',
                    #'excel_import': excel_file,
                }

                # Проверка, изменились ли данные.
                emp, created = Employee.objects.get_or_create(mdm_id=emp_mdm_id, defaults=emp_defaults)

                # Если сотрудник создан.
                if created:

                    logger.info(f"Добавлен сотрудник: {emp}")
                    # Добавление сотрудника в группу, связанную с его импортом Excel.
                    group_name = f"Импорт из Excel: [{excel_file.id}] {excel_file.name}"
                    group, _ = EmployeesGroup.objects.get_or_create(name=group_name)
                    group.user_set.add(emp)
                    logger.info(f"Сотрудник добавлен в группу: {group}")

                    # Если группа была создана в процессе, связываем её с импортом Excel.
                    if created:
                        excel_file.group = group
                        excel_file.save()
                        logger.info(f"{excel_file} связан с группой: {group}")

                # Если сотрудник уже есть.
                if not created:
                    needs_update = any(getattr(emp, key) != value for key, value in emp_defaults.items())
                    if needs_update:
                        for key, value in emp_defaults.items():
                            setattr(emp, key, value)
                        emp.save()
                        logger.info(f"Обновлен сотрудник: {emp}")

                # Получение или генерация данных для Placement.
                placement_defaults = {
                    'manager': row['Руководитель'].strip().lower() == 'true',
                    'start_date': None if pd.isna(row['Дата начала работы']) else row['Дата начала работы'],
                    'end_date': None if pd.isna(row['Дата окончания работы']) else row['Дата окончания работы']
                }

                # Получение объекта Placement или создание нового, если он не существует.
                placement, created = Placement.objects.get_or_create(
                    position=pos,
                    employee=emp,
                    defaults=placement_defaults
                )

                # Если объект был найден, а не создан, проверим, нужно ли обновлять поля.
                if created:
                    logger.info(f"Добавлена должность сотрудника: {placement}")
                if not created:
                    needs_update = any(getattr(placement, key) != value for key, value in placement_defaults.items())
                    if needs_update:
                        for key, value in placement_defaults.items():
                            setattr(placement, key, value)
                        placement.save()
                        logger.info(f"Обновлена должность сотрудника: {placement}")

        # Отметка о завершении обработки файла.
        excel_file.processed = True
        excel_file.save()

    except Exception as e:
        # Логирование ошибки с полной трассировкой исключения
        logger.error(f"Ошибка при импорте данных: {e}", exc_info=True)

        # Если DEBUG=True, повторно вызываем исключение, чтобы Django отобразил страницу ошибки.
        if settings.DEBUG:
            raise
        else:
            return HttpResponseServerError("Ошибка сервера, обратитесь к администратору")

    # Возврат созданных сотрудников.
    return HttpResponse(f"Импорт завершен успешно. {back_button}")

# Импорт по именам объектов.
@permission_required('core.add_employeeexcelimport')
def start_employee_excel_import_name_view(request, pk):
    # Генерируем URL на основе имени маршрута 'employee_excel_import' и передавая значение pk
    back_button_url = reverse('core:employee_excel_import', kwargs={'pk': pk})
    back_button = f"<a href='{back_button_url}'>Назад</a>"

    try:
        # Загрузка и обработка Excel файла.
        excel_file = get_object_or_404(EmployeeExcelImport, pk=pk)
        date_columns = ['Дата рождения пользователя', 'Дата начала работы', 'Дата окончания работы']
        df = pd.read_excel(
            # Забираем файл.
            excel_file.upload_file.path,
            # Описываем типы обычных полей.
            dtype={
                'Юридическое название организации': str,
                'ИНН организации': str,
                'Название подразделения': str,
                'Название родительского подразделения': str,
                'Название должности': str,
                'Логин пользователя': str,
                'Имя пользователя': str,
                'Фамилия пользователя': str,
                'Отчество пользователя': str,
                'Номер телефона пользователя': str,
                'Номер мобильного телефона пользователя': str,
                'Электронный адрес пользователя': str,
                'Пользователь активен': str,
                'Руководитель': str
            },
            # Описываем даты.
            parse_dates=date_columns,
            # Вставляем стандартную проверку ошибок.
            date_parser=lambda x: pd.to_datetime(x, errors='coerce')
        )

        for _, row in df.iterrows():

            # Проверка возможности добавить организацию.
            organizations_required_fields = [
                'Юридическое название организации',
                'ИНН организации',
            ]

            # Если данных не хватает - бездействуем.
            if any(pd.isna(row[field]) or row[field].strip() == "" for field in organizations_required_fields):
                logger.info(f"Не хватает данных для добавления организации")

            # Если данные есть - добавляем.
            else:

                # Обработка Organization.
                org_defaults = {
                    'legal_name': row['Юридическое название организации'].strip(),
                    'tin': row['ИНН организации'].strip()
                }
                org, created = Organization.objects.get_or_create(tin=org_defaults['tin'], defaults=org_defaults)
                if created:
                    logger.info(f"Добавлена организация: {org}")
                if not created:
                    needs_update = any(getattr(org, key) != value for key, value in org_defaults.items())
                    if needs_update:
                        for key, value in org_defaults.items():
                            setattr(org, key, value)
                        org.save()
                    logger.info(f"Обновлена организация: {org}")

            # Проверка возможности добавить подразделение.
            subdivisions_required_fields = [
                'Юридическое название организации',
                'ИНН организации',
                'Название подразделения'
            ]

            # Если данных не хватает - бездействуем.
            if any(pd.isna(row[field]) or (isinstance(row[field], str) and row[field].strip() == "") for
                   field in subdivisions_required_fields):
                logger.info(f"Не хватает данных для добавления подразделения")

            # Если данные есть - добавляем.
            else:

                # Обработка Subdivision.
                sub_defaults = {
                    'name': row['Название подразделения'].strip(),
                    'organization': org
                }
                sub, created = Subdivision.objects.get_or_create(
                    name=sub_defaults['name'],
                    organization=sub_defaults['organization'],
                    defaults=sub_defaults
                )
                if created:
                    logger.info(f"Добавлено подразделение: {sub}")
                if not created:
                    needs_update = any(getattr(sub, key) != value for key, value in sub_defaults.items())
                    if needs_update:
                        for key, value in sub_defaults.items():
                            setattr(sub, key, value)
                        sub.save()
                        logger.info(f"Обновлено подразделение: {sub}")

                # Установка родительского подразделения.
                parent_sub_name = row.get('Название родительского подразделения')
                # Проверка, что parent_sub_name существует и не None или NaN.
                if parent_sub_name and not pd.isna(parent_sub_name):
                    # Создание.
                    parent_sub_name = parent_sub_name.strip()
                    parent_sub = Subdivision.objects.filter(name=parent_sub_name).first()
                    if parent_sub:
                        sub.parent_subdivision = parent_sub
                        sub.save()
                        logger.info(f"Установлено родительское подразделение: {parent_sub}")
                    else:
                        logger.info(f"Родительское подразделение не найдено")

            # Проверка возможности добавить должность.
            positions_required_fields = [
                'Название подразделения',
                'Название должности',
            ]

            # Если данных не хватает - бездействуем.
            if any(pd.isna(row[field]) or (isinstance(row[field], str) and row[field].strip() == "") for field
                   in positions_required_fields):
                logger.info(f"Не хватает данных для добавления должности")

            # Если данные есть - добавляем.
            else:

                # Обработка Position.
                pos_defaults = {
                    'name': row['Название должности'].strip(),
                    'subdivision': sub
                }
                pos, created = Position.objects.get_or_create(name=pos_defaults['name'], defaults=pos_defaults)
                if created:
                    logger.info(f"Добавлена должность: {pos}")
                if not created:
                    needs_update = any(getattr(pos, key) != value for key, value in pos_defaults.items())
                    if needs_update:
                        for key, value in pos_defaults.items():
                            setattr(pos, key, value)
                        pos.save()
                        logger.info(f"Обновлена должность: {pos}")

            # Проверка возможности добавить сотрудника.
            employees_required_fields = [
                'Юридическое название организации',
                'ИНН организации',
                'Название подразделения',
                'Название должности',
                'Логин пользователя',
                'Имя пользователя',
                'Фамилия пользователя',
                'Отчество пользователя',
                'Электронный адрес пользователя',
                'Дата начала работы',
                'Пользователь активен',
                'Руководитель',
            ]

            # Если данных не хватает - бездействуем.
            if any(pd.isna(row[field]) or (isinstance(row[field], str) and row[field].strip() == "") for
                   field in employees_required_fields):
                logger.info(f"Не хватает данных для добавления сотрудника")

            # Если данные есть - добавляем.
            else:

                # Обработка Employee.
                emp_defaults = {
                    'username': row['Логин пользователя'].strip(),
                    'first_name': row['Имя пользователя'].strip(),
                    'last_name': row['Фамилия пользователя'].strip(),
                    'fathers_name': row['Отчество пользователя'].strip(),
                    'phone': row['Номер телефона пользователя'].strip() if not pd.isna(row['Номер телефона пользователя']) else None,
                    'mobile_phone': row['Номер мобильного телефона пользователя'].strip() if not pd.isna(row['Номер мобильного телефона пользователя']) else None,
                    'email': row['Электронный адрес пользователя'].strip(),
                    'birthday': None if pd.isna(row['Дата рождения пользователя']) else row['Дата рождения пользователя'],
                    'is_active': row['Пользователь активен'].strip().lower() == 'true',
                    #'excel_import': excel_file,
                }
                emp, created = Employee.objects.get_or_create(username=emp_defaults['username'], defaults=emp_defaults)

                # Если сотрудник создан.
                if created:
                    logger.info(f"Добавлен сотрудник: {emp}")
                    # Добавление сотрудника в группу, связанную с его импортом Excel.
                    group_name = f"Импорт из Excel: [{excel_file.id}] {excel_file.name}"
                    group, _ = EmployeesGroup.objects.get_or_create(name=group_name)
                    group.user_set.add(emp)
                    logger.info(f"Сотрудник добавлен в группу: {group}")

                    # Если группа была создана в процессе, связываем её с импортом Excel.
                    if created:
                        excel_file.group = group
                        excel_file.save()
                        logger.info(f"{excel_file} связан с группой: {group}")

                # Если сотрудник уже есть.
                if not created:
                    needs_update = any(getattr(emp, key) != value for key, value in emp_defaults.items())
                    if needs_update:
                        for key, value in emp_defaults.items():
                            setattr(emp, key, value)
                        emp.save()
                        logger.info(f"Обновлен сотрудник: {emp}")

                # Получение или генерация данных для Placement.
                placement_defaults = {
                    'manager': row['Руководитель'].strip().lower() == 'true',
                    'start_date': None if pd.isna(row['Дата начала работы']) else row['Дата начала работы'],
                    'end_date': None if pd.isna(row['Дата окончания работы']) else row['Дата окончания работы']
                }

                # Получение объекта Placement или создание нового, если он не существует.
                placement, created = Placement.objects.get_or_create(
                    position=pos,
                    employee=emp,
                    defaults=placement_defaults
                )

                # Если объект был найден, а не создан, проверим, нужно ли обновлять поля.
                if created:
                    logger.info(f"Добавлена должность сотрудника: {placement}")
                if not created:
                    needs_update = any(getattr(placement, key) != value for key, value in placement_defaults.items())
                    if needs_update:
                        for key, value in placement_defaults.items():
                            setattr(placement, key, value)
                        placement.save()
                        logger.info(f"Обновлена должность сотрудника: {placement}")

        # Отметка о завершении обработки файла.
        excel_file.processed = True
        excel_file.save()

    except Exception as e:
        # Логирование ошибки с полной трассировкой исключения
        logger.error(f"Ошибка при импорте данных: {e}", exc_info=True)

        # Если DEBUG=True, повторно вызываем исключение, чтобы Django отобразил страницу ошибки.
        if settings.DEBUG:
            raise
        else:
            return HttpResponseServerError("Ошибка сервера, обратитесь к администратору")

    return HttpResponse(f"Импорт завершен успешно. {back_button}")

# Список категорий.
class CategoriesView(PreviousPageSetMixinL1, PermissionListMixin, ListView):
    # Права доступа
    permission_required = 'core.view_category'
    # Модель.
    model = Category
    # Поле сортировки.
    ordering = 'name'
    # Шаблон.
    template_name = 'categories.html'
    # Количество объектов на странице
    paginate_by = 6

    # Переопределяем выборку вью.
    def get_queryset(self):
        # Забираем изначальную выборку вью.
        queryset = super().get_queryset()
        # Добавляем модель фильтрации в выборку вью.
        self.filterset = CategoryFilter(self.request.GET, queryset, request=self.request)
        # Возвращаем вью новую выборку.
        return self.filterset.qs

    # Добавляем во вью переменные.
    def get_context_data(self, **kwargs):
        # Забираем изначальный набор переменных.
        context = super().get_context_data(**kwargs)
        # Добавляем фильтрсет.
        context['filterset'] = self.filterset
        # Возвращаем новый набор переменных.
        return context

# Объект категории.
class CategoryView(PreviousPageGetMixinL1, PermissionRequiredMixin, DetailView):
    # Права доступа.
    permission_required = 'core.view_category'
    accept_global_perms = True
    # Модель.
    model = Category
    # Шаблон.
    template_name = 'category.html'

# Создание категории.
class CategoryCreateView(GPermissionRequiredMixin, CreateView):
    # Права доступа.
    permission_required = 'core.add_category'
    # Форма.
    form_class = CategoryForm
    # Модель.
    model = Category
    # Шаблон.
    template_name = 'category_edit.html'

    # Заполнение полей данными.
    def get_initial(self):
        # Забираем изначальный набор.
        initial = super().get_initial()
        # Добавляем создателя: юзера отправившего запрос.
        initial["creator"] = self.request.user
        # Возвращаем значения в форму.
        return initial

    # Перенаправление после валидации формы.
    def get_success_url(self):
        # Направляем по адресу объекта.
        return reverse('core:category', kwargs={'pk': self.object.pk})

# Изменение категории.
class CategoryUpdateView(PermissionRequiredMixin, UpdateView):
    # Права доступа.
    permission_required = 'core.change_category'
    accept_global_perms = True
    # Форма.
    form_class = CategoryForm
    # Модель.
    model = Category
    # Шаблон.
    template_name = 'category_edit.html'

    # Заполнение полей данными.
    def get_initial(self):
        # Забираем изначальный набор.
        initial = super().get_initial()
        # Добавляем создателя: юзера отправившего запрос.
        initial["creator"] = self.request.user
        # Возвращаем значения в форму.
        return initial

    # Перенаправление после валидации формы.
    def get_success_url(self):
        # Направляем по адресу объекта.
        return reverse('core:category', kwargs={'pk': self.object.pk})

# Удаление категории.
class CategoryDeleteView(PermissionRequiredMixin, DeleteView):
    # Права доступа.
    permission_required = 'core.delete_category'
    # Модель.
    model = Category
    # Шаблон.
    template_name = 'category_delete.html'

    # Перенаправление после валидации формы.
    def get_success_url(self):
        # Направляем по адресу объектов.
        return reverse('core:categories')

# Список прав на объекты.
class GroupsView(PreviousPageSetMixinL1, PermissionListMixin, ListView):
    # Права доступа
    permission_required = 'core.view_employeesgroup'
    # Модель.
    model = EmployeesGroup
    # Поле сортировки.
    ordering = 'name'
    # Шаблон.
    template_name = 'groups.html'
    # Количество объектов на странице
    paginate_by = 6

    # Переопределяем выборку вью.
    def get_queryset(self):
        # Забираем изначальную выборку вью.
        queryset = super().get_queryset().prefetch_related(
            'categories',
        )
        # Добавляем модель фильтрации в выборку вью.
        self.filterset = GroupFilter(self.request.GET, queryset, request=self.request)
        # Возвращаем вью новую выборку.
        return self.filterset.qs

    # Добавляем во вью переменные.
    def get_context_data(self, **kwargs):
        # Забираем изначальный набор переменных.
        context = super().get_context_data(**kwargs)
        # Добавляем фильтрсет.
        context['filterset'] = self.filterset
        # Возвращаем новый набор переменных.
        return context

# Объект категории.
class GroupView(PreviousPageGetMixinL1, PreviousPageSetMixinL0, PermissionRequiredMixin, ListView):
    # Права доступа
    permission_required = 'core.view_employeesgroup'
    accept_global_perms = True
    # Модель.
    model = Employee
    # Шаблон.
    template_name = 'group.html'
    # Количество объектов на странице
    paginate_by = 6

    # Определяем объект проверки.
    def get_permission_object(self):
        group = EmployeesGroup.objects.get(pk=self.kwargs.get('pk'))
        return group

    # Переопределяем выборку вью.
    def get_queryset(self):
        # Переопределяем изначальную выборку.
        group = self.get_permission_object()
        queryset = super().get_queryset().filter(groups=group).order_by('last_name')
        self.qs_count = len(queryset)
        # Добавляем модель фильтрации в выборку вью.
        self.filterset = GroupsEmployeeFilter(self.request.GET, queryset, request=self.request)
        # Возвращаем вью новую выборку.
        return self.filterset.qs

    # Добавляем во вью переменные.
    def get_context_data(self, **kwargs):
        # Забираем изначальный набор переменных.
        context = super().get_context_data(**kwargs)

        # Добавляем во вью.
        group = self.get_permission_object()
        context['object'] = group
        context['qs_count'] = self.qs_count

        # Добавляем фильтрсет.
        context['filterset'] = self.filterset

        # Добавляем объектные права.
        if EmployeesGroupObjectPermission.objects.filter(group__id=self.kwargs.get('pk')).prefetch_related('content_object').exists():
            group_object_permissions_queryset = EmployeesGroupObjectPermission.objects.filter(
                group__id=self.kwargs.get('pk')
            ).prefetch_related('content_object').order_by('-id')
        else:
            group_object_permissions_queryset = EmployeesGroupObjectPermission.objects.none()
        context['group_object_permissions_qs_count'] = len(group_object_permissions_queryset)
        group_object_permissions_filter = EmployeesGroupObjectPermissionFilter(self.request.GET, queryset=group_object_permissions_queryset, request=self.request)
        group_object_permissions = group_object_permissions_filter.qs
        # Добавляем пагинатор.
        group_object_permissions_paginator = Paginator(group_object_permissions, 6)
        group_object_permissions_page_number = self.request.GET.get('group_object_permissions_page')
        group_object_permissions_page_obj = group_object_permissions_paginator.get_page(group_object_permissions_page_number)

        # Добавляем глобальные права.
        if Permission.objects.filter(group__id=self.kwargs.get('pk')).exists():
            global_permissions_queryset = Permission.objects.filter(group__id=self.kwargs.get('pk')).order_by('-id')
        else:
            global_permissions_queryset = Permission.objects.none()
        context['global_permissions_qs_count'] = len(global_permissions_queryset)
        # Добавляем пагинатор.
        global_permissions_paginator = Paginator(global_permissions_queryset, 6)
        global_permissions_page_number = self.request.GET.get('global_permissions_page')
        global_permissions_page_obj = global_permissions_paginator.get_page(global_permissions_page_number)

        # Добавляем во вью.
        context['global_permissions_page_obj'] = global_permissions_page_obj
        context['group_object_permissions_filter'] = group_object_permissions_filter
        context['group_object_permissions_page_obj'] = group_object_permissions_page_obj

        # Возвращаем новый набор переменных.
        return context

# Создание категории.
class GroupCreateView(GPermissionRequiredMixin, CreateView):
    # Права доступа
    permission_required = 'core.add_employeesgroup'
    # Форма.
    form_class = GroupForm
    # Модель.
    model = EmployeesGroup
    # Шаблон.
    template_name = 'group_edit.html'

    # Заполнение полей данными.
    def get_initial(self):
        # Забираем изначальный набор.
        initial = super().get_initial()
        # Добавляем создателя: юзера отправившего запрос.
        initial["creator"] = self.request.user
        # Добавляем тип.
        initial["type"] = 'custom'
        # Возвращаем значения в форму.
        return initial

    # Перенаправление после валидации формы.
    def get_success_url(self):
        # Направляем по адресу объекта.
        return reverse('core:group', kwargs={'pk': self.object.pk})

# Изменение категории.
class GroupUpdateView(PermissionRequiredMixin, UpdateView):
    # Права доступа.
    permission_required = 'core.change_employeesgroup'
    accept_global_perms = True
    # Форма.
    form_class = GroupForm
    # Модель.
    model = EmployeesGroup
    # Шаблон.
    template_name = 'group_edit.html'

    # Проверяем права.
    def dispatch(self, request, *args, **kwargs):

        # Забираем группу.
        group = self.get_object()

        # Если имеется полное разрешение.
        if group.type == 'custom':

            # Идем дальше.
            return super().dispatch(request, *args, **kwargs)

        else:

            # Запрет.
            return HttpResponseForbidden('Нельзя менять группы такого типа!')

    # Заполнение полей данными.
    def get_initial(self):
        # Забираем изначальный набор.
        initial = super().get_initial()
        # Добавляем создателя: юзера отправившего запрос.
        initial["creator"] = self.request.user
        # Добавляем тип.
        initial["type"] = self.object.type
        # Возвращаем значения в форму.
        return initial

    # Перенаправление после валидации формы.
    def get_success_url(self):
        # Направляем по адресу объекта.
        return reverse('core:group', kwargs={'pk': self.object.pk})

# Удаление категории.
class GroupDeleteView(PermissionRequiredMixin, DeleteView):
    # Права доступа.
    permission_required = 'core.delete_employeesgroup'
    accept_global_perms = True
    # Модель.
    model = EmployeesGroup
    # Шаблон.
    template_name = 'group_delete.html'

    # Проверяем права.
    def dispatch(self, request, *args, **kwargs):

        # Забираем группу.
        group = self.get_object()

        # Если имеется полное разрешение.
        if group.type == 'custom':

            # Идем дальше.
            return super().dispatch(request, *args, **kwargs)

        else:

            # Запрет.
            return HttpResponseForbidden('Нельзя удалять группы такого типа!')

    # Перенаправление после валидации формы.
    def get_success_url(self):
        # Направляем по адресу объектов.
        return reverse('core:groups')

# Создание категории.
class GroupsGeneratorCreateView(GPermissionRequiredMixin, CreateView):
    # Права доступа.
    permission_required = 'core.add_employeesgroup'
    # Форма.
    form_class = GroupsGeneratorForm
    # Модель.
    model = GroupsGenerator
    # Шаблон.
    template_name = 'groups_generator_edit.html'

    # Определяем объект проверки.
    def get_permission_object(self):
        group = EmployeesGroup.objects.get(pk=self.kwargs.get('pk'))
        return group

    # Заполнение полей данными.
    def get_initial(self):
        # Забираем изначальный набор.
        initial = super().get_initial()
        # Добавляем создателя: юзера отправившего запрос.
        initial["creator"] = self.request.user
        # Добавляем группу из которой создан генератор.
        group = self.get_permission_object()
        initial["group"] = group
        # Возвращаем значения в форму.
        return initial

    # Валидация формы.
    def form_valid(self, form):
        # Сохраняем объект без коммита.
        self.object = form.save(commit=False)
        # Сохраняем объект в базу данных.
        self.object.save()

        # Логируем информацию об объекте после сохранения.
        if settings.DEBUG:
            logger.info(f"Объект после сохранения: {self.object}")
            logger.info(f"Поля объекта после сохранения: {vars(self.object)}")

        # Сохраняем связи.
        form.save_m2m()

        # Логируем информацию о связанных объектах.
        if settings.DEBUG:
            for related_object in form.cleaned_data:
                logger.info(f"Связанный объект: {related_object}")
                logger.info(f"Значение: {form.cleaned_data[related_object]}")

        # Вызываем базовую реализацию для дальнейшей обработки.
        return super(GroupsGeneratorCreateView, self).form_valid(form)

    # Перенаправление после валидации формы.
    def get_success_url(self):
        # Направляем по адресу объекта.
        return reverse('core:group', kwargs={'pk': self.object.group.pk})

# Изменение категории.
class GroupsGeneratorUpdateView(PermissionRequiredMixin, UpdateView):
    # Права доступа.
    permission_required = 'core.change_employeesgroup'
    accept_global_perms = True
    # Форма.
    form_class = GroupsGeneratorForm
    # Модель.
    model = GroupsGenerator
    # Шаблон.
    template_name = 'groups_generator_edit.html'

    # Определяем объект проверки.
    def get_permission_object(self):
        group = self.get_object().group
        return group

    # Заполнение полей данными.
    def get_initial(self):
        # Забираем изначальный набор.
        initial = super().get_initial()
        # Добавляем создателя: юзера отправившего запрос.
        initial["creator"] = self.request.user
        # Добавляем даты.
        if self.object.start_date_lte:
            initial["start_date_lte"] = self.object.start_date_lte.strftime('%Y-%m-%d')
        if self.object.start_date_gte:
            initial["start_date_gte"] = self.object.start_date_gte.strftime('%Y-%m-%d')
        # Возвращаем значения в форму.
        return initial

    # Валидация формы.
    def form_valid(self, form):
        # Сохраняем объект без коммита.
        self.object = form.save(commit=False)
        # Сохраняем объект в базу данных.
        self.object.save()

        # Логируем информацию об объекте после сохранения.
        if settings.DEBUG:
            logger.info(f"Объект после сохранения: {self.object}")
            logger.info(f"Поля объекта после сохранения: {vars(self.object)}")

        # Сохраняем связи.
        form.save_m2m()

        # Логируем информацию о связанных объектах.
        if settings.DEBUG:
            for related_object in form.cleaned_data:
                logger.info(f"Связанный объект: {related_object}")
                logger.info(f"Значение: {form.cleaned_data[related_object]}")

        # Вызываем базовую реализацию для дальнейшей обработки.
        return super(GroupsGeneratorUpdateView, self).form_valid(form)

    # Перенаправление после валидации формы.
    def get_success_url(self):
        # Направляем по адресу объекта.
        return reverse('core:group', kwargs={'pk': self.object.group.pk})

# Создание права на объект.
class EmployeesGroupObjectPermissionCreateView(GPermissionRequiredMixin, CreateView):
    # Права доступа
    permission_required = 'core.add_employeesgroupobjectpermission'
    # Форма.
    form_class = EmployeesGroupObjectPermissionForm
    # Модель.
    model = EmployeesGroupObjectPermission
    # Шаблон.
    template_name = 'employees_group_object_permission_edit.html'

    # Добавляем в форму аргументы.
    def get_form_kwargs(self):
        kwargs = super(EmployeesGroupObjectPermissionCreateView, self).get_form_kwargs()
        kwargs['type'] = self.kwargs.get('type')
        return kwargs

    # Заполнение полей данными.
    def get_initial(self):
        # Забираем изначальный набор.
        initial = super().get_initial()
        # Добавляем создателя: юзера отправившего запрос.
        initial["creator"] = self.request.user
        # Добавляем тип контента.
        if self.kwargs.get('type') == 'material':
            content_type = ContentType.objects.get_for_model(Material)
        elif self.kwargs.get('type') == 'course':
            content_type = ContentType.objects.get_for_model(Course)
        elif self.kwargs.get('type') == 'test':
            content_type = ContentType.objects.get_for_model(Test)
        elif self.kwargs.get('type') == 'event':
            content_type = ContentType.objects.get_for_model(Event)
        initial["content_type"] = content_type
        initial["object_pk"] = self.kwargs.get('pk')
        # Возвращаем значения в форму.
        return initial

    # Перенаправление после валидации формы.
    def get_success_url(self):
        # Направляем по адресу объекта.
        if self.kwargs.get('type') == 'material':
            return reverse('materials:material', kwargs={'pk': self.kwargs.get('pk')})
        elif self.kwargs.get('type') == 'course':
            return reverse('courses:course', kwargs={'pk': self.kwargs.get('pk')})
        elif self.kwargs.get('type') == 'test':
            return reverse('tests:test', kwargs={'pk': self.kwargs.get('pk')})
        elif self.kwargs.get('type') == 'event':
            return reverse('events:event', kwargs={'pk': self.kwargs.get('pk')})


# Удаление права на объект.
class EmployeesGroupObjectPermissionDeleteView(PermissionRequiredMixin, DeleteView):
    # Права доступа.
    permission_required = 'core.delete_employeesgroupobjectpermission'
    accept_global_perms = True
    # Модель.
    model = EmployeesGroupObjectPermission
    # Шаблон.
    template_name = 'employees_group_object_permission_delete.html'
    # Название параметра pk в urls
    pk_url_kwarg = 'employees_group_object_permission_pk'

    # Перенаправление после валидации формы.
    def get_success_url(self):
        # Направляем по адресу объекта.
        if self.kwargs.get('type') == 'material':
            return reverse('materials:material', kwargs={'pk': self.kwargs.get('pk')})
        elif self.kwargs.get('type') == 'course':
            return reverse('courses:course', kwargs={'pk': self.kwargs.get('pk')})
        elif self.kwargs.get('type') == 'test':
            return reverse('tests:test', kwargs={'pk': self.kwargs.get('pk')})
        elif self.kwargs.get('type') == 'event':
            return reverse('events:event', kwargs={'pk': self.kwargs.get('pk')})
        elif self.kwargs.get('type') == 'group':
            return reverse('core:group', kwargs={'pk': self.kwargs.get('pk')})

# Домашняя.
def home (request):
    # Сохраняем полный URL предыдущей страницы в сессии при каждом запросе.
    previous_page = request.get_full_path()
    request.session['previous_page_l1'] = previous_page
    print("Previous page l1 set to:", previous_page)
    # Забираем юзера и его результаты.
    employee = request.user
    if employee.is_authenticated:

        # Подзапрос информеров.
        latest_paths_results = employee.results.filter(
            learning_path=OuterRef('learning_path'),
            type='learning_path',
            employee=request.user
        ).order_by('-id').values('id')[:1]

        # Основной запрос информеров.
        employees_paths_results = employee.results.filter(
            id__in=Subquery(latest_paths_results)
        ).prefetch_related('learning_path')

        # Забираем траектории юзера.
        appointed_paths_count = employees_paths_results.filter(
            status='appointed',
        ).count()
        paths_in_progress_count = employees_paths_results.filter(
            status='in_progress',
        ).count()
        completed_paths_count = employees_paths_results.filter(
            status='completed',
        ).count()
        failed_paths_count = employees_paths_results.filter(
            status='failed',
        ).count()

        # Запрос учебных задач.
        employees_results = employee.results.filter(
            employee=request.user
        ).order_by('-event__date', '-planned_end_date', '-id')
        appointed_education = employees_results.filter(
            status='appointed',
        )
        appointed_education_count = appointed_education.count()
        appointed_education_paginator = Paginator(appointed_education, 6)
        appointed_education_page_number = request.GET.get('appointed_education_page')
        appointed_education_page_obj = appointed_education_paginator.get_page(appointed_education_page_number)
        education_in_progress = employees_results.filter(
            status='in_progress',
        )
        education_in_progress_count = education_in_progress.count()
        education_in_progress_paginator = Paginator(education_in_progress, 6)
        education_in_progress_page_number = request.GET.get('education_in_progress_page')
        education_in_progress_page_obj = education_in_progress_paginator.get_page(education_in_progress_page_number)
        completed_education = employees_results.filter(
            status='completed',
        )
        completed_education_count = completed_education.count()
        completed_education_paginator = Paginator(completed_education, 6)
        completed_education_page_number = request.GET.get('completed_education_page')
        completed_education_page_obj = completed_education_paginator.get_page(completed_education_page_number)
        failed_education = employees_results.filter(
            status='failed',
        )
        failed_education_count = failed_education.count()
        failed_education_paginator = Paginator(failed_education, 6)
        failed_education_page_number = request.GET.get('failed_education_page')
        failed_education_page_obj = failed_education_paginator.get_page(failed_education_page_number)

        # Отдаем контекст.
        context = {
            'employee': employee,
            'appointed_paths_count': appointed_paths_count,
            'paths_in_progress_count': paths_in_progress_count,
            'completed_paths_count': completed_paths_count,
            'failed_paths_count': failed_paths_count,
            'appointed_education_count': appointed_education_count,
            'education_in_progress_count': education_in_progress_count,
            'completed_education_count': completed_education_count,
            'failed_education_count': failed_education_count,
            'appointed_education_page_obj': appointed_education_page_obj,
            'education_in_progress_page_obj': education_in_progress_page_obj,
            'completed_education_page_obj': completed_education_page_obj,
            'failed_education_page_obj': failed_education_page_obj,
        }

    else:

        # Отдаем контекст.
        context = {
            'employee': employee
        }

    return render(request, 'home.html', context)

