from main import bot

def download_image(image_file: list) -> list:
    new_image_file = list()
    for image in image_file:
        image_id = bot.download_file(file_path=image)
        new_image_file.append(image_id)
    return new_image_file