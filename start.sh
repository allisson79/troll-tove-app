#!/bin/bash
# Quick start script for local development

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔮 Troll-Tove Local Development Setup${NC}\n"

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file from .env.example...${NC}"
    cp .env.example .env
    
    # Generate a random SECRET_KEY
    SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
    
    # Update .env with generated key
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/your-secret-key-here/$SECRET_KEY/" .env
    else
        # Linux
        sed -i "s/your-secret-key-here/$SECRET_KEY/" .env
    fi
    
    # Enable debug mode for local development
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' 's/FLASK_DEBUG=false/FLASK_DEBUG=true/' .env
    else
        sed -i 's/FLASK_DEBUG=false/FLASK_DEBUG=true/' .env
    fi
    
    echo -e "${GREEN}✓ .env file created with random SECRET_KEY${NC}"
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -q -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Run the application
echo -e "\n${GREEN}Starting Troll-Tove app...${NC}"
echo -e "${BLUE}Access the app at: http://localhost:5000${NC}"
echo -e "${BLUE}Health check: http://localhost:5000/health${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop${NC}\n"

python app.py
