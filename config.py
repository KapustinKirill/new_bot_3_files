#DATABASE_URL = 'postgresql://user:password@localhost/dbname'
# Замените на ваш токен бота
#TOKEN = "6191614629:AAEYf7iVkKAbl0WiKj_H6JMQTtVoItz3oUw"  #Боевой
TOKEN ='6011155293:AAHnaGNFFwNqoXsIzlgjWm6Lsjy8zKf6kH8'  #Тестовый

# Параметры подключения к базе данных
DB_USER = "telegram_bot"
DB_PASS = "Annela356"
DB_NAME = "telegram_bot"
DB_HOST = "87.249.44.78"

DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'

ADMIN_IDS = [221917894, 393145480]

EMAIL_ADDRESS = "marya.bot.2023@gmail.com"
EMAIL_PASSWORD = "pvggndtzabrxjqyi"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "marya.bot.2023@gmail.com"
EMAIL_HOST_PASSWORD = "pvggndtzabrxjqyi"

SMTP_SERVER = "smtp.yandex.ru"
SMTP_PORT = 465  # Yandex использует порт 465 для SSL
