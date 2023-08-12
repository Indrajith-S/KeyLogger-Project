from pynput.mouse import Listener
import logging

logging.basicConfig(filename="mouse_log.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')

def on_click(x, y, button, pressed):
    if pressed:
        logging.info('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))

with Listener(on_click=on_click) as listener:
    listener.join()