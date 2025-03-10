# Storm911 Call Center Application

A professional call center application designed for managing roofing inspection appointments and customer interactions.

## Features

- **Professional Call Script**: Guided 22-page script for consistent customer interactions
- **Real-time Lead Management**: Integrated with ReadyMode API for lead tracking
- **Objection Handling**: Built-in responses for common customer objections
- **PDF Generation**: Automated report and confirmation generation
- **Email Integration**: Automated appointment confirmations and follow-ups
- **Progress Tracking**: Real-time call progress monitoring
- **Data Validation**: Comprehensive input validation and error handling
- **Theme Support**: Light and dark theme options
- **Customizable Settings**: Flexible application configuration

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/storm911.git
cd storm911
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run setup test:
```bash
python test_setup.py
```

## Configuration

1. Create a `.env` file in the root directory with your API credentials:
```env
STORM911_EMAIL=your_email@example.com
STORM911_EMAIL_PASSWORD=your_email_password
READYMODE_API_USER=your_api_username
READYMODE_API_PASS=your_api_password
```

2. Configure application settings in `config.py` as needed.

## Usage

1. Start the application:
```bash
python app.py
```

2. Log in with your ReadyMode credentials.

3. The interface consists of three main panels:
   - **Caller Data & Info**: Customer and appointment information
   - **Transcript**: Call script and progress tracking
   - **Objections**: Quick access to objection responses

## Directory Structure

```
STORM911/
├── app.py                  # Main application entry point
├── app_initializer.py      # Application initialization
├── api_handler.py          # API integration
├── caller_info_panel.py    # Caller information UI
├── config.py              # Configuration settings
├── dialog_manager.py      # Dialog and popup management
├── disposition_handler.py  # Call disposition handling
├── email_handler.py       # Email functionality
├── event_logger.py        # Event logging
├── hotkey_manager.py      # Keyboard shortcuts
├── menu_manager.py        # Menu and toolbar
├── objection_responses.py # Objection handling
├── pdf_handler.py         # PDF generation
├── settings_manager.py    # Settings management
├── state_manager.py       # Application state
├── theme_manager.py       # Theme handling
├── transcript_content.py  # Script content
├── transcript_panel.py    # Transcript UI
├── ui_panels.py          # UI components
├── utils.py              # Utility functions
├── requirements.txt      # Dependencies
├── LICENSE              # License information
└── README.md           # Documentation
```

## Key Components

### Caller Information Panel
- Phone number search
- Customer details
- Roofing information
- Insurance details
- Appointment scheduling

### Transcript Panel
- 22-page guided script
- Progress tracking
- Navigation controls
- Key points display

### Objections Panel
- Two groups of common objections
- Quick access buttons
- Detailed response dialogs
- Keyboard shortcuts

## Development

### Adding New Features
1. Create a new module in the appropriate directory
2. Update `app_initializer.py` to include the new module
3. Add any new dependencies to `requirements.txt`
4. Update tests in `test_setup.py`

### Running Tests
```bash
python -m pytest tests/
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Include docstrings
- Add logging statements

## Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Check API credentials in `.env`
   - Verify internet connection
   - Check API endpoint status

2. **Email Sending Failures**
   - Verify email credentials
   - Check SMTP settings
   - Ensure proper email format

3. **PDF Generation Issues**
   - Check write permissions
   - Verify template existence
   - Ensure required data is present

### Logging

Logs are stored in the `logs` directory:
- `storm911.log`: Main application log
- `api.log`: API interaction log
- `error.log`: Error tracking
- `security.log`: Security events

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:
- Email: support@storm911.com
- Phone: 1-800-STORM911
- Documentation: [docs.storm911.com](https://docs.storm911.com)

## Acknowledgments

- CustomTkinter for the modern UI components
- ReadyMode for API integration
- All contributors and testers
