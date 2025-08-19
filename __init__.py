"""
Miro Engine Package
Модульная система для создания диаграмм в Miro
"""

from .miro_api import MiroAPI
from .instruction_parser import InstructionParser
from .command_executor import CommandExecutor

__version__ = "1.0.0"
__all__ = ["MiroAPI", "InstructionParser", "CommandExecutor"]
