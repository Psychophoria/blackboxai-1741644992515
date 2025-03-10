#!/bin/bash

# Storm911 Setup Script for Unix/Linux Systems

# Text colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Storm911 Setup...${NC}\n"

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
if command -v python3 &>/dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')
    echo -e "${GREEN}Found Python $PYTHON_VERSION${NC}"
else
    echo -e "${RED}Python 3 not found. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

# Create virtual environment
echo -e "\n${YELLOW}Creating virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment already exists. Recreating...${NC}"
    rm -rf venv
fi

python3 -m venv venv
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to create virtual environment.${NC}"
    exit 1
fi
echo -e "${GREEN}Virtual environment created successfully.${NC}"

# Activate virtual environment
echo -e "\n${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to activate virtual environment.${NC}"
    exit 1
fi
echo -e "${GREEN}Virtual environment activated.${NC}"

# Upgrade pip
echo -e "\n${YELLOW}Upgrading pip...${NC}"
python -m pip install --upgrade pip
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to upgrade pip.${NC}"
    exit 1
fi
echo -e "${GREEN}Pip upgraded successfully.${NC}"

# Install dependencies
echo -e "\n${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to install dependencies.${NC}"
    exit 1
fi
echo -e "${GREEN}Dependencies installed successfully.${NC}"

# Create required directories
echo -e "\n${YELLOW}Creating required directories...${NC}"
mkdir -p assets EXPORTS logs data
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to create directories.${NC}"
    exit 1
fi
echo -e "${GREEN}Directories created successfully.${NC}"

# Set file permissions
echo -e "\n${YELLOW}Setting file permissions...${NC}"
chmod +x *.py
chmod 755 assets EXPORTS logs data
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to set permissions.${NC}"
    exit 1
fi
echo -e "${GREEN}Permissions set successfully.${NC}"

# Create .env file if it doesn't exist
echo -e "\n${YELLOW}Checking .env file...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cat > .env << EOL
# Storm911 Environment Configuration

# Email Settings
STORM911_EMAIL=your_email@example.com
STORM911_EMAIL_PASSWORD=your_email_password

# API Settings
READYMODE_API_USER=your_api_username
READYMODE_API_PASS=your_api_password
EOL
    echo -e "${GREEN}.env file created. Please update with your credentials.${NC}"
else
    echo -e "${GREEN}.env file already exists.${NC}"
fi

# Run setup test
echo -e "\n${YELLOW}Running setup test...${NC}"
python test_setup.py
if [ $? -ne 0 ]; then
    echo -e "${RED}Setup test failed. Please check the errors above.${NC}"
    exit 1
fi
echo -e "${GREEN}Setup test completed successfully.${NC}"

echo -e "\n${GREEN}Storm911 setup completed successfully!${NC}"
echo -e "\nTo start the application:"
echo -e "1. Activate the virtual environment: ${YELLOW}source venv/bin/activate${NC}"
echo -e "2. Run the application: ${YELLOW}python app.py${NC}"
echo -e "\nFor more information, please read the README.md file."
