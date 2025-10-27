#!/bin/bash
# Setup script for Founding Engineers Newsletter Agent

echo "🚀 Setting up Founding Engineers Newsletter Agent..."

# Create virtual environment (optional but recommended)
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your API keys (optional)"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the agent:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run the agent: python main.py"
echo ""
