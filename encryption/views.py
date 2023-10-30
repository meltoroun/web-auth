from django.shortcuts import render
from django.http import HttpResponse
from encryption.utils import encrypt, decrypt

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import io

ALPHABET_POWER = 26


def encrypt_file(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        key = int(request.POST['key'])

        encrypted_text = ''
        with io.BytesIO(myfile.read()) as file:
            lines = file.readlines()
            for line in lines:
                stripped_line = line.strip().decode('utf-8')  # декодирование из байтов в текст
                for char in stripped_line:
                    if char.isalpha():
                        encrypted_text += chr((ord(char) + key - 65) % ALPHABET_POWER + 65)
                    else:
                        encrypted_text += char

        with open(myfile.name + '.cry', 'wt', encoding='utf-8') as encrypted_file:
            encrypted_file.write(encrypted_text)

        return render(request, 'encryption/encryption_success.html', {
            'encrypted_file': encrypted_file
        })
    return render(request, 'encryption/encryption_form.html')


def decrypt_file(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        key = int(request.POST['key'])

        decrypted_text = ''
        with io.BytesIO(myfile.read()) as file:
            lines = file.readlines()
            for line in lines:
                stripped_line = line.strip().decode('utf-8')  # декодирование из байтов в текст
                for char in stripped_line:
                    if char.isalpha():
                        char_code = ord(char)
                        base = ord('a') if char.islower() else ord('A')
                        decrypted_text += chr((char_code - base - key) % ALPHABET_POWER + base)
                    else:
                        decrypted_text += char

        with open(myfile.name.split('.')[0] + '.txt', 'wt', encoding='utf-8') as decrypted_file:
            decrypted_file.write(decrypted_text)

        return render(request, 'encryption/decryption_success.html', {
            'decrypted_file': decrypted_file
        })
    return render(request, 'encryption/decryption_form.html')
