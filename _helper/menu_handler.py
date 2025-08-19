#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Menu Handler - обработка меню и пользовательского интерфейса
"""

import sys
import time
import getpass
from pathlib import Path
from typing import List

class MenuHandler:
    """Обработчик меню и пользовательского интерфейса"""
    
    def __init__(self):
        pass
    
    def get_credentials(self):
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
    
    def select_files(self, files: List[Path]) -> List[Path]:
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
    
    def process_instructions(self, engine, board_id: str):
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
        selected_files = self.select_files(files)
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
    
    def change_token(self, engine_class, board_id: str):
        """Смена токена"""
        print("\n🔑 СМЕНА ТОКЕНА")
        print("-"*60)
        print("📌 Где взять токен:")
        print("  1. Войдите в Miro")
        print("  2. Settings → Apps → Your apps")
        print("  3. Create new app → Get OAuth token")
        
        new_token = getpass.getpass("\n➤ Введите новый API Token (ввод скрыт): ").strip()
        if new_token:
            engine = engine_class(new_token, board_id)
            masked_token = new_token[:10] + "..." if len(new_token) > 10 else new_token
            print(f"✅ Токен обновлен: {masked_token}")
            return new_token, engine
        else:
            print("⚠️  Токен не изменен")
            return None, None
    
    def change_board(self, engine_class, token: str, current_board_id: str):
        """Смена доски"""
        print("\n📋 СМЕНА ДОСКИ")
        print("-"*60)
        print("📌 Где взять Board ID:")
        print("  Откройте доску → скопируйте ID из URL")
        print("  Пример: miro.com/app/board/{BOARD_ID}/")
        print(f"\n  Текущая доска: {current_board_id}")
        
        new_board_id = input("\n➤ Введите новый Board ID: ").strip()
        if new_board_id:
            engine = engine_class(token, new_board_id)
            print(f"✅ Доска изменена: {new_board_id}")
            return new_board_id, engine
        else:
            print("⚠️  Доска не изменена")
            return None, None
    
    def show_files(self, engine):
        """Показать доступные файлы"""
        files = engine.find_instruction_files()
        if files:
            print(f"\n📁 Найдено файлов: {len(files)}")
            for i, file_path in enumerate(files, 1):
                print(f"  {i}. {file_path.name}")
        else:
            print("\n❌ Файлы инструкций не найдены")
    
    def show_main_menu(self):
        """Показать главное меню"""
        print("\n" + "="*60)
        print("🔄 ГЛАВНОЕ МЕНЮ")
        print("="*60)
        print("1. Обработать инструкции")
        print("2. Показать доступные файлы")
        print("3. Сменить токен")
        print("4. Сменить доску")
        print("5. Выход")
        
        return input("\n➤ Выберите действие (1-5): ").strip()
