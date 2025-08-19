#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Miro Engine - главный модуль
"""

import sys
import time
import getpass
from pathlib import Path
from typing import List

from _helper.miro_api import MiroAPI
from _helper.instruction_parser import InstructionParser
from _helper.command_executor import CommandExecutor

class MiroEngine:
    """Основной движок"""
    
    def __init__(self, token: str, board_id: str):
        self.api = MiroAPI(token, board_id)
        self.parser = InstructionParser()
        self.executor = CommandExecutor(self.api)
    
    def process_file(self, file_path: str) -> bool:
        """Обрабатывает один файл инструкций"""
        print(f"\n📄 Обработка файла: {file_path}")
        print("-" * 50)
        
        # Парсинг инструкций
        instructions = self.parser.parse_file(file_path)
        if not instructions:
            print("  ⚠️  Нет инструкций в файле")
            return False
        
        # Выполнение команд
        success_count = 0
        for instruction in instructions:
            if self.executor.execute(instruction):
                success_count += 1
        
        print(f"Выполнено: {success_count}/{len(instructions)} инструкций")
        return success_count > 0
    
    def find_instruction_files(self) -> List[Path]:
        """Находит все файлы инструкций"""
        files = []
        
        # Ищем в папке instructions
        instructions_dir = Path("instructions")
        if instructions_dir.exists():
            files.extend(sorted(instructions_dir.glob("*.txt")))
        
        # Ищем в текущей папке
        files.extend(sorted(Path(".").glob("*_instructions.txt")))
        
        return files

def get_credentials():
    """Получает учетные данные от пользователя"""
    print("\n📋 Настройка подключения к Miro:")
    print("-"*60)
    
    # Token
    print("\n📌 Где взять токен:")
    print("  1. Войдите в Miro")
    print("  2. Settings → Apps → Your apps")
    print("  3. Create new app → Get OAuth token")
    
    # Безопасный ввод токена (скрытый)
    token = getpass.getpass("\n➤ Введите API Token (ввод скрыт): ").strip()
    if not token:
        print("❌ Token обязателен!")
        sys.exit(1)
    
    # Показываем только первые символы для подтверждения
    masked_token = token[:10] + "..." if len(token) > 10 else token
    print(f"  ✓ Token получен: {masked_token}")
    
    # Board ID
    print("\n📌 Где взять Board ID:")
    print("  Откройте доску → скопируйте ID из URL")
    print("  Пример: miro.com/app/board/{BOARD_ID}/")
    
    board_id = input("\n➤ Введите Board ID: ").strip()
    if not board_id:
        print("❌ Board ID обязателен!")
        sys.exit(1)
    
    return token, board_id

def select_files(files: List[Path]) -> List[Path]:
    """Выбор файлов для обработки"""
    print(f"\n📋 Найдено файлов инструкций: {len(files)}")
    for i, file in enumerate(files, 1):
        print(f"  {i}. {file}")
    
    print("\n➤ Какие файлы обработать?")
    print("  1. Все файлы")
    print("  2. Выбрать конкретные")
    
    choice = input("Выбор (1/2): ").strip()
    
    if choice == "2":
        numbers = input("Введите номера файлов через запятую: ").strip()
        try:
            indices = [int(n.strip())-1 for n in numbers.split(',')]
            return [files[i] for i in indices if 0 <= i < len(files)]
        except:
            print("❌ Неверный формат")
            sys.exit(1)
    else:
        return files

def process_instructions(engine: MiroEngine, board_id: str):
    """Обработка инструкций"""
    # Находим файлы инструкций
    print("\n📂 Поиск файлов инструкций...")
    print("-"*60)
    
    files = engine.find_instruction_files()
    if not files:
        print("⚠️  Не найдено файлов инструкций!")
        print("\nСоздайте файлы в папке 'instructions/'")
        return False
    
    # Выбираем файлы
    selected_files = select_files(files)
    if not selected_files:
        print("❌ Файлы не выбраны")
        return False
    
    # Подтверждение
    print(f"\n📌 Будет обработано файлов: {len(selected_files)}")
    confirm = input("➤ Начать создание? (да/нет): ").strip().lower()
    
    if confirm not in ["да", "yes", "y", "д"]:
        print("⚠️  Отменено")
        return False
    
    # Обработка файлов
    print("\n" + "="*60)
    print("🎯 НАЧИНАЮ ОБРАБОТКУ")
    print("="*60)
    
    for file_path in selected_files:
        engine.process_file(file_path)
        time.sleep(1)
    
    # Статистика
    engine.executor.print_stats()
    
    print(f"\n🔗 Откройте доску для просмотра:")
    print(f"   https://miro.com/app/board/{board_id}/")
    print("\n✅ Готово!")
    return True

def main():
    """Главная функция с жизненным циклом"""
    print("\n" + "="*60)
    print("   🚀 MIRO ENGINE - UNIVERSAL DIAGRAM BUILDER")
    print("="*60)
    
    # Получаем учетные данные (один раз)
    token, board_id = get_credentials()
    
    # Создаем движок (один раз)
    engine = MiroEngine(token, board_id)
    
    # Жизненный цикл
    while True:
        print("\n" + "="*60)
        print("🔄 ГЛАВНОЕ МЕНЮ")
        print("="*60)
        print("1. Обработать инструкции")
        print("2. Показать доступные файлы")
        print("3. Сменить токен")
        print("4. Сменить доску")
        print("5. Выход")
        
        choice = input("\n➤ Выберите действие (1-5): ").strip()
        
        if choice == "1":
            process_instructions(engine, board_id)
            
        elif choice == "2":
            files = engine.find_instruction_files()
            if files:
                print(f"\n📁 Найдено файлов: {len(files)}")
                for i, file_path in enumerate(files, 1):
                    print(f"  {i}. {file_path.name}")
            else:
                print("\n❌ Файлы инструкций не найдены")
                
        elif choice == "3":
            print("\n🔑 СМЕНА ТОКЕНА")
            print("-"*60)
            print("📌 Где взять токен:")
            print("  1. Войдите в Miro")
            print("  2. Settings → Apps → Your apps")
            print("  3. Create new app → Get OAuth token")
            
            new_token = getpass.getpass("\n➤ Введите новый API Token (ввод скрыт): ").strip()
            if new_token:
                token = new_token
                engine = MiroEngine(token, board_id)  # Пересоздаем движок
                masked_token = token[:10] + "..." if len(token) > 10 else token
                print(f"✅ Токен обновлен: {masked_token}")
            else:
                print("⚠️  Токен не изменен")
                
        elif choice == "4":
            print("\n📋 СМЕНА ДОСКИ")
            print("-"*60)
            print("📌 Где взять Board ID:")
            print("  Откройте доску → скопируйте ID из URL")
            print("  Пример: miro.com/app/board/{BOARD_ID}/")
            print(f"\n  Текущая доска: {board_id}")
            
            new_board_id = input("\n➤ Введите новый Board ID: ").strip()
            if new_board_id:
                board_id = new_board_id
                engine = MiroEngine(token, board_id)  # Пересоздаем движок
                print(f"✅ Доска изменена: {board_id}")
            else:
                print("⚠️  Доска не изменена")
                
        elif choice == "5":
            print("\n👋 До свидания!")
            break
            
        else:
            print("\n⚠️  Неверный выбор. Попробуйте снова.")
        
        # Пауза перед следующей итерацией
        input("\n📌 Нажмите Enter для продолжения...")

if __name__ == "__main__":
    main()