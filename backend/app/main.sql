

-- 1. Таблица пользователей (users)
CREATE TABLE users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password TEXT,                           -- Может быть NULL, если пользователь зарегистрирован через OAuth
    role VARCHAR(50) NOT NULL DEFAULT 'user',  -- Роль пользователя (например, user, admin)
    is_active BOOLEAN DEFAULT FALSE,           -- Подтверждение email
    auth_provider VARCHAR(50) NULL,            -- Название OAuth-провайдера (google, github и т.д.)
    provider_id VARCHAR(255) NULL,      -- ID пользователя у OAuth-провайдера
    is_2fa_enabled BOOLEAN DEFAULT FALSE,       -- Флаг включенной двухфакторной аутентификации
    two_factor_secret TEXT,                    -- Секрет для TOTP (например, для Google Authenticator)
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

-- 2. Таблица сессий (user_sessions)
CREATE TABLE user_sessions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token TEXT NOT NULL UNIQUE,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);

-- 3. Таблица сброса пароля (password_resets)
CREATE TABLE password_resets (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token TEXT NOT NULL UNIQUE,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);

-- 4. Таблица привязки OAuth-аккаунтов (oauth_accounts)
CREATE TABLE oauth_accounts (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL,              -- Название провайдера (google, github и т.д.)
    provider_id VARCHAR(255) NOT NULL UNIQUE,     -- Уникальный ID пользователя у провайдера
    created_at TIMESTAMP DEFAULT now()
);

-- 5. Таблица хранения OAuth-токенов (oauth_tokens)
CREATE TABLE oauth_tokens (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL,               -- Название провайдера
    access_token TEXT NOT NULL,
    refresh_token TEXT,                          -- Может отсутствовать в некоторых провайдерах
    expires_at TIMESTAMP,                        -- Время истечения access_token
    created_at TIMESTAMP DEFAULT now()
);


CREATE TABLE students (
    id UUID PRIMARY KEY,
    group_number VARCHAR(50),
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);


CREATE TABLE schedule (
    group_number VARCHAR(20) NOT NULL,
    week_number INT NOT NULL CHECK (week_number BETWEEN 1 AND 4),
    monday JSON,
    tuesday JSON, 
    wednesday JSON,
    thursday JSON,
    friday JSON,
    saturday JSON,
    sunday JSON,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),
    PRIMARY KEY (group_number, week_number)
);


CREATE TABLE tasks (
    task_id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    deadline DATE,
    description VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),
    -- Опционально: внешний ключ на таблицу пользователей
    FOREIGN KEY (user_id) REFERENCES users(id)
);





-- Дополнительные индексы для ускорения запросов
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_user_sessions_token ON user_sessions(token);
CREATE INDEX idx_password_resets_token ON password_resets(token);
CREATE INDEX idx_oauth_accounts_provider_id ON oauth_accounts(provider_id);
CREATE INDEX idx_oauth_tokens_access_token ON oauth_tokens(access_token);
