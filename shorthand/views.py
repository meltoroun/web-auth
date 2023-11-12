from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
import random


def encode_end_of_line(request):
    if request.method == 'POST':
        image_path = 'image.png'
        message = request.POST.get('message')
        img = Image.open(image_path)

        # конвертируем сообщение в бинарный вид
        binary_message = ''.join(format(ord(char), '08b') for char in message)

        # получим значения по ширине/высоте
        width, height = img.size

        # Вставим маркеры конца строки в бинарное сообщение
        encoded_message = ''
        marker_index = 0
        for i, bit in enumerate(binary_message):
            encoded_message += bit
            if (i + 1) % width == 0:  # маркер конца строки в конце каждой строки
                encoded_message += format(height, '08b')  # высота в качестве маркера конца строки
                marker_index += 1

        # вставляем двоичное сообщение в изображение
        pixel_index = 0
        for bit in encoded_message:
            # Получить пиксель по текущему индексу
            pixel = img.getpixel((pixel_index % width, pixel_index // width))
            r, g, b, a = pixel

            # Обновляем младший бит синего канала битом двоичного сообщения
            if bit == '1':
                b |= 1
            else:
                b &= 254

            # Обновляем пиксель измененными значениями RGB.
            img.putpixel((pixel_index % width, pixel_index // width), (r, g, b))
            pixel_index += 1

        # сохраняем
        encoded_image_path = 'encoded_image.png'
        img.save(encoded_image_path)

        # Возвращаем закодированное изображение в качестве ответа HTTP
        with open(encoded_image_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='image/png')
            response['Content-Disposition'] = 'attachment; filename="encoded_image.png"'
            return response

    return render(request, 'shorthand/encode.html')


def decode_end_of_line(request):
    if request.method == 'POST' and 'image' in request.FILES:
        image = request.FILES['image']
        img = Image.open(image)
        width, height = img.size

        binary_message = ''
        end_of_line_marker = format(height, '08b')  # Используем высоту в качестве маркера конца строки

        # извлекаем двоичное сообщение из изображения
        for y in range(height):
            for x in range(width):
                pixel = img.getpixel((x, y))
                if isinstance(pixel, int):
                    bit = pixel & 1
                else:
                    if len(pixel) == 3:  # для rgb
                        r, g, b = pixel
                        bit = b & 1
                    else:  # RGBA
                        r, g, b, a = pixel
                        bit = b & 1
                binary_message += str(bit)

                # Проверка на маркер в конце строки
                if len(binary_message) >= 8 and binary_message[-8:] == end_of_line_marker:
                    binary_message = binary_message[:-8]  # удаляем маркер
                    break

        # Преобразуем двоичное сообщение в символы
        binary_chunks = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
        decoded_message = ''.join(chr(int(chunk, 2)) for chunk in binary_chunks)

        return HttpResponse(decoded_message)

    return render(request, 'shorthand/decode.html')

