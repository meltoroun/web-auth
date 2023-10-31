from django.shortcuts import render
import pyDes
import base64

def encrypt_file(file_path, key):
    cipher = pyDes.des(key.encode('utf-8'), pyDes.ECB, pad=None, padmode=pyDes.PAD_PKCS5)
    with open(file_path, 'rb') as file:
        plain_text = file.read()
        cipher_text = cipher.encrypt(plain_text)
        encrypted_file_path = file_path + '.encrypted'
        with open(encrypted_file_path, 'wb') as encrypted_file:
            encrypted_file.write(base64.b64encode(cipher_text))
    return encrypted_file_path


def decrypt_file(file_path, key):
    cipher = pyDes.des(key.encode('utf-8'), pyDes.ECB, pad=None, padmode=pyDes.PAD_PKCS5)
    with open(file_path, 'rb') as encrypted_file:
        cipher_text = base64.b64decode(encrypted_file.read())
        plain_text = cipher.decrypt(cipher_text)
        decrypted_file_path = file_path.replace('.encrypted', '.decrypted')
        with open(decrypted_file_path, 'wb') as decrypted_file:
            decrypted_file.write(plain_text)
    return decrypted_file_path


def file_operation(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
            key = request.POST['key']
            action = request.POST['action']
            file_path = handle_uploaded_file(uploaded_file)

            if action == 'encrypt':
                result_file = encrypt_file(file_path, key)
                result = f"Файл успешно зашифрован! Сохранен как {result_file}"
            elif action == 'decrypt':
                result_file = decrypt_file(file_path, key)
                result = f"Файл успешно расшифрован! Сохранен как {result_file}"
            else:
                result = "Действие не выбрано."

            return render(request, 'encryptionDES/encryptionDES.html', {'result': result})

    return render(request, 'encryptionDES/encryptionDES.html')


def handle_uploaded_file(file):
    file_path = 'uploaded_files/' + file.name
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return file_path