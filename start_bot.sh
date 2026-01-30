#!/bin/bash

# Bog'bon AI botini ishga tushirish scripti

cd "$(dirname "$0")"

echo "🤖 Bog'bon AI botini ishga tushiryapman..."

# Virtual environmentni aktivlashtirish
source .venv/bin/activate

# Botni ishga tushirish
python3 -m bot.main
