import os
import sys
import ollama
from PIL import ImageGrab


def get_image_path_from_clipboard() -> str | None:
    image = ImageGrab.grabclipboard()
    if isinstance(image, ImageGrab.Image.Image):
        print("Found image in clipboard, saving it as a file")
        path = "./clipboard_image.png"
        image.save(path)
        print("Image saved as 'clipboard_image.png'")
        return path
    else:
        print("No image in clipboard.")
        return None


def process_image(question: str = 'explain this image'):
    image_path = get_image_path_from_clipboard()
    if not image_path:
        print("No image found in clipboard")
        return
    try:
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
    except Exception as e:
        print(f"Error during chat: {e}")
    finally:
        try:
            os.remove(image_path)
            print("Image removed")
        except Exception as e:
            print(f"Error removing temporary image file: {e}")
            pass


def main(argv):
    if len(argv) > 2:
        print("Usage: python look-here.py [optional_question]")
        return
    question = argv[1] if len(argv) == 2 else None
    process_image(question)

if __name__ == '__main__':
    main(sys.argv)


