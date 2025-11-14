# 🚀 Инструкция по запуску проекта hac_

## 📋 Предварительные требования

- Docker и Docker Compose установлены
- Git установлен
- Редактор кода (VS Code рекомендуется)
- API ключи (OpenAI/Mistral/Flux) - опционально для начала

---

## ⚡ Быстрый старт (5 минут)

### 1. Клонирование репозитория
```bash
git clone https://github.com/Rafaildavar/-_-.git
cd "ХАКАТОН ДИЗАЙН"
```

### 2. Настройка переменных окружения
```bash
# Скопируйте пример файла
cp .env.example .env

# Откройте .env и добавьте ваши API ключи (если есть)
# Минимально необходимые:
# - TELEGRAM_BOT_TOKEN (для Telegram бота)
# - OPENAI_API_KEY или MISTRAL_API_KEY (для AI)
```

### 3. Запуск всех сервисов
```bash
docker-compose up -d
```

### 4. Проверка работы
- Backend API: http://localhost:8000/docs
- n8n: http://localhost:5678 (admin/admin)
- Frontend: http://localhost:3000 (после запуска)

---

## 🔧 Детальная настройка

### Backend (FastAPI)

#### Локальный запуск (без Docker)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Проверка работы
```bash
curl http://localhost:8000/health
# Должен вернуть: {"status": "healthy"}
```

#### Доступные эндпоинты
- `GET /` - главная страница API
- `GET /health` - проверка здоровья
- `GET /docs` - Swagger документация
- `POST /api/assistant` - диалог с AI
- `POST /api/schedule` - генерация расписания
- `POST /api/lesson` - генерация урока
- `POST /api/image` - генерация изображения
- `POST /api/tg/send` - отправка в Telegram
- `POST /api/n8n/webhook` - webhook для n8n

---

### Frontend (Next.js)

#### Установка зависимостей
```bash
cd frontend
npm install
# или
pnpm install
```

#### Запуск в режиме разработки
```bash
npm run dev
# или
pnpm dev
```

#### Сборка для продакшена
```bash
npm run build
npm start
```

#### Настройка shadcn/ui
```bash
npx shadcn-ui@latest init
```

---

### n8n

#### Доступ
- URL: http://localhost:5678
- Логин: admin (или из .env)
- Пароль: admin (или из .env)

#### Создание первого workflow

1. Нажмите "Add workflow"
2. Добавьте ноды:
   - **Webhook** (Trigger) - для входящих запросов
   - **HTTP Request** - для запросов к backend
   - **Telegram** - для отправки сообщений

3. Настройте Webhook:
   - Method: POST
   - Path: `/webhook/test`
   - Response Mode: "Using 'Respond to Webhook' Node"

4. Настройте HTTP Request:
   - Method: POST
   - URL: `http://backend:8000/api/assistant`
   - Body: JSON с полем `message`

5. Настройте Telegram:
   - Operation: Send Message
   - Chat ID: ваш chat_id
   - Message: `{{ $json.response }}`

#### Тестирование workflow
```bash
curl -X POST http://localhost:5678/webhook/test \
  -H "Content-Type: application/json" \
  -d '{"message": "Привет!"}'
```

---

### Telegram бот

#### Создание бота
1. Откройте @BotFather в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Скопируйте токен бота
5. Добавьте токен в `.env` файл: `TELEGRAM_BOT_TOKEN=ваш_токен`

#### Получение Chat ID
1. Откройте @userinfobot в Telegram
2. Отправьте `/start`
3. Скопируйте ваш Chat ID
4. Добавьте в `.env`: `TELEGRAM_CHAT_ID=ваш_chat_id`

#### Тестирование бота
```bash
# Через API
curl -X POST http://localhost:8000/api/tg/send \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Тестовое сообщение",
    "chat_id": "ваш_chat_id"
  }'
```

---

## 🐳 Docker команды

### Запуск
```bash
docker-compose up -d
```

### Остановка
```bash
docker-compose down
```

### Просмотр логов
```bash
# Все сервисы
docker-compose logs -f

# Конкретный сервис
docker-compose logs -f backend
docker-compose logs -f n8n
```

### Перезапуск сервиса
```bash
docker-compose restart backend
docker-compose restart n8n
```

### Очистка (удаление контейнеров и volumes)
```bash
docker-compose down -v
```

---

## 🔑 Настройка API ключей

### OpenAI
1. Зарегистрируйтесь на https://platform.openai.com
2. Создайте API ключ
3. Добавьте в `.env`: `OPENAI_API_KEY=sk-...`

### Mistral
1. Зарегистрируйтесь на https://mistral.ai
2. Получите API ключ
3. Добавьте в `.env`: `MISTRAL_API_KEY=...`

### Flux (для изображений)
1. Зарегистрируйтесь на https://blackforestlabs.ai
2. Получите API ключ
3. Добавьте в `.env`: `FLUX_API_KEY=...`

**Примечание:** Если API ключей нет, проект будет работать с заглушками для демо.

---

## 🧪 Тестирование

### Тест Backend API
```bash
# Health check
curl http://localhost:8000/health

# Assistant
curl -X POST http://localhost:8000/api/assistant \
  -H "Content-Type: application/json" \
  -d '{"message": "Привет, как дела?"}'

# Schedule
curl -X POST http://localhost:8000/api/schedule \
  -H "Content-Type: application/json" \
  -d '{
    "subjects": ["Математика", "Физика"],
    "hours_per_week": 10
  }'
```

### Тест Frontend
1. Откройте http://localhost:3000
2. Проверьте все страницы
3. Протестируйте формы

### Тест n8n
1. Откройте http://localhost:5678
2. Создайте тестовый workflow
3. Активируйте его
4. Отправьте тестовый запрос

---

## 🐛 Решение проблем

### Порт занят
```bash
# Проверьте, что занимает порт
lsof -i :8000
lsof -i :5678
lsof -i :3000

# Измените порты в docker-compose.yml
```

### Docker не запускается
```bash
# Проверьте статус Docker
docker ps

# Перезапустите Docker
# macOS: перезапустите Docker Desktop
```

### Зависимости не устанавливаются
```bash
# Backend
cd backend
pip install --upgrade pip
pip install -r requirements.txt

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### n8n не открывается
```bash
# Проверьте логи
docker-compose logs n8n

# Перезапустите
docker-compose restart n8n
```

### API не отвечает
```bash
# Проверьте, что backend запущен
docker-compose ps

# Проверьте логи
docker-compose logs backend

# Проверьте .env файл
cat .env
```

---

## 📚 Полезные ссылки

- [FastAPI документация](https://fastapi.tiangolo.com/)
- [Next.js документация](https://nextjs.org/docs)
- [n8n документация](https://docs.n8n.io/)
- [shadcn/ui](https://ui.shadcn.com/)
- [TailwindCSS](https://tailwindcss.com/docs)

---

## 🎯 Следующие шаги

1. ✅ Запустите все сервисы
2. ✅ Проверьте работу API
3. ✅ Настройте Telegram бота
4. ✅ Создайте n8n workflows
5. ✅ Начните разработку фич

**Удачи на хакатоне! 🚀**

