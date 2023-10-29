def encrypt(text, shift, alphabet_size):
    encrypted = ""
    for char in text:
        if char.isalpha():
            encrypted += chr((ord(char) + shift - 65) % alphabet_size + 65)
        else:
            encrypted += char
    return encrypted

def decrypt(text, shift, alphabet_size):
    decrypted = ""
    for char in text:
        if char.isalpha():
            char_code = ord(char)
            base = ord('a') if char.islower() else ord('A')
            decrypted += chr((char_code - base - shift) % alphabet_size + base)
        else:
            decrypted += char
    return decrypted