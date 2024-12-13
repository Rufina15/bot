from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)
import os
from dotenv import load_dotenv

# Resume Information
INFO = {
    "en": {
        "name": "Rufina Saiputulina",
        "position": "Mobile Developer (React Native / Android)",
        "email": "saiputulina.rufina@gmail.com",
        "phone": "+7-777-209-12-35",
        "commands": {
            "start": "👋 Hello! I'm *{name}*, a {position}.\n\nHere’s what you can learn about me:\n"
                     "/education - Education\n/experience - Work Experience\n/projects - Study Projects\n"
                     "/skills - Skills\n/contacts - Contact Information\n/language - Change language",
            "education": "🎓 *Education:*\nBachelor of Science in Information Systems\n"
                         "*Suleyman Demirel University*, 2020 – 2024\nGPA: 3.27/4.00",
            "experience": "💼 *Work Experience:*\n\n🔹 Tele2/ALTEL | Mobile Developer Intern (June – August 2024)\n"
                          "• Developed a mobile app using React Native CLI.\n"
                          "• Added new pages and integrated map functionality.\n\n"
                          "🔹 Richstone | Android Developer (March – June 2024)\n"
                          "• Built an Android app using Kotlin and Jetpack Compose.\n"
                          "• Implemented order screens and route maps.\n\n"
                          "🔹 XXL Mebel | Content Manager (June – August 2023)\n"
                          "• Collected furniture data and calculated prices.",
            "projects": "📝 *Projects:*\n\n🎓 *Cargo Management System* - Android app for cargo tracking with notifications.\n"
                        "🚀 *Drone Optimization* - Reinforcement Learning for route optimization.\n"
                        "🖌️ *UX/UI Design Project* - Created interactive student test app with branding.",
            "skills": "🛠️ *Skills:*\n• Programming Languages: JavaScript, Kotlin, HTML/CSS\n"
                      "• Frameworks: React Native, Jetpack Compose\n"
                      "• Tools: Git, Figma, PostgreSQL\n"
                      "• Languages: Uyghur, Kazakh, Russian, English, Turkish",
            "contacts": "📞 *Contact Information:*\n📧 Email: {email}\n📱 Phone: {phone}",
            "language": "🌐 Please choose your language:"
        }
    },
    "ru": {
        "name": "Руфина Сайпутулина",
        "position": "Мобильный разработчик (React Native / Android)",
        "email": "saiputulina.rufina@gmail.com",
        "phone": "+7-777-209-12-35",
        "commands": {
            "start": "👋 Привет! Я *{name}*, {position}.\n\nВот, что вы можете узнать обо мне:\n"
                     "/education - Образование\n/experience - Опыт работы\n/projects - Проекты\n"
                     "/skills - Навыки\n/contacts - Контакты\n/language - Выбрать язык",
            "education": "🎓 *Образование:*\nБакалавр информационных систем\n"
                         "*Университет Сулеймана Демиреля*, 2020 – 2024\nGPA: 3.27/4.00",
            "experience": "💼 *Опыт работы:*\n\n🔹 Tele2/ALTEL | Мобильный разработчик (Июнь – Август 2024)\n"
                          "• Разработка мобильного приложения на React Native CLI.\n"
                          "• Добавление страниц и карт.\n\n"
                          "🔹 Richstone | Android разработчик (Март – Июнь 2024)\n"
                          "• Создание Android-приложения с Kotlin и Jetpack Compose.\n"
                          "• Реализация экранов заказов и маршрутов.\n\n"
                          "🔹 XXL Mebel | Контент-менеджер (Июнь – Август 2023)\n"
                          "• Сбор данных о мебели и расчет цен.",
            "projects": "📝 *Проекты:*\n\n🎓 *Система управления грузами* - Android приложение для отслеживания грузов.\n"
                        "🚀 *Оптимизация с дронами* - Маршрутизация с помощью RL.\n"
                        "🖌️ *Проект UX/UI* - Интерактивное приложение для тестов студентов.",
            "skills": "🛠️ *Навыки:*\n• Языки программирования: JavaScript, Kotlin, HTML/CSS\n"
                      "• Фреймворки: React Native, Jetpack Compose\n"
                      "• Инструменты: Git, Figma, PostgreSQL\n"
                      "• Языки: Уйгурский, Казахский, Русский, Английский, Турецкий",
            "contacts": "📞 *Контактная информация:*\n📧 Email: {email}\n📱 Телефон: {phone}",
            "language": "🌐 Пожалуйста, выберите язык:"
        }
    },
    "kk": {
        "name": "Руфина Сайпутулина",
        "position": "Мобильді әзірлеуші (React Native / Android)",
        "email": "saiputulina.rufina@gmail.com",
        "phone": "+7-777-209-12-35",
        "commands": {
            "start": "👋 Сәлем! Мен *{name}*, {position}.\n\nМен туралы біле аласыз:\n"
                     "/education - Білім\n/experience - Жұмыс тәжірибесі\n/projects - Жобалар\n"
                     "/skills - Дағдылар\n/contacts - Байланыс ақпараттары\n/language - Тілді өзгерту",
            "education": "🎓 *Білімі:*\nАқпараттық жүйелер бакалавры\n"
                         "*Сүлейман Демирел Университеті*, 2020 – 2024\nGPA: 3.27/4.00",
            "experience": "💼 *Жұмыс тәжірибесі:*\n\n🔹 Tele2/ALTEL | Мобильді әзірлеуші (Маусым – Тамыз 2024)\n"
                          "• React Native арқылы қосымша әзірлеу.\n\n"
                          "🔹 Richstone | Android әзірлеуші (Наурыз – Маусым 2024)\n"
                          "• Kotlin және Jetpack Compose арқылы Android қосымшасын жасау.\n\n"
                          "🔹 XXL Mebel | Контент-менеджер (Маусым – Тамыз 2023)\n"
                          "• Жиһаздар туралы мәліметтер жинау және баға есептеу.",
            "projects": "📝 *Жобалар:*\n\n🎓 *Жүк басқару жүйесі* - Android қосымшасы.\n"
                        "🚀 *Дронмен оңтайландыру* - RL арқылы маршрутты оңтайландыру.\n"
                        "🖌️ *UX/UI жобасы* - Студенттер үшін тест қосымшасының дизайны.",
            "skills": "🛠️ *Дағдылар:*\n• Бағдарламалау тілдері: JavaScript, Kotlin, HTML/CSS\n"
                      "• Фреймворктер: React Native, Jetpack Compose\n"
                      "• Құралдар: Git, Figma, PostgreSQL\n"
                      "• Тілдер: Ұйғырша, Қазақша, Орысша, Ағылшынша, Түрікше",
            "contacts": "📞 *Байланыс ақпараттары:*\n📧 Email: {email}\n📱 Телефон: {phone}",
            "language": "🌐 Тілді таңдаңыз:"
        }
    }
}


# Helper function to get user language
def get_language(context):
    return context.user_data.get("language", "ru")

# Language Selection
async def language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("English 🇬🇧", callback_data="en")],
        [InlineKeyboardButton("Русский 🇷🇺", callback_data="ru")],
        [InlineKeyboardButton("Қазақша 🇰🇿", callback_data="kk")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🌐 Пожалуйста, выберите язык:", reply_markup=reply_markup)

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    language = query.data
    context.user_data["language"] = language
    await query.answer()
    text = INFO[language]["commands"]["start"].format(
        name=INFO[language]["name"], position=INFO[language]["position"]
    )
    await query.edit_message_text(text=text, parse_mode="Markdown")

# Generalized command handler
async def generic_command(update: Update, context: ContextTypes.DEFAULT_TYPE, key: str):
    language = get_language(context)
    data = INFO.get(language, INFO["en"])
    commands = data["commands"]

    name = data.get("name", "Rufina Saiputulina")
    position = data.get("position", "Mobile Developer")
    email = data.get("email", "not-provided@example.com")
    phone = data.get("phone", "Not Available")

    text = commands[key].format(name=name, position=position, email=email, phone=phone)
    await update.message.reply_text(text, parse_mode="Markdown")

# Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await generic_command(update, context, "start")

async def education(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await generic_command(update, context, "education")

async def experience(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await generic_command(update, context, "experience")

async def projects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await generic_command(update, context, "projects")

async def skills(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await generic_command(update, context, "skills")

async def contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await generic_command(update, context, "contacts")

# Main
if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("language", language))
    app.add_handler(CallbackQueryHandler(set_language))
    app.add_handler(CommandHandler("education", education))
    app.add_handler(CommandHandler("experience", experience))
    app.add_handler(CommandHandler("projects", projects))
    app.add_handler(CommandHandler("skills", skills))
    app.add_handler(CommandHandler("contacts", contacts))

    print("Bot is running...")
    app.run_polling()