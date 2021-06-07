# CRUD для компании и ее новостей с правами пользователей

### Регистрация пользователя
- **POST**```/api/v1/registration/``` Регистрация, передать login и password

Тебования:
- login:
  - Максимум 150 символов.
  - Буквы, цифры и только @/./+/ -/_.
- password:
   - Не должен совпадать с вашим именем или другой персональной информацией или быть слишком похожим на неё.
   - Должен содержать как минимум 8 символов.
   - Не может быть одним из широко распространённых паролей.
   - Не может состоять только из цифр
  
  
### JSON компании
```
[
    {
        "id": 1,
        "name": "Nord Wings",
        "description": "Air company"
    }
]
```

### JSON новости
```
[
    {
        "id": 4,
        "author": "kitty",
        "company": "Nord Wings",
        "title": "Pay new plane",
        "text": "we are pay new plane in oure park",
        "pub_date": "2021-06-06T16:31:00.676552+03:00"
    },
]
```

### ENDPOINT
#### Компании
- **GET**```/api/v1/companies/```  Список всех компаний. Доступно всем пользователям
- **POST**```/api/v1/companies/``` Админ может создать новую компанию
- **GET**```/api/v1/companies/1/``` Просмотр компании с id=1. Просматривать подробную информацию о компании могут только сотрудники компании.
В подробной информации указываются все новости компании и количество сотрудников
```{   
    "id": 1,
    "news": [
        {
            "id": 4,
            "author": "kitty",
            "company": "Nord Wings",
            "title": "Pay new plane",
            "text": "we are pay new plane in oure park",
            "pub_date": "2021-06-06T16:31:00.676552+03:00"
        },
        {
            "id": 3,
            "author": "leo",
            "company": "Nord Wings",
            "title": "Летим и в европу",
            "text": "открыты полеты в европу",
            "pub_date": "2021-06-06T12:38:54.010113+03:00"
        }
    ],
    "amount_of_employees": 2,
    "name": "Nord Wings",
    "description": "Air company"
}
```
- **PUT**```/api/v1/companies/1/```  Администратор и Модератор могут редактировать свою компанию
- **DELETE**```/api/v1/companies/1/``` Администратор и Модератор могут удалить свою компанию
#### Новости
- **GET**```/api/v1/companies/1/news/```  Список всех новостей компании с id=1. Доступно всем пользователям
- **POST**```/api/v1/companies/1/news/``` Создать новую новость компании. Доступно Админу и сотруднику компании
- **GET**```/api/v1/companies/1/news/1/``` Просмотр новости с id=1, которая относится компании с id=1. Доступно всем пользователям

- **PUT**```/api/v1/companies/1/news/1/```  Администратор, Модератор и автор новости могут редактировать новость компании
- **DELETE**```/api/v1/companies/1/``` Администратор, Модератор и автор новости могут удалить новость компанию

#### Профиль (Доступно только Администратору)
```
[
    {
        "id": 3,
        "user": "kitty",
        "role": "user",
        "company": 1
    }
]
```
- **GET**```/api/v1/profiles/``` Просмотр всех профилей пользователей
- **POST**```/api/v1/profiles/``` Создать профиль, добавить пользователя в компанию. 
  Указать user, role('moderator', 'user'), company
- **PUT**```/api/v1/profiles/1/```  Редактировать профиль. Изменить роль пользователя и компанию
- **DELETE**```/api/v1/profiles/1/``` Удалить профиль


## Установка и запуск на сервере разработчика
1. Клонировать репозиторий
    ```
    git clone https://github.com/cement-hools/crud_company
    ```
2. Перейдите в директорию crud_company
    ```
   cd crud_company
    ```
3. Создать виртуальное окружение, активировать и установить зависимости
    ``` 
   python -m venv venv
    ```
   Варианты активации окружения:
   - windows ``` venv/Scripts/activate ```
   - linux ``` venv/bin/activate ```
     <br><br>
   ```
   python -m pip install -U pip
   ```
   ```
   pip install -r requirements.txt
   ```
4. Выполните миграции
   ```
   python manage.py migrate
   ```
5. Создать суперюзера
   ```
   python manage.py createsuperuser
   ```
6. Запустить приложение на сервере разработчика
   ```
   python manage.py runserver
   ```
7. Проект доступен 
   ```
   http://localhost:8000/
   ```

## Тесты
```
python manage.py test
```

## Запуск в трех контейнерах (PostgreSQL, Web, Nginx)

1. Клонировать репозиторий
    ```
    git clone https://github.com/cement-hools/crud_company
    ```
2. Перейдите в директорию crud_company
    ```
   cd crud_company
    ```
3. Запустить docker-compose
    ```
    docker-compose up --build
    ```
4. Зайти в контейнер и выполнить миграции
    ```
    docker-compose exec web python manage.py migrate --noinput
    ```
5. Зайти в контейнер и создать суперюзера. Указать username, email, password
    ```
    docker-compose exec web python manage.py createsuperuser
    ```
7. Проект доступен 
   ```
   http://127.0.0.1/
   ```
