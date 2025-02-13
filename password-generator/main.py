import secrets
import string
from argparse import ArgumentParser
from typing import Dict, List

DEFAULT_SPECIAL_CHARS = "!@#$%^&*+-_=?"
AMBIGUOUS_CHARS = {"l", "I", "1", "O", "0"}  # Символы, которые можно спутать

class PasswordGenerator:
    def __init__(self):
        self.char_categories: Dict[str, str] = {
            'lower': string.ascii_lowercase,
            'upper': string.ascii_uppercase,
            'digits': string.digits,
            'special': DEFAULT_SPECIAL_CHARS
        }
    
    def generate_password(
        self,
        length: int = 16,
        min_categories: int = 3,
        allow_ambiguous: bool = False,
        custom_special: str = None
    ) -> str:
        """
        Генерирует безопасный пароль с настройкой параметров
        
        :param length: Длина пароля (12-64)
        :param min_categories: Минимум категорий (2-4)
        :param allow_ambiguous: Разрешить неоднозначные символы
        :param custom_special: Кастомные специальные символы
        :return: Сгенерированный пароль
        """
        # Валидация параметров
        self._validate_params(length, min_categories)
        
        # Настройка категорий
        categories = self._prepare_categories(custom_special, allow_ambiguous)
        
        # Генерация обязательных символов
        password = self._generate_required_chars(categories, min_categories)
        
        # Заполнение оставшихся позиций
        all_chars = self._combine_chars(categories)
        password += self._generate_random_chars(all_chars, length - len(password))
        
        # Перемешивание и возврат результата
        return self._shuffle_password(password)

    def _validate_params(self, length: int, min_categories: int):
        """Проверка входных параметров"""
        if not 12 <= length <= 64:
            raise ValueError("Длина пароля должна быть между 12 и 64 символами")
        if not 2 <= min_categories <= 4:
            raise ValueError("Количество категорий должно быть между 2 и 4")

    def _prepare_categories(
        self,
        custom_special: str,
        allow_ambiguous: bool
    ) -> Dict[str, str]:
        """Подготовка категорий символов с учетом настроек"""
        categories = self.char_categories.copy()
        
        # Обработка кастомных символов
        if custom_special:
            categories['special'] = custom_special
        
        # Удаление неоднозначных символов
        if not allow_ambiguous:
            for cat in ['lower', 'upper', 'digits']:
                categories[cat] = ''.join(
                    c for c in categories[cat] 
                    if c not in AMBIGUOUS_CHARS
                )
        
        return categories

    def _generate_required_chars(
        self, 
        categories: Dict[str, str], 
        min_categories: int
    ) -> List[str]:
        """Генерация обязательных символов из разных категорий"""
        selected = secrets.SystemRandom().sample(
            list(categories.keys()), 
            min_categories
        )
        return [secrets.choice(categories[cat]) for cat in selected]

    def _combine_chars(self, categories: Dict[str, str]) -> str:
        """Объединение всех разрешенных символов"""
        return ''.join(categories.values())

    def _generate_random_chars(self, chars: str, count: int) -> List[str]:
        """Генерация случайных символов"""
        return [secrets.choice(chars) for _ in range(count)]

    def _shuffle_password(self, password: List[str]) -> str:
        """Криптобезопасное перемешивание"""
        shuffled = password.copy()
        secrets.SystemRandom().shuffle(shuffled)
        return ''.join(shuffled)

def main():
    parser = ArgumentParser(description="Генератор безопасных паролей")
    parser.add_argument("-l", "--length", type=int, default=16,
                       help="Длина пароля (12-64, по умолчанию 16)")
    parser.add_argument("-c", "--categories", type=int, default=3,
                       help="Минимальное количество категорий (2-4)")
    parser.add_argument("-a", "--allow-ambiguous", action="store_true",
                       help="Разрешить неоднозначные символы (e.g. 1 и l)")
    parser.add_argument("-s", "--special", type=str,
                       help="Кастомные специальные символы")
    parser.add_argument("-n", "--number", type=int, default=3,
                       help="Количество паролей для генерации")

    args = parser.parse_args()
    generator = PasswordGenerator()

    try:
        for _ in range(args.number):
            print(generator.generate_password(
                length=args.length,
                min_categories=args.categories,
                allow_ambiguous=args.allow_ambiguous,
                custom_special=args.special
            ))
    except ValueError as e:
        print(f"Ошибка генерации: {e}")
        exit(1)

if __name__ == "__main__":
    main()