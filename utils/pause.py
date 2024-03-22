import threading
import keyboard
import cv2 as cv
from .log import log

class Pause:
    def __init__(self, dev=False):
        self.dev = dev
        if self.dev:
            self.pause_event = threading.Event()
            self.last_key_pressed = None  # 记录最后按下的按键
            self.pause_event.clear()
            keyboard.on_press_key("F8", self.toggle_pause)
            keyboard.on_press_key("F9", self.continue_and_restart)
            keyboard.on_press_key("F10", self.continue_new_map)
            
        else:
            self.pause_event = None

    def toggle_pause(self, event):
        if not self.dev:
            return
        if self.pause_event.is_set():
            log.info("检测到按下'F8'，即将继续")
            self.pause_event.clear()
            self.last_key_pressed = 'F8'
        else:
            log.info("检测到按下'F8'暂停，将在下一个检测点自动暂停。按下'F8'继续 或 选中传送点后按下'F9'重新传送至地图")
            self.pause_event.set()
            self.last_key_pressed = 'F8'

    def continue_and_restart(self, event):
        if not self.dev:
            return
        if self.pause_event.is_set():
            log.info("检测到按下'F9'，即将重新传送至地图")
            self.pause_event.clear()
            self.last_key_pressed = 'F9'
            
    def continue_new_map(self, event):
        if not self.dev:
            return
        if self.pause_event.is_set():
            log.info("检测到按下'F10'，即将重跑map")
            self.pause_event.clear()
            self.last_key_pressed = 'F10'
    
    def _show_img(self, img: str):
        """展示图片

        Args:
            img (str): 图片地址
        """
        log.info(f"展示图片：{img}")
        image = cv.imread(img)
        if image is not None:
            cv.imshow('temp_point', image)
            while self.pause_event.is_set():
                cv.waitKey(1)

    def check_pause(self, dev: bool, last_point: str) -> str | bool:
        """检查是否暂停，暂停情况下返回取消暂停使用的按键

        Args:
            dev (bool): 开发者模式下允许暂停
            last_point (str): 最后传送点图片地址

        Returns:
            str | bool: 暂停取消时返回暂停取消的按键字符串'F10','F9','F8'，无暂停时返回False
        """

        if not self.dev:
            return False
        if dev:
            show = False
            press = False
            while self.pause_event.is_set():
                press = True
                if not show and last_point:
                    show = True
                    self._show_img(last_point)
            if press:
                cv.destroyAllWindows()
                return self.last_key_pressed
            else:
                return False
        else:
            return False
