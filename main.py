import os
import sys

import ollama

from PIL import ImageGrab


def get_image_path_from_clipboard():
    # Get the image from the clipboard
    image = ImageGrab.grabclipboard()

    if isinstance(image, ImageGrab.Image.Image):
        print("Image copied to clipboard!")
        # Save or process the image as needed
        path = "./clipboard_image.png"
        image.save(path)
        print("Image saved as 'clipboard_image.png'")
        return path
    else:
        print("No image in clipboard.")
        return None


def process_image(question=None):
    image_path: str = ""
    clip_path = get_image_path_from_clipboard()
    if clip_path is not None:
        image_path = clip_path
    question = question or 'explain this image'
    response = ollama.chat(
        model='llama3.2-vision',
        stream=True,
        messages=[{
            'role': 'user',
            'content': question,
            'images': [image_path],
        }]
    )
    for message in response:
        print(message['message']['content'], end='', flush=True)
    try:
        os.remove(image_path)
    except FileNotFoundError:
        print("File not found")
        pass


def main(argv):
    process_image(*argv[1:])
if __name__ == '__main__':
    main(sys.argv)


