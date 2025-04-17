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
    tuesday JSON,  -- Исправлено написание (было tuseday)
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