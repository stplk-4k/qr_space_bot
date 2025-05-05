import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.constants import ParseMode

def get_object_data(object_id):
    conn = sqlite3.connect('space_objects.db')
    cursor = conn.cursor()
    cursor.execute('SELECT title, description, image_url, model_url, add_info_url FROM objects WHERE id=?', (object_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
    
    return {
        "title": row[0],
        "description": row[1],
        "image_url": row[2],
        "model_url": row[3],
        "add_info_url": row[4]
    }

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    object_id = context.args[0] if context.args else None
    
    if not object_id:
        await update.message.reply_text(
            "Отсканируйте QR-код с объектом"
        )
        return

    data = get_object_data(object_id)
    
    if not data:
        await update.message.reply_text("🚫 Объект не найден")
        return

    message_text = f"✨ <b>{data['title']}</b>\n\n{data['description']}"
    
    if data["add_info_url"]:
        message_text += f"\n\n<a href='{data['add_info_url']}'>🔗 Дополнительная информация</a>"

    if data["image_url"]:
        await update.message.reply_photo(
            photo=data["image_url"],
            caption=message_text,
            parse_mode=ParseMode.HTML
        )
    else:
        await update.message.reply_text(
            message_text,
            parse_mode=ParseMode.HTML
        )

    if data["model_url"]:
        await update.message.reply_text(
            "Доступна 3D-модель:",
            reply_markup={
                "inline_keyboard": [[
                    {"text": "👀 Посмотреть в 3D", "web_app": {"url": data["model_url"]}}
                ]]
            }
        )


if __name__ == '__main__':
    application = ApplicationBuilder().token('8139380751:AAHCs0GLk5R8hPIIr8en9VbkkNzHgYQ0eis').build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()