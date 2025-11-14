from datetime import datetime

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# ===== Настройки БД =====
# файл app.db создастся в папке рядом со скриптом
DATABASE_URL = "sqlite:///app.db"

engine = create_engine(
    DATABASE_URL,
    echo=True,        # лог SQL в консоль (можно выключить на prod: echo=False)
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

Base = declarative_base()


# ===== Модели =====

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    tg_id = Column(String(50), unique=True, nullable=True)

    # связь с напоминаниями
    reminders = relationship("Reminder", back_populates="user")

    def __repr__(self):
        return f"<User id={self.id} login={self.login!r}>"


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    text = Column(Text, nullable=False)
    remind_at = Column(DateTime, nullable=False)
    is_sent = Column(Boolean, nullable=False, default=False)

    user = relationship("User", back_populates="reminders")

    def __repr__(self):
        return f"<Reminder id={self.id} user_id={self.user_id} at={self.remind_at}>"


# ===== Инициализация БД =====

def init_db():
    """
    Создаёт файл БД (если его нет) и все таблицы согласно моделям.
    """
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("База и таблицы созданы.")
