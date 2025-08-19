#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Miro API Client - работа с API Miro
"""

import requests
from typing import Optional, Dict, Any

class MiroAPI:
    """Клиент для работы с Miro API"""
    
    def __init__(self, token: str, board_id: str):
        self.token = token
        self.board_id = board_id
        self.base_url = "https://api.miro.com/v2"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        self.elements = {}  # {name: id} для связей
        
    def api_call(self, endpoint: str, data: dict) -> Optional[str]:
        """Универсальный API вызов"""
        url = f"{self.base_url}/boards/{self.board_id}/{endpoint}"
        
        try:
            response = requests.post(url, headers=self.headers, json=data, timeout=10)
            if response.status_code == 201:
                return response.json().get("id")
            else:
                print(f"⚠️  API ошибка {response.status_code} для {endpoint}")
                try:
                    error_details = response.json()
                    
                    # Специальная обработка ошибки цвета стикера
                    if (endpoint == "sticky_notes" and 
                        error_details.get('code') == '2.0703' and
                        'style.fillColor' in str(error_details)):
                        
                        # Извлекаем неправильный цвет из ошибки
                        context = error_details.get('context', {})
                        fields = context.get('fields', [])
                        for field in fields:
                            if field.get('field') == 'style.fillColor':
                                message = field.get('message', '')
                                # Ищем цвет в сообщении типа "Unexpected value [#E0E0E0]"
                                import re
                                color_match = re.search(r'\[([#\w]+)\]', message)
                                if color_match:
                                    wrong_color = color_match.group(1)
                                    print(f"    ❌ Неправильный цвет стикера: {wrong_color}")
                                    print(f"    💡 Для стикеров используйте только: gray, light_yellow, yellow, orange,")
                                    print(f"       light_green, green, dark_green, cyan, light_pink, pink, violet,")
                                    print(f"       red, light_blue, blue, dark_blue, black")
                                    return None
                    
                    # Для остальных ошибок показываем детали
                    print(f"    Детали: {error_details}")
                except:
                    print(f"    Ответ: {response.text[:200]}")
                return None
        except requests.exceptions.Timeout:
            print(f"⚠️  Таймаут для {endpoint}")
            return None
        except Exception as e:
            print(f"❌ Ошибка {endpoint}: {e}")
            return None
    
    def create_frame(self, title: str, x: float, y: float, 
                    width: float, height: float) -> Optional[str]:
        """Создает рамку"""
        data = {
            "data": {"title": title, "type": "freeform"},
            "style": {"fillColor": "#ffffff"},
            "position": {"x": x, "y": y},
            "geometry": {"width": width, "height": height}
        }
        return self.api_call("frames", data)
    
    def create_shape(self, name: str, x: float, y: float,
                    width: float, height: float, 
                    color: str = "#4169E1", shape: str = "rectangle") -> Optional[str]:
        """Создает фигуру"""
        data = {
            "data": {"shape": shape, "content": name},
            "style": {
                "fillColor": color,
                "fontSize": "14",
                "textAlign": "center",
                "textAlignVertical": "middle",
                "borderColor": "#1a1a1a",
                "borderWidth": "2",
                "color": "#ffffff" if color not in ["#FFFF00", "#FFD700"] else "#000000"
            },
            "position": {"x": x, "y": y},
            "geometry": {"width": width, "height": height}
        }
        
        result = self.api_call("shapes", data)
        if result:
            self.elements[name] = result  # Сохраняем для связей
        return result
    
    def create_sticky(self, text: str, x: float, y: float, 
                     color: str = "#FFFF99") -> Optional[str]:
        """Создает стикер"""
        # Конвертируем HEX цвета в допустимые значения Miro
        color_map = {
            "#FFE4E4": "light_pink",
            "#FFE4CC": "orange", 
            "#E6F3FF": "light_blue",
            "#E6FFE6": "light_green",
            "#E0E0E0": "gray",
            "#FFFF99": "light_yellow",
            "#FFFF00": "yellow",
            "#FFD700": "yellow"
        }
        
        miro_color = color_map.get(color, "light_yellow")
        
        data = {
            "data": {
                "content": text,
                "shape": "square"
            },
            "style": {
                "fillColor": miro_color,
                "textAlign": "left",
                "textAlignVertical": "top"
            },
            "position": {"x": x, "y": y},
            "geometry": {"width": 200}
        }
        return self.api_call("sticky_notes", data)
    
    def create_text(self, content: str, x: float, y: float, 
                   size: str = "14") -> Optional[str]:
        """Создает текст"""
        data = {
            "data": {"content": content},
            "style": {"fontSize": size, "color": "#000000"},
            "position": {"x": x, "y": y}
        }
        return self.api_call("texts", data)
    
    def create_connector(self, start_name: str, end_name: str, 
                        label: str = "") -> Optional[str]:
        """Создает связь между элементами"""
        start_id = self.elements.get(start_name)
        end_id = self.elements.get(end_name)
        
        if not start_id or not end_id:
            print(f"  ⚠️  Не могу связать '{start_name}' -> '{end_name}'")
            return None
        
        data = {
            "startItem": {"id": start_id},
            "endItem": {"id": end_id},
            "style": {
                "strokeColor": "#2D2D2D",
                "strokeWidth": "2",
                "endStrokeCap": "stealth"
            }
        }
        
        if label:
            data["captions"] = [{
                "content": label,
                "position": 0.5,
                "textAlignVertical": "middle"
            }]
        
        return self.api_call("connectors", data)
