from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image

# Функция для кодирования сообщения в конце строки изображения
def encode_end_of_line(request):
    if request.method == 'POST':
        image_path = 'image.png'  # Путь к исходному изображению
        message = request.POST.get('message')  # Получаем сообщение из запроса
        img = Image.open(image_path)  # Открываем изображение для кодирования
        message += "!"
        # Конвертируем сообщение в двоичную последовательность
        binary_message = ''.join(format(ord(char), '08b') for char in message)

        # Получаем размеры изображения
        width, height = img.size

        # Вставляем маркеры конца строки в двоичное сообщение
        encoded_message = ''
        for i, bit in enumerate(binary_message):
            encoded_message += bit
            # Вставляем маркер конца строки в конце каждой строки изображения
            if (i + 1) % width == 0:
                encoded_message += format(height, '08b')  # Используем высоту в качестве маркера конца строки

        # Вставляем двоичное сообщение в изображение
        pixel_index = 0
        for bit in encoded_message:
            pixel = img.getpixel((pixel_index % width, pixel_index // width))
            r, g, b, a = pixel

            # Обновляем младший бит синего канала битом двоичного сообщения
            if bit == '1':
                b |= 1
            else:
                b &= 254

            # Обновляем пиксель измененными значениями RGB
            img.putpixel((pixel_index % width, pixel_index // width), (r, g, b))
            pixel_index += 1

        # Сохраняем закодированное изображение
        encoded_image_path = 'encoded_image.png'
        img.save(encoded_image_path)

        # Возвращаем кодированное изображение в ответе HTTP
        with open(encoded_image_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='image/png')
            response['Content-Disposition'] = 'attachment; filename="encoded_image.png"'
            return response

    return render(request, 'shorthand/encode.html')


# Функция для декодирования сообщения из конца строки изображения
from PIL import Image
from django.http import JsonResponse

def decode_end_of_line(request):
    if request.method == 'POST' and 'image' in request.FILES:
        image = request.FILES['image']
        img = Image.open(image)  # Open the uploaded image
        width, height = img.size

        binary_message = ''
        end_of_line_marker = format(height, '08b')
        for y in range(height):
            for x in range(width):
                pixel = img.getpixel((x, y))
                if isinstance(pixel, int):
                    bit = pixel & 1
                else:
                    if len(pixel) == 3:  #RGB
                        r, g, b = pixel
                        bit = b & 1
                    else:  #RGBA
                        r, g, b, a = pixel
                        bit = b & 1
                binary_message += str(bit)
                if len(binary_message) >= 8 and binary_message[-8:] == end_of_line_marker:
                    binary_message = binary_message[:-8]
                    break


        decoded_message = ''
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i+8]
            if byte:
                decoded_message += chr(int(byte, 2))

        exclamation_index = decoded_message.find('!')

        # Extract the message before the exclamation mark
        extracted_message = decoded_message[:exclamation_index + 1]

        return HttpResponse(extracted_message[:-1])


    return render(request, 'shorthand/decode.html')