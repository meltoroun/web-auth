from django.shortcuts import render
import pyDes
import base64


# Функция для шифрования файла
def encrypt_file(file_path, key):
    # Создание экземпляра DES шифра с использованием ключа
    cipher = pyDes.des(key.encode('utf-8'), pyDes.ECB, pad=None, padmode=pyDes.PAD_PKCS5)

    # Открытие файла для чтения
    with open(file_path, 'rb') as file:
        # Чтение содержимого файла
        plain_text = file.read()
        # Шифрование содержимого файла
        cipher_text = cipher.encrypt(plain_text)
        # Создание пути для сохранения зашифрованного файла
        encrypted_file_path = file_path + '.encrypted'
        # Запись зашифрованного текста в новый файл в кодировке base64
        with open(encrypted_file_path, 'wb') as encrypted_file:
            encrypted_file.write(base64.b64encode(cipher_text))
    # Возвращение пути к зашифрованному файлу
    return encrypted_file_path


# Функция для дешифрования файла
def decrypt_file(file_path, key):
    # Создание экземпляра DES шифра с использованием ключа
    cipher = pyDes.des(key.encode('utf-8'), pyDes.ECB, pad=None, padmode=pyDes.PAD_PKCS5)

    # Открытие зашифрованного файла для чтения
    with open(file_path, 'rb') as encrypted_file:
        # Чтение содержимого зашифрованного файла и декодирование из base64
        cipher_text = base64.b64decode(encrypted_file.read())
        # Дешифрование содержимого файла
        plain_text = cipher.decrypt(cipher_text)
        # Создание пути для сохранения расшифрованного файла
        decrypted_file_path = file_path.replace('.encrypted', '.decrypted')
        # Запись расшифрованного текста в новый файл
        with open(decrypted_file_path, 'wb') as decrypted_file:
            decrypted_file.write(plain_text)
    # Возвращение пути к расшифрованному файлу
    return decrypted_file_path


# Функция для обработки загруженного файла
def file_operation(request):
    # Проверка метода запроса
    if request.method == 'POST':
        # Проверка наличия файла в запросе
        if 'file' in request.FILES:
            # Получение загруженного файла и ключа из запроса
            uploaded_file = request.FILES['file']
            key = request.POST['key']
            action = request.POST['action']
            # Обработка загруженного файла и получение его пути
            file_path = handle_uploaded_file(uploaded_file)

            # Проверка выбранного действия (шифрование или дешифрование)
            if action == 'encrypt':
                # Выполнение шифрования файла
                result_file = encrypt_file(file_path, key)
                result = f"Файл успешно зашифрован! Сохранен как {result_file}"
            elif action == 'decrypt':
                # Выполнение дешифрования файла
                result_file = decrypt_file(file_path, key)
                result = f"Файл успешно расшифрован! Сохранен как {result_file}"
            else:
                result = "Действие не выбрано."

            return render(request, 'encryptionDES/encryptionDES.html', {'result': result})

    return render(request, 'encryptionDES/encryptionDES.html')


# Вспомогательная функция для сохранения загруженного файла на сервере
def handle_uploaded_file(file):
    file_path = 'uploaded_files/' + file.name
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return file_path

