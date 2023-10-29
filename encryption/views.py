from django.shortcuts import render
from django.http import HttpResponse
from encryption.utils import encrypt, decrypt

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage


# Constants
ALPHABET_POWER = 26
def encrypt_file(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        key = int(request.POST['key'])

        encrypted_text = ''
        for line in myfile:
            for char in line:
                ascii_val = int(char)
                encrypted_char = chr((ascii_val + key) % ALPHABET_POWER)
                encrypted_text += encrypted_char

        # Save encrypted text to a new file
        with open(myfile.name.split('.')[0] + '.cry', 'w') as encrypted_file:
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
        for line in myfile:
            for char in line:
                ascii_val = int(char)
                decrypted_char = chr((ascii_val - key) % ALPHABET_POWER)
                decrypted_text += decrypted_char

        # Save decrypted text to a new file
        with open(myfile.name.split('.')[0] + '.txt', 'w') as decrypted_file:
            decrypted_file.write(decrypted_text)

        return render(request, 'encryption/decryption_success.html', {
            'decrypted_file': decrypted_file
        })
    return render(request, 'encryption/decryption_form.html')
