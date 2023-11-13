import io
import os
from django.http import HttpResponse
from django.shortcuts import render


ALPHABET_POWER = 26  # Задание константы для длины алфавита (в данном случае английского)

# Функция для шифрования файла
def encrypt_file(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']  # Получение загруженного файла из запроса
        key = int(request.POST['key'])  # Получение ключа шифрования из запроса

        encrypted_text = ''
        with io.BytesIO(myfile.read()) as file:  # Использование байтового потока для чтения файла
            lines = file.readlines()  # Чтение всех строк из файла
            for line in lines:
                stripped_line = line.strip().decode('utf-8')  # Преобразование байтов строки в обычную строку
                # в кодировке UTF-8
                for char in stripped_line:
                    if char.isalpha():
                        encrypted_text += chr((ord(char) + key - 65) % ALPHABET_POWER + 65)  # Шифрование символов
                    else:
                        encrypted_text += char

        encrypted_file_path = os.path.join(myfile.name + '.cry')  # Формирование пути для сохранения
        # зашифрованного файла

        with open(encrypted_file_path, 'wt', encoding='utf-8') as encrypted_file:
            encrypted_file.write(encrypted_text)  # Запись зашифрованного текста в файл

        with open(encrypted_file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='text/plain')  # Формирование HTTP-ответа с
            # зашифрованным файлом
            response['Content-Disposition'] = f'attachment; filename="{myfile.name}.cry"'  # Задание заголовка
            # Content-Disposition для скачивания файла
            return response

    return render(request, 'encryption/encryption_form.html')  # Отображение формы шифрования

# Функция для дешифрования файла
def decrypt_file(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']  # Получение загруженного файла из запроса
        key = int(request.POST['key'])  # Получение ключа дешифрования из запроса

        decrypted_text = ''
        with io.BytesIO(myfile.read()) as file:  # Использование байтового потока для чтения файла
            lines = file.readlines()  # Чтение всех строк из файла
            for line in lines:
                stripped_line = line.strip().decode('utf-8')  # Преобразование байтов
                # строки в обычную строку в кодировке UTF-8
                for char in stripped_line:
                    if char.isalpha():
                        char_code = ord(char)
                        base = ord('a') if char.islower() else ord('A')
                        decrypted_text += chr((char_code - base - key) % ALPHABET_POWER + base)  # Дешифрование
                        # символов
                    else:
                        decrypted_text += char

        decrypted_file_path = os.path.join(myfile.name.split('.')[0] + '.txt')  # Формирование пути
        # для сохранения дешифрованного файла

        with open(decrypted_file_path, 'wt', encoding='utf-8') as decrypted_file:
            decrypted_file.write(decrypted_text)  # Запись дешифрованного текста в файл

        with open(decrypted_file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='text/plain')  # Формирование HTTP-ответа с
            # дешифрованным файлом
            response['Content-Disposition'] = f'attachment; filename="{myfile.name.split(".")[0]}.txt"'  # Задание
            # заголовка Content-Disposition для скачивания файла
            return response

    return render(request, 'encryption/decryption_form.html')  # Отображение формы дешифрования