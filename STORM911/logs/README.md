# Storm911 Logs Directory

This directory contains application log files generated during runtime.

## Log Files

- `storm911.log` - Main application log
- `api.log` - API interaction logs
- `error.log` - Error tracking and debugging
- `security.log` - Security-related events
- `calls.log` - Call activity logs

## Log Levels

The application uses the following log levels:
- DEBUG: Detailed information for debugging
- INFO: General operational information
- WARNING: Minor issues that don't affect core functionality
- ERROR: Serious issues that affect functionality
- CRITICAL: Critical issues that require immediate attention

## Log Format

Each log entry follows this format:
```
TIMESTAMP - LEVEL - MODULE - MESSAGE
```

Example:
```
2023-08-15 14:30:45,123 - INFO - api_handler - API connection established
```

## Log Rotation

Logs are automatically rotated:
- Maximum file size: 10MB
- Backup count: 5 files
- Rotation occurs daily or when size limit is reached

## Maintenance

- Log files are excluded from version control
- Old logs are automatically archived after 30 days
- The logs directory is automatically created if missing
- Log files can be cleared using the application's tools menu

## Security

- Sensitive information is automatically redacted
- Log files are only accessible to authorized users
- Failed login attempts are logged in security.log
- API credentials are never logged in plain text

## Troubleshooting

If logs are not being generated:
1. Check write permissions on the logs directory
2. Verify log level settings in config.py
3. Ensure disk space is available
4. Check application logging configuration

## Support

For log-related issues:
- Email: support@storm911.com
- Documentation: [docs.storm911.com/logs](https://docs.storm911.com/logs)
