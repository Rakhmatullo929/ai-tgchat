#!/bin/bash

# =================================
# SmartGroupBot Startup Script
# =================================

echo "🤖 Starting SmartGroupBot..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run: python -m venv venv"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if config file exists
if [ ! -f "config.env" ]; then
    echo "❌ Configuration file not found. Please copy config.env.example to config.env and fill it out."
    exit 1
fi

# Check if database exists, create if not
if [ ! -f "bot_database.db" ]; then
    echo "🗄️ Creating database..."
    python models.py
fi

# Start the bot
echo "🚀 Starting SmartGroupBot..."
python main_bot.py 