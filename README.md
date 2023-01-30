# main.py - точка входа
Основной скрипт.
Демонстрация алгоритма с Blender 2.91 Python API.
Алгоритм взят из книги "Алгоритмы. Справочник с примерами на C, C++, Java и Python", 2-е изд., Хейнеман Джордж, Поллис Гэри, Селков Стенли, 2017 (стра. 41).
Algorithm taken from book "Algorithms in a Nutshell", Second Edition, George T. Heineman, Gary Pollice, Stanley Selkow, 2016.

# 2 пути запуска скрипта:
1. В командной строке прописать:  
```blender --background --python main.py``` (где blender - исполняемый файл Blender).
2. В Blender открыть файл start.blend и нажать Run Script (Alt + P).

# Настройки в main.py
Переменной ```PATH_OUT``` задаем путь куда будут сохраняться изображения или анимация.  
Переменной ```NUM_OBJS``` задаем тип количество объектов.  
Если переменная ```ANIM = False``` то на выходе получим набор изображений, если ```True``` то получим анимацию.

# Требования
Blender 2.91

# plus.py
Реализация алгоритма в текстовом (консольном) режиме.

# demo (snap)
![](https://raw.githubusercontent.com/antonsrc/algorithm_demo/main/preview.jpg)
