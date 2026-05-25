# Secure Flask Lab

Учебный pet-проект на Flask: мини-лента постов с комментариями и лайками, с базовыми мерами защиты от SQL Injection и XSS.

## Возможности

- Регистрация / логин / логаут
- Лента постов с пагинацией
- Комментарии (AJAX)
- Лайки (toggle, AJAX)

## Технологии

* Python + Flask
* SQLite
* Flask-WTF (CSRF)
* Flask-Limiter (rate limiting)
* bcrypt

## Безопасность (что реализовано)

- Параметризованные SQL-запросы (`?`) для защиты от SQL Injection
- CSRF-защита для HTML-форм и AJAX
- Ограничение частоты запросов (rate limiting)
- Автоэкранирование шаблонов Jinja
- HTTP security headers:
  - `X-Frame-Options: DENY`
  - `X-Content-Type-Options: nosniff`
  - `Referrer-Policy: strict-origin-when-cross-origin`
  - базовый CSP

## Быстрый старт

1. Клонировать репозиторий
2. Создать и активировать virtualenv
3. Установить зависимости:
```bash
pip install -r requirements.txt
```
4. Создать.env
```env
SECRET_KEY=<your-strong-random-secret>
DEBUG=False
DATABASE=database.db
```
5. Инициализировать БД
```bash
python -m app.init_db
```
6. Запустить приложение
```bash
python run.py
```

## Production Notes

* Запуск только на HTTPS
* `SESSION_COOKIE_SECURE=True`
* Добавить HSTS (`Strict-Transport-Security`)
* Использовать сильный `SECRET_KEY` (не менее 32+ случайных символов)
* Настроить reverse proxy (nginx/traefik) с HTTP→HTTPS redirect
* Включить централизованные логи и мониторинг 4xx/5xx

## Security Roadmap

* Усилить Content Security Policy
* Добавить HSTS
* Снизить риск username enumeration
* Добавить автоматические security-тесты
* Рассмотреть миграцию на PostgreSQL и Alembic

## Disclaimer

Проект создан в учебных целях и демонстрирует базовые практики защиты веб-приложений. Перед использованием в production требуется дополнительный аудит и hardening.
