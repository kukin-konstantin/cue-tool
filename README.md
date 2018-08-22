## Описание
Python скрипт для нарезки целых flac, ape, wv файлов в группу файлов flac.

Внимание!
Удаляет исходный музыкальный файл.

## Необходимые пакеты
Python 2.7

Может запускаться в linux и в Windows 10 в bash консоли.

Необходимо поставить пакеты(Ubuntu):

    sudo apt-get install flac
    sudo apt-get install monkeys-audio
    sudo apt-get install wavpack
    sudo apt-get install shntool

## Тестирование

Чтобы проверить правильность работы необходимо запустить test.py.
Скрипт проверит по хэш-функциям правильность работы кодирования.
В случае успеха будет выведена надпись:
"All tests were passed successful!"

## Запуск

Для создания дополнительных директорий, если музыкальные файлы лежат в одной директории:

    python reorg_files.py --path=path_to_directory

Для разделения целых файлов:
    
    python split.py --path=path_to_directory
 