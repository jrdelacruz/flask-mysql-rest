import os

class Config:
    SERVER_PORT = os.getenv('SERVER_PORT', 5000)
    DEBUG = os.getenv('DEBUG', True)
    ALLOWED_DOMAINS = os.getenv('ALLOWED_DOMAINS', '*')
    
    ## MySQL configurations
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USERNAME', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DB = os.getenv('MYSQL_DB', '')