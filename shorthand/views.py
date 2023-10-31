from django.shortcuts import render


def encode_text(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        encoded_text = encode_with_spaces(text)
        return render(request, 'shorthand/encoded_text.html', {'encoded_text': encoded_text})
    return render(request, 'shorthand/encode_text.html')


def encode_with_spaces(text):
    encoded_text = ''
    for char in text:
        encoded_text += char + ' '
    return encoded_text