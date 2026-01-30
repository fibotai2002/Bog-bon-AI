
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
import json
import os
from bot.config import is_admin

router = Router()

def get_admin_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Statistika"), KeyboardButton(text="👥 Foydalanuvchilar")]
        ],
        resize_keyboard=True
    )

@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔️ Sizda admin huquqi yo'q!")
        return
    
    await message.answer(
        "🔐 <b>Admin Panel</b>\n\nXush kelibsiz!", 
        reply_markup=get_admin_keyboard(),
        parse_mode="HTML"
    )

@router.message(F.text == "📊 Statistika")
async def show_stats(message: Message):
    if not is_admin(message.from_user.id):
        return

    try:
        with open("data/users.json", "r") as f:
            users = json.load(f)
        
        total_users = len(users)
        regions = {}
        
        for user in users.values():
            region = user.get("region", "Noma'lum")
            regions[region] = regions.get(region, 0) + 1
            
        stats_msg = f"📊 <b>Bot Statistikasi</b>\n\n"
        stats_msg += f"Jami foydalanuvchilar: {total_users}\n\n"
        stats_msg += "<b>Hududlar bo'yicha:</b>\n"
        
        for region, count in regions.items():
            stats_msg += f"- {region}: {count}\n"
            
        await message.answer(stats_msg, parse_mode="HTML")
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {str(e)}")

@router.message(F.text == "👥 Foydalanuvchilar")
async def show_users(message: Message):
    if not is_admin(message.from_user.id):
        return

    try:
        with open("data/users.json", "r") as f:
            users = json.load(f)
            
        users_list = "👥 <b>Foydalanuvchilar Ro'yxati:</b>\n\n"
        
        # Determine the maximum message length (Telegram limit is 4096)
        MAX_LENGTH = 4000 
        current_msg = users_list
        
        i = 1
        for user_id, data in users.items():
            name = data.get("name", "Noma'lum")
            phone = data.get("phone", "Noma'lum")
            
            line = f"{i}. <b>{name}</b> - {phone}\n"
            
            if len(current_msg) + len(line) > MAX_LENGTH:
                await message.answer(current_msg, parse_mode="HTML")
                current_msg = ""
            
            current_msg += line
            i += 1
            
        if current_msg:
            await message.answer(current_msg, parse_mode="HTML")
            
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {str(e)}")
