#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Miro Engine - главный модуль
"""

from pathlib import Path
from typing import List

from _helper.miro_api import MiroAPI
from _helper.instruction_parser import InstructionParser
from _helper.command_executor import CommandExecutor
from _helper.menu_handler import MenuHandler

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

def main():
    """Главная функция с жизненным циклом"""
    print("\n" + "="*60)
    print("   🚀 MIRO ENGINE - UNIVERSAL DIAGRAM BUILDER")
    print("="*60)
    
    # Создаем обработчик меню
    menu = MenuHandler()
    
    # Получаем учетные данные (один раз)
    token, board_id = menu.get_credentials()
    
    # Создаем движок (один раз)
    engine = MiroEngine(token, board_id)
    
    # Жизненный цикл
    while True:
        choice = menu.show_main_menu()
        
        if choice == "1":
            menu.process_instructions(engine, board_id)
            
        elif choice == "2":
            menu.show_files(engine)
                
        elif choice == "3":
            result = menu.change_token(MiroEngine, board_id)
            if result[0]:  # Если токен изменен
                token, engine = result
                
        elif choice == "4":
            result = menu.change_board(MiroEngine, token, board_id)
            if result[0]:  # Если доска изменена
                board_id, engine = result
                
        elif choice == "5":
            print("\n👋 До свидания!")
            break
            
        else:
            print("\n⚠️  Неверный выбор. Попробуйте снова.")
        
        # Пауза перед следующей итерацией
        input("\n📌 Нажмите Enter для продолжения...")

if __name__ == "__main__":
    main()