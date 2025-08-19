#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instruction Parser - парсер текстовых инструкций
"""

from typing import List, Dict, Tuple, Optional

class InstructionParser:
    """Парсер инструкций из текстовых файлов"""
    
    def __init__(self):
        self.variables = {}  # Переменные для подстановки
        
    def parse_line(self, line: str) -> Optional[Dict]:
        """Парсит одну строку инструкции"""
        
        # Очистка и пропуск пустых/комментариев
        line = line.strip()
        if not line or line.startswith('#'):
            return None
        
        # Подстановка переменных
        for var, value in self.variables.items():
            line = line.replace(f"${var}", str(value))
        
        # Замена спецсимволов
        line = line.replace('\\n', '\n')
        
        # Разбор на части
        parts = line.split('|')
        if len(parts) < 1:
            return None
        
        command = parts[0].strip().upper()
        
        # Парсинг по типу команды
        if command == "SET":
            if len(parts) >= 3:
                self.variables[parts[1].strip()] = parts[2].strip()
                return {"type": "SET", "var": parts[1].strip(), "value": parts[2].strip()}
                
        elif command == "FRAME":
            if len(parts) >= 6:
                return {
                    "type": "FRAME",
                    "title": parts[1].strip(),
                    "x": float(parts[2]),
                    "y": float(parts[3]),
                    "width": float(parts[4]),
                    "height": float(parts[5])
                }
                
        elif command == "SHAPE":
            if len(parts) >= 6:
                return {
                    "type": "SHAPE",
                    "name": parts[1].strip(),
                    "x": float(parts[2]),
                    "y": float(parts[3]),
                    "width": float(parts[4]),
                    "height": float(parts[5]),
                    "color": parts[6].strip() if len(parts) > 6 else "#4169E1",
                    "shape": parts[7].strip() if len(parts) > 7 else "rectangle"
                }
                
        elif command == "STICKY":
            if len(parts) >= 4:
                return {
                    "type": "STICKY",
                    "text": parts[1].strip(),
                    "x": float(parts[2]),
                    "y": float(parts[3]),
                    "color": parts[4].strip() if len(parts) > 4 else "#FFFF99"
                }
                
        elif command == "TEXT":
            if len(parts) >= 4:
                return {
                    "type": "TEXT",
                    "content": parts[1].strip(),
                    "x": float(parts[2]),
                    "y": float(parts[3]),
                    "size": parts[4].strip() if len(parts) > 4 else "14"
                }
                
        elif command == "LINK":
            if len(parts) >= 3:
                return {
                    "type": "LINK",
                    "start": parts[1].strip(),
                    "end": parts[2].strip(),
                    "label": parts[3].strip() if len(parts) > 3 else ""
                }
                
        elif command == "SLEEP":
            if len(parts) >= 2:
                return {
                    "type": "SLEEP",
                    "seconds": float(parts[1])
                }
                
        elif command == "PRINT":
            if len(parts) >= 2:
                return {
                    "type": "PRINT",
                    "message": parts[1].strip()
                }
        
        return None
    
    def load_file(self, file_path: str) -> List[str]:
        """Загружает файл инструкций"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.readlines()
        except Exception as e:
            print(f"❌ Ошибка чтения файла {file_path}: {e}")
            return []
    
    def parse_file(self, file_path: str) -> List[Dict]:
        """Парсит весь файл инструкций"""
        lines = self.load_file(file_path)
        instructions = []
        
        for line in lines:
            try:
                parsed = self.parse_line(line)
                if parsed:
                    instructions.append(parsed)
            except Exception as e:
                print(f"⚠️  Ошибка парсинга строки: {e}")
                continue
        
        return instructions
