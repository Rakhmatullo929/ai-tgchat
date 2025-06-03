#!/usr/bin/env python3
"""
Скрипт для остановки всех процессов SmartGroupBot
"""

import subprocess
import sys
import signal
import time

def find_processes():
    """Находит все процессы, связанные с ботом"""
    processes = []
    
    try:
        # Ищем процессы Python с ботом
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        
        for line in lines:
            if 'python' in line.lower() and ('main_bot.py' in line or 'run_all.py' in line or 'start_simple.py' in line):
                parts = line.split()
                if len(parts) > 1:
                    try:
                        pid = int(parts[1])
                        processes.append((pid, line))
                    except ValueError:
                        continue
    except Exception as e:
        print(f"❌ Ошибка поиска процессов: {e}")
    
    return processes

def stop_process(pid, description):
    """Останавливает процесс по PID"""
    try:
        print(f"🛑 Остановка процесса {pid}: {description[:60]}...")
        
        # Сначала пробуем мягко остановить
        subprocess.run(['kill', '-TERM', str(pid)], check=False)
        time.sleep(2)
        
        # Проверяем, остановился ли процесс
        result = subprocess.run(['kill', '-0', str(pid)], capture_output=True)
        if result.returncode == 0:
            # Если не остановился, принудительно завершаем
            print(f"💀 Принудительное завершение процесса {pid}")
            subprocess.run(['kill', '-KILL', str(pid)], check=False)
        
        print(f"✅ Процесс {pid} остановлен")
        
    except Exception as e:
        print(f"❌ Ошибка остановки процесса {pid}: {e}")

def main():
    """Основная функция"""
    print("🔍 Поиск процессов SmartGroupBot...")
    
    processes = find_processes()
    
    if not processes:
        print("✅ Активных процессов не найдено")
        return
    
    print(f"📋 Найдено процессов: {len(processes)}")
    
    for pid, description in processes:
        stop_process(pid, description)
    
    print("\n🏁 Все процессы остановлены")

if __name__ == "__main__":
    main() 