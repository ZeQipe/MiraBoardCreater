#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command Executor - выполнение распарсенных команд
"""

import time
from typing import Dict, Any
from miro_api import MiroAPI

class CommandExecutor:
    """Исполнитель команд"""
    
    def __init__(self, api_client: MiroAPI):
        self.api = api_client
        self.stats = {
            "frames": 0,
            "shapes": 0,
            "stickies": 0,
            "connectors": 0,
            "texts": 0
        }
    
    def execute(self, command: Dict[str, Any]) -> bool:
        """Выполняет одну команду"""
        
        cmd_type = command.get("type")
        
        try:
            if cmd_type == "FRAME":
                result = self.api.create_frame(
                    command["title"],
                    command["x"],
                    command["y"],
                    command["width"],
                    command["height"]
                )
                if result:
                    self.stats["frames"] += 1
                    print(f"  ✓ Рамка '{command['title']}'")
                return bool(result)
            
            elif cmd_type == "SHAPE":
                result = self.api.create_shape(
                    command["name"],
                    command["x"],
                    command["y"],
                    command["width"],
                    command["height"],
                    command["color"],
                    command["shape"]
                )
                if result:
                    self.stats["shapes"] += 1
                    print(f"  ✓ Фигура '{command['name']}'")
                return bool(result)
            
            elif cmd_type == "STICKY":
                result = self.api.create_sticky(
                    command["text"],
                    command["x"],
                    command["y"],
                    command["color"]
                )
                if result:
                    self.stats["stickies"] += 1
                    print(f"  ✓ Стикер")
                return bool(result)
            
            elif cmd_type == "TEXT":
                result = self.api.create_text(
                    command["content"],
                    command["x"],
                    command["y"],
                    command["size"]
                )
                if result:
                    self.stats["texts"] += 1
                    print(f"  ✓ Текст")
                return bool(result)
            
            elif cmd_type == "LINK":
                result = self.api.create_connector(
                    command["start"],
                    command["end"],
                    command["label"]
                )
                if result:
                    self.stats["connectors"] += 1
                    print(f"  ✓ Связь '{command['start']}' -> '{command['end']}'")
                return bool(result)
            
            elif cmd_type == "SLEEP":
                time.sleep(command["seconds"])
                return True
            
            elif cmd_type == "PRINT":
                print(command["message"])
                return True
            
            elif cmd_type == "SET":
                # Переменные уже обработаны в парсере
                return True
            
            else:
                print(f"⚠️  Неизвестная команда: {cmd_type}")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка выполнения: {e}")
            return False
    
    def get_stats(self) -> Dict[str, int]:
        """Возвращает статистику"""
        return self.stats
    
    def print_stats(self):
        """Выводит статистику"""
        print("\n" + "="*50)
        print("📊 СТАТИСТИКА СОЗДАНИЯ:")
        print("-"*50)
        for item_type, count in self.stats.items():
            if count > 0:
                print(f"  • {item_type}: {count}")
        print(f"  • ВСЕГО: {sum(self.stats.values())}")
        print("="*50)
