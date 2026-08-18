<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&height=250&color=8B5CF6&customColorList=12,14,18,20,24&text=NextRoom&fontColor=ffffff&fontSize=70&fontAlignY=40&descAlignY=65&descSize=24&animation=twinkling&section=header" width="100%" /> 
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=24&duration=2800&pause=1000&color=A855F7&background=0D111700&center=true&vCenter=true&width=850&lines=NextRoom+-+Real-Time+AI-Powered+Chat+Platform;Multi-LLM+Orchestration+%7C+Image+Generation+%7C+Mini-Games;Powered+by+Django+5%2C+PostgreSQL+16+%26+TailwindCSS;Cryptographic+Security+%26+Modular+AI+Routing" alt="Animated Banner" />
</p>


<p align="center">
  <img src="https://api.visitorbadge.io/api/visitors?path=X2X13211.NextRoom&label=VIEWS&labelColor=555555&countColor=8B5CF6&style=for-the-badge" alt="Views" />
  <img src="https://img.shields.io/github/stars/X2X13211/NextRoom?style=for-the-badge&color=8B5CF6" alt="Stars" />
  <img src="https://img.shields.io/github/forks/X2X13211/NextRoom?style=for-the-badge&color=8B5CF6" alt="Forks" />
  <img src="https://img.shields.io/github/issues/X2X13211/NextRoom?style=for-the-badge&color=8B5CF6" alt="Issues" />
  <img src="https://img.shields.io/github/license/X2X13211/NextRoom?style=for-the-badge&color=8B5CF6" alt="License" />
  <img src="https://img.shields.io/github/last-commit/X2X13211/NextRoom?style=for-the-badge&color=8B5CF6" alt="Last Commit" />
  <img src="https://img.shields.io/github/repo-size/X2X13211/NextRoom?style=for-the-badge&color=8B5CF6" alt="Repo Size" />
</p>

<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=python,django,postgres,tailwind,js,docker,linux,git,html,css,postman,redis" alt="Tech Stack Icons" />
  </a>
</p>

<p align="center">
  <a href="https://nextroom.vercel.app">
    <img 
      src="https://img.shields.io/badge/ОТКРЫТЬ_ПРИЛОЖЕНИЕ_NEXTROOM-8B5CF6?style=for-the-badge&logo=vercel&logoColor=white&labelColor=6D28D9" 
      alt="Открыть приложение NextRoom" 
      height="46" 
      />
  </a>
</p>

## <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Rocket.svg" width="24" height="24" valign="middle" /> Обзор платформы

**NextRoom** — это многофункциональная веб-платформа реального времени для групповой и приватной коммуникации, объединяющая возможности современных мессенджеров, гибкую организацию пространств по интересам и прямое взаимодействие с передовыми большими языковыми моделями (LLM) и генераторами медиа.

Проект спроектирован для обеспечения комфортного командного взаимодействия, образовательных дискуссий, проведения интеллектуальных мини-игр и генерации медиаконтента в едином бесшовном интерфейсе с адаптивным дизайном и аппаратным шифрованием приватных данных.

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=18&duration=2000&pause=800&color=9333EA&center=true&vCenter=true&width=750&lines=21%2B+Thematic+Categories;Multi-Provider+AI+Hub+(RouterAI%2C+Groq%2C+OpenRouter);Interactive+AI+Mini-Games+%26+Simulators;AI+Image+Generation+Studio" alt="Features subtitle" />
</p>

## <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/FastAPI.svg" width="24" height="24" valign="middle" /> Архитектура системы

```mermaid
flowchart TD
    classDef client fill:#8B5CF6,stroke:#7C3AED,stroke-width:2px,color:#ffffff,font-weight:bold;
    classDef router fill:#3B82F6,stroke:#1D4ED8,stroke-width:2px,color:#ffffff,font-weight:bold;
    classDef engine fill:#1E1B4B,stroke:#6366F1,stroke-width:2px,color:#E0E7FF;
    classDef ai fill:#581C87,stroke:#A855F7,stroke-width:2px,color:#F3E8FF,font-weight:bold;
    classDef db fill:#064E3B,stroke:#10B981,stroke-width:2px,color:#ECFDF5,font-weight:bold;

    Client["Frontend UI (TailwindCSS, Vanilla JS, Lottie Web Player)"]:::client
    
    subgraph CoreEngine ["Server Framework (Django 5.x)"]
        Router["Router & Middleware (Rate Limiting, Session, IPWare)"]:::router
        ChatEngine["Rooms, Messages & Reactions Engine"]:::engine
        AIEngine["AI Orchestrator (Key Encryption, Provider Routing)"]:::engine
        GameEngine["Game Module (Movie Game & Hints)"]:::engine
        BillingEngine["Billing & YooKassa API Gateway"]:::engine
        AchievementsEngine["Achievements, Rewards & Streaks"]:::engine
        CacheLayer["Multi-level Cache (Cache Utils)"]:::engine
    end
    
    subgraph AIProviders ["AI Providers & Models"]
        RouterAI["RouterAI API (DeepSeek, Qwen, GLM, GPT-OSS)"]:::ai
        GroqCerebras["Groq & Cerebras (LPU Ultra-Low Latency)"]:::ai
        Cloro["Cloro Gemini Gateway"]:::ai
        OpenRouter["OpenRouter Auto Beta"]:::ai
    end
    
    subgraph DataStorage ["Data Storage Layer"]
        PostgresDB[(PostgreSQL 16 / SQLite)]:::db
        MediaStorage[(Media Storage / File Storage)]:::db
    end

    Client <--> Router
    Router --> ChatEngine
    Router --> AIEngine
    Router --> GameEngine
    Router --> BillingEngine
    Router --> AchievementsEngine
    
    AIEngine <--> RouterAI
    AIEngine <--> GroqCerebras
    AIEngine <--> Cloro
    AIEngine <--> OpenRouter
    
    ChatEngine <--> CacheLayer
    ChatEngine --> PostgresDB
    ChatEngine --> MediaStorage
    AIEngine --> PostgresDB
    AchievementsEngine --> PostgresDB
    BillingEngine --> PostgresDB
```

## <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/PostgreSQL-Dark.svg" width="24" height="24" valign="middle" /> Модели данных и связи (Entity-Relationship)

```mermaid
erDiagram
    USER ||--o{ USER_PROFILE : "has profile (1:1)"
    USER ||--o{ ROOM : "creates rooms"
    USER ||--o{ MESSAGE : "sends messages"
    USER ||--o{ MESSAGE_REACTION : "adds reactions"
    USER ||--o{ USER_ACHIEVEMENT : "unlocks achievements"
    USER ||--o{ USER_ACTIVITY : "logs activity"
    USER ||--o{ ROUTERAI_KEY : "generates API keys"
    USER ||--o{ PAYMENT : "makes payments"

    ROOM ||--o{ MESSAGE : "stores history"
    ROOM ||--o{ ROOM_AI_INTEGRATION : "attaches AI models"
    ROOM ||--o{ ROOM_INVITATION : "contains invite links"
    ROOM ||--o{ MOVIE_GAME : "hosts game sessions"

    USER_PROFILE ||--o{ AI_INTEGRATION : "configures providers"
    USER_PROFILE ||--o{ AI_USAGE_LOG : "tracks token usage"
    USER_PROFILE ||--o{ GENERATED_IMAGE : "saves AI artwork"

    GUEST_SESSION ||--o{ MESSAGE : "guest messages"
    GUEST_SESSION ||--o{ GENERATED_IMAGE : "guest generations"

    USER {
        int id PK
        string username
        string email
        boolean is_premium
    }
    ROOM {
        int id PK
        string title
        string category
        boolean is_private
    }
    MESSAGE {
        int id PK
        text content
        datetime created_at
        boolean is_ai
    }
    AI_INTEGRATION {
        int id PK
        string provider
        string model_name
        text system_prompt
    }
```

## <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/GraphQL-Dark.svg" width="24" height="24" valign="middle" /> Функциональные возможности

### 1. Пространства для общения и управление комнатами
- **Тематическая категоризация**: 21 предустановленная категория (Технологии, ИИ, Программирование, Учеба, Наука, Книги, Аниме, Спорт, Новости, Юмор, Творчество, Дизайн, Бизнес, Стартапы, Путешествия, Языки, Игры, Фильмы, Музыка, Социальное).
- **Публичные и защищенные комнаты**: Свободный вход или закрытый доступ по секретному коду.
- **Инвайты**: Генерация криптографически стойких токенов доступа (`secrets.token_urlsafe`).
- **Закрепление комнат**: Механизм закрепления приоритетных комнат вверху списка дашборда.
- **Аналитика**: Отслеживание счетчиков сообщений, активных пользователей и AI-трафика.

### 2. Мультипровайдерная интеграция искусственного интеллекта
- **Контекстный вызов**: Обращение к моделям через команды в чате (`@gpt`, `@claude`, `@deepseek`, `@routerai`, `@groq` или кастомный никнейм модели).
- **Режим Auto-Reply**: Автоматический ответ модели на каждое сообщение в пространстве.
- **Кастомные промпты**: Персональные системные инструкции для каждой модели с определением тона, роли и правил форматирования.
- **Управление API-ключами**: Генерация, хеширование, валидация и отключение персональных ключей RouterAI.
- **Мониторинг расходов**: Подсчет использованных токенов, задержки ответа и построение аналитических графиков.

### 3. Студия генерации изображений и медиа
- **Выделенный интерфейс `/image-chat/`**: Генерация графики по текстовым описаниям с сохранением в историю.
- **Журнал артов**: Хранение параметров промпта, размеров, времени рендеринга и использованной модели.
- **Голосовые и медиасообщения**: Отправка аудиофайлов, изображений и автоматическое распознавание внешних графических ссылок.

### 4. Интерактивные мини-игры и симуляторы
- **Игра «Угадай фильм»**: Сессионная викторина с выдачей подсказок, валидацией ответов и фиксацией побед.
- **Фоновые боты**: Симуляторы собеседников с уникальными характерами и динамикой споров для тестирования активности.

### 5. Геймификация и система наград
- **Достижения с Lottie-анимациями**: Награды за регистрацию, количество отправленных сообщений (10, 100, 1000), создание комнат, инвайты и стрики.
- **Бонусный Premium**: Автоматическое продление Premium-подписки за выполнение целевых действий.
- **Трекер стриков**: Валидация непрерывной ежедневной активности пользователей.

## <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/CSS.svg" width="24" height="24" valign="middle" /> Пользовательский интерфейс

<table align="center">
<tr>

<td align="center" width="33%" valign="top">
  <p align="center"><b>Главный экран</b></p>
  <a href="https://github.com/user-attachments/assets/bec2ac00-fc64-4b0a-bec0-fbef639bb914">
    <img width="360" src="https://github.com/user-attachments/assets/bec2ac00-fc64-4b0a-bec0-fbef639bb914" alt="Главная страница NextRoom" />
  </a>
  <p align="center"><img src="https://img.shields.io/badge/Обзор-8B5CF6?style=flat-square" /></p>
  <a href="https://github.com/user-attachments/assets/3b22ab9f-ed2b-47bf-943b-2dfed0fd22e7">
    <img width="360" src="https://github.com/user-attachments/assets/3b22ab9f-ed2b-47bf-943b-2dfed0fd22e7" alt="Панель управления" />
  </a>
  <p align="center"><img src="https://img.shields.io/badge/Лента-8B5CF6?style=flat-square" /></p>
  <a href="https://github.com/user-attachments/assets/04e590b6-fedc-42d5-8762-dcfae5da4d11">
    <img width="360" src="https://github.com/user-attachments/assets/04e590b6-fedc-42d5-8762-dcfae5da4d11" alt="Информация" />
  </a>
</td>

<td align="center" width="33%" valign="top">
  <p align="center"><b>Комнаты и Чат</b></p>
  <a href="https://github.com/user-attachments/assets/cd7e9466-a7a5-44fe-a7b4-6eae507dc828">
    <img width="360" src="https://github.com/user-attachments/assets/cd7e9466-a7a5-44fe-a7b4-6eae507dc828" alt="Комнаты NextRoom" />
  </a>
  <p align="center"><img src="https://img.shields.io/badge/Чат-8B5CF6?style=flat-square" /></p>
  <a href="https://github.com/user-attachments/assets/cc91efc6-477c-4cf3-9a77-5d97813781be">
    <img width="360" src="https://github.com/user-attachments/assets/cc91efc6-477c-4cf3-9a77-5d97813781be" alt="Чат" />
  </a>
  <p align="center"><img src="https://img.shields.io/badge/Диалог_с_ИИ-8B5CF6?style=flat-square" /></p>
  <a href="https://github.com/user-attachments/assets/54ca41e1-58c4-4e0b-8e35-16dbb0a7398c">
    <img width="360" src="https://github.com/user-attachments/assets/54ca41e1-58c4-4e0b-8e35-16dbb0a7398c" alt="Диалог с ИИ" />
  </a>
  <p align="center"><img src="https://img.shields.io/badge/Возможности-8B5CF6?style=flat-square" /></p>
  <a href="https://github.com/user-attachments/assets/29e9fb2c-3b88-4ce2-998a-1c04e38fd029">
    <img width="360" src="https://github.com/user-attachments/assets/29e9fb2c-3b88-4ce2-998a-1c04e38fd029" alt="Функции комнат" />
  </a>
</td>

<td align="center" width="33%" valign="top">
  <p align="center"><b>Профиль и Настройки</b></p>
  <a href="https://github.com/user-attachments/assets/0baad315-b5de-48ef-9812-e37623f02985">
    <img width="360" src="https://github.com/user-attachments/assets/0baad315-b5de-48ef-9812-e37623f02985" alt="Профиль пользователя" />
  </a>
  <p align="center"><img src="https://img.shields.io/badge/Настройки-8B5CF6?style=flat-square" /></p>
  <a href="https://github.com/user-attachments/assets/a7a250ea-9d45-4038-a82c-84d168bcde05">
    <img width="360" src="https://github.com/user-attachments/assets/a7a250ea-9d45-4038-a82c-84d168bcde05" alt="Настройки профиля" />
  </a>
  <p align="center"><img src="https://img.shields.io/badge/Аналитика-8B5CF6?style=flat-square" /></p>
  <a href="https://github.com/user-attachments/assets/6b5e9e1b-06a1-46ea-abbe-0b3cabb692e4">
    <img width="360" src="https://github.com/user-attachments/assets/6b5e9e1b-06a1-46ea-abbe-0b3cabb692e4" alt="Аналитика" />
  </a>
</td>

</tr>
</table>

## Каталог поддерживаемых AI-моделей

Платформа поддерживает гибкий мультипровайдерный хаб, включающий в себя новейшие открытые и проприетарные языковые модели, а также специализированные диффузионные генераторы изображений:

### Большие языковые модели (LLM & Мультимодальность)

| Модель | Провайдер | Контекст | Назначение и особенности |
| :--- | :--- | :--- | :--- |
| <img src="https://assets.routerai.ru/assets/icons/deepseek-9896b5f6.svg" width="18" height="18" valign="middle" /> **DeepSeek V4 Flash (0731)** | RouterAI | 1M токенов | MoE-архитектура (13B активных из 284B). Высокая скорость в кодинге, рассуждениях и агентных пайплайнах |
| <img src="https://assets.routerai.ru/assets/icons/deepseek-9896b5f6.svg" width="18" height="18" valign="middle" /> **DeepSeek V4 Pro** | RouterAI | 1M токенов | Флагманская MoE-модель (1.6T общих / 49B активных параметров) для сложнейшего комплексного анализа |
| <img src="https://assets.routerai.ru/assets/icons/qwen-826a8925.png" width="18" height="18" valign="middle" /> **Qwen 3.5 (9B)** | RouterAI | 262K токенов | Мультимодальная базовая модель для точного распознавания изображений, текста и логических задач |
| <img src="https://assets.routerai.ru/assets/icons/qwen-826a8925.png" width="18" height="18" valign="middle" /> **Qwen 3.5 Flash** | RouterAI | 1M токенов | Нативная Vision-Language модель с гибридным линейным вниманием и MoE для сверхбыстрых ответов |
| <img src="https://assets.routerai.ru/assets/icons/z-ai-f9c74318.png" width="18" height="18" valign="middle" /> **GLM 4.7 Flash** | RouterAI / Cerebras | 203K токенов | Оптимизирована под агентное кодирование, долгосрочное планирование и глубокое сотрудничество с API |
| <img src="https://assets.routerai.ru/assets/icons/google-80717409.svg" width="18" height="18" valign="middle" /> **Gemma 4 (31B Instruct)** | RouterAI / Cerebras | 262K токенов | Плотная мультимодальная модель от Google DeepMind с поддержкой 140+ языков и function calling |
| <img src="https://assets.routerai.ru/assets/icons/google-80717409.svg" width="18" height="18" valign="middle" /> **Gemini 2.5 Flash Lite** | RouterAI | 1M токенов | Ультранизкая задержка, быстрый стриминг токенов и настраиваемый уровень глубины рассуждений |
| <img src="https://api.iconify.design/logos:openai-icon.svg" width="18" height="18" valign="middle" /> **OpenAI GPT-OSS (120B)** | RouterAI / Groq / Cerebras | 131K токенов | Открытые веса MoE от OpenAI (117B параметров) для сложных логических рассуждений и структурированного вывода |
| <img src="https://api.iconify.design/logos:openai-icon.svg" width="18" height="18" valign="middle" /> **OpenAI GPT-OSS (20B)** | RouterAI / Groq / Cerebras | 131K токенов | Компактная быстрая модель в формате ответов Harmony с поддержкой вызова функций и инструментов |
| <img src="https://api.iconify.design/logos:openai-icon.svg" width="18" height="18" valign="middle" /> **OpenAI GPT-OSS Safeguard 20B** | RouterAI / Groq | 131K токенов | Модель безопасности и модерации для задач фильтрации, классификации и контроля контекста |
| <img src="https://cdn.simpleicons.org/meta/0668E1" width="18" height="18" valign="middle" /> **Llama 3.3 (70B Versatile)** | Groq | 128K токенов | Мощная открытая модель Meta с аппаратным ускорением инференса на чипах Groq LPU |
| <img src="https://cdn.simpleicons.org/meta/0668E1" width="18" height="18" valign="middle" /> **Llama 3.1 (8B Instant)** | Groq | 128K токенов | Мгновенный отклик для интерактивных текстовых сценариев, диалогов и экспресс-генерации |
| <img src="https://cdn.simpleicons.org/meta/0668E1" width="18" height="18" valign="middle" /> **Meta Llama Prompt Guard 2** | Groq | 128K токенов | Специализированные фильтры безопасности (22M / 86M) для защиты от prompt injection и атак |
| <img src="https://raw.githubusercontent.com/lobehub/lobe-icons/master/packages/static-svg/icons/openrouter.svg" width="18" height="18" valign="middle" /> **OpenRouter Auto Beta** | OpenRouter | 1M токенов | Динамическая авто-маршрутизация запросов к наиболее подходящей и доступной модели сети |
| <img src="https://raw.githubusercontent.com/lobehub/lobe-icons/master/packages/static-svg/icons/groq.svg" width="18" height="18" valign="middle" /> **Groq Auto** | Groq | 128K токенов | Автоматический выбор доступной модели на платформе аппаратных ускорителей Groq |
| <img src="https://raw.githubusercontent.com/lobehub/lobe-icons/master/packages/static-svg/icons/cerebras.svg" width="18" height="18" valign="middle" /> **Cerebras Auto** | Cerebras | 128K токенов | Интеллектуальный балансировщик задач на суперкомпьютерной архитектуре Cerebras WSE |

### Модели генерации и обработки изображений (AI Image Studio)

| Модель | Провайдер | Стоимость | Разрешение / Особенности |
| :--- | :--- | :--- | :--- |
| <img src="https://cdn.simpleicons.org/artstation/13AFF0" width="18" height="18" valign="middle" /> **Krea 2 Medium Turbo** | RouterAI | 3.00 ₽ / фото | Высококачественная быстрая генерация и гибкая обработка изображений (Image-to-Image) |
| <img src="https://cdn.simpleicons.org/sourcetree/0052CC" width="18" height="18" valign="middle" /> **Riverflow V2.5 Fast** | RouterAI | 4.25 ₽ / фото | Генерация ультрачетких изображений в разрешении 2K с поддержкой визуальных референсов |
| <img src="https://cdn.simpleicons.org/x/cbd5e1" width="18" height="18" valign="middle" /> **SpaceXAI: Grok Imagine** | RouterAI | 8.00 ₽ / фото | Модель генерации от xAI (1K) с глубоким контекстным пониманием сложных креативных промптов |
| <img src="https://cdn.simpleicons.org/flux/fde047" width="18" height="18" valign="middle" /> **FLUX.2 Pro** | RouterAI | 5.50 ₽ / фото | SOTA фотореализм от Black Forest Labs с безупречной детализацией композиций и текстур |
| <img src="https://assets.routerai.ru/assets/icons/qwen-826a8925.png" width="18" height="18" valign="middle" /> **Qwen Image 3 Pro** | RouterAI | 6.30 ₽ / фото | Продвинутая модель генерации и трансформации изображений в высоком разрешении от Qwen |


## Сравнение тарифных планов

| Параметр | Free | Premium |
| :--- | :--- | :--- |
| **Лимит комнат** | До 5 комнат | До 30 комнат |
| **Лимит инвайт-ссылок** | До 10 приглашений | Неограниченно |
| **Доступ к LLM** | Базовые модели | Полный каталог (включая флагманские MoE модели) |
| **Генерация картинок** | Стандартный лимит | Расширенный лимит и приоритетная очередь |
| **Персональные промпты** | 1 глобальный промпт | Индивидуальные системные промпты под каждую модель |
| **Пополнение баланса** | Не требуется | Интеграция с ЮKassa (СБП, Карты, Mir Pay) |

## <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Git.svg" width="24" height="24" valign="middle" /> Структура репозитория

```mermaid
mindmap
  root((NextRoom Project))
    (chat App)
      (Схемы и Модели)
        models.py
        models_catalog.py
      (Контроллеры и API)
        views.py
        urls.py
      (Конфигурация ИИ)
        bot_prompts.py
        admin.py
      (Утилиты)
        cache_utils.py
      (Консольные команды)
        run_bots.py
        setup_bots.py
    (nextroom_project)
      (Конфигурация Django)
        settings.py
      (Маршрутизация)
        urls.py
      (Веб-интерфейсы)
        asgi.py
        wsgi.py
    (templates UI)
      (Лэйауты)
        base.html
      (Дашборд и Профиль)
        dashboard.html
        profile.html
      (Взаимодействие)
        room_detail.html
        image_chat.html
      (Управление)
        ai_management.html
        achievements.html
    (Конфиги и Скрипты)
      (Сборка)
        build.sh
        vercel.json
      (Зависимости)
        requirements.txt
        package.json
      (Стилизация)
        tailwind.config.js
```

## <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Bash-Dark.svg" width="24" height="24" valign="middle" /> Установка и запуск

<details>
<summary><b>Пошаговая инструкция по локальной установке</b></summary>

### 1. Клонирование репозитория
```bash
git clone https://github.com/X2X13211/NextRoom.git
cd NextRoom
```

### 2. Подготовка виртуального окружения
```bash
python -m venv venv
source venv/bin/activate  # Для Linux/macOS
# venv\Scripts\activate   # Для Windows
```

### 3. Установка пакетов
```bash
pip install -r requirements.txt
npm install
```

### 4. Конфигурация переменных (.env)
```env
SECRET_KEY=your_django_secret_key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/nextroom_db
FIELD_ENCRYPTION_KEY=your_cryptography_key
ROUTERAI_API_KEY=your_routerai_key
YOOKASSA_SHOP_ID=your_shop_id
YOOKASSA_SECRET_KEY=your_yookassa_secret_key
```

### 5. Сборка статики и миграции
```bash
npm run build:css
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
```

### 6. Запуск локального сервера
```bash
python manage.py runserver
```
</details>

## <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Postman.svg" width="24" height="24" valign="middle" /> Основные эндпоинты API

| Эндпоинт | Метод | Описание |
| :--- | :--- | :--- |
| `/dashboard/` | `GET` | Дашборд, фильтрация по категориям и поиск комнат |
| `/room/create/` | `GET, POST` | Создание новой комнаты с настройкой приватности |
| `/room/<slug>/` | `GET` | Детальный вид комнаты и переписка |
| `/room/<slug>/send/` | `POST` | Отправка текста, медиа или голосового сообщения |
| `/room/<slug>/messages/` | `GET` | Асинхронная подгрузка новых сообщений |
| `/room/<slug>/ai-integrations/` | `POST` | Подключение и настройка AI-моделей в комнате |
| `/room/<slug>/start_game/` | `POST` | Запуск интерактивной игры «Угадай фильм» |
| `/image-chat/generate/` | `POST` | Генерация артов по текстовому описанию |
| `/ai-management/generate-key/` | `POST` | Создание персонального API-ключа RouterAI |
| `/profile/subscribe/` | `POST` | Создание платежной сессии ЮKassa |

## <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Github-Dark.svg" width="24" height="24" valign="middle" /> Активность и Коммиты

<p align="center">
  <a href="https://github.com/X2X13211/NextRoom/commits/main">
    <img src="https://github-readme-activity-graph.vercel.app/graph?username=X2X13211&theme=tokyonight&color=8B5CF6&line=8B5CF6&point=ffffff&hide_border=true&bg_color=0D1117" alt="Commit activity graph" width="100%" />
  </a>
</p>

<p align="center">
  <img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=8B5CF6&height=130&section=footer" />
</p>
