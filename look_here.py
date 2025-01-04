import os
import ollama
from ui import ui
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


def process_image(question: None | str = 'explain this image'):
    image_path = get_image_path_from_clipboard()
    if not image_path:
        raise Exception("No image found in clipboard")
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
            if os.getenv('CONSOLE'):
                print(message['message']['content'], end='', flush=True)
            yield message['message']['content']
    except Exception as e:
        print(f"Error during chat: {e}")
    finally:
        try:
            os.remove(image_path)
            print("Image removed")
        except Exception as e:
            print(f"Error removing temporary image file: {e}")

if __name__ == '__main__':
    ui.main()


