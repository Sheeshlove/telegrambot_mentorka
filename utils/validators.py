import re
from datetime import datetime

# English: Validation functions for user input
# Russian: Функции валидации пользовательского ввода

def validate_snils(snils: str) -> bool:
    """
    English: Validate SNILS format (XXX-XXX-XXX XX)
    Russian: Проверка формата СНИЛС (XXX-XXX-XXX XX)
    
    Args:
        snils (str): SNILS number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^\d{3}-\d{3}-\d{3} \d{2}$'
    return bool(re.match(pattern, snils))

def validate_date(date_str: str) -> bool:
    """
    English: Validate date format (YYYY-MM-DD)
    Russian: Проверка формата даты (YYYY-MM-DD)
    
    Args:
        date_str (str): Date string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_fio(fio: str) -> bool:
    """
    English: Validate FIO format (at least two words)
    Russian: Проверка формата ФИО (минимум два слова)
    
    Args:
        fio (str): FIO string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    return len(fio.strip().split()) >= 2 