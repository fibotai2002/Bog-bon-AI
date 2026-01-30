#!/bin/bash
echo "🚀 GitHub ga yuklash yordamchisi"
echo "-----------------------------------"
echo "1. Brauzerda ushbu manzilga kiring va yangi token yarating:"
echo "   https://github.com/settings/tokens/new?scopes=repo&description=AgroAI_Deploy"
echo ""
echo "2. Sahifa pastida 'Generate token' tugmasini bosing."
echo "3. Chiqqan kodni (tokenni) nusxalab oling."
echo "-----------------------------------"
read -p "Tokenni shu yerga tashlang (paste) va Enterni bosing: " TOKEN

if [ -z "$TOKEN" ]; then
    echo "❌ Token kiritilmadi!"
    exit 1
fi

echo "🔄 Yuklanmoqda..."
git remote set-url origin https://$TOKEN@github.com/fibotai2002/Bog-bon-AI.git
git push -u origin main

if [ $? -eq 0 ]; then
    echo "✅ Muvaffaqiyatli yuklandi!"
    echo "Endi Render.com ga o'tib deploy qilishingiz mumkin."
else
    echo "❌ Xatolik yuz berdi. Token to'g'riligini tekshiring."
fi
