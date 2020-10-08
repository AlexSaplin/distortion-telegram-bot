import io

import Augmentor
import numpy as np
import telebot
from PIL import Image

TOKEN = '<insert your token>'

bot = telebot.TeleBot(token=TOKEN)


def fetch_photo(message):
    file_id = message.photo[0].file_id
    file_info = bot.get_file(file_id)
    data = bot.download_file(file_info.file_path)
    image_data = io.BytesIO(data)
    image = Image.open(image_data)
    return image


def distort_photo(image):
    images = [[np.asarray(image)]]
    pipeline = Augmentor.DataPipeline(images)
    pipeline.random_distortion(probability=1, grid_width=4, grid_height=4, magnitude=40)
    prepared_images = pipeline.sample(1)
    ready_image = Image.fromarray(prepared_images[0][0])
    return ready_image


@bot.message_handler(content_types=['photo'])
def send_message(message):
    photo = fetch_photo(message)
    updated_photo = distort_photo(photo)
    output_file = io.BytesIO()
    updated_photo.save(output_file, format='jpeg')
    output_file.seek(0)
    bot.send_photo(message.chat.id, output_file)


@bot.message_handler(func=lambda x: True)
def send_message(message):
    bot.send_message(message.chat.id, 'Я умею только в фотки')


bot.polling(none_stop=True)
