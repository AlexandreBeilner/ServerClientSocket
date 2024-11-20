import base64
import cv2
import numpy as np
import threading


class Video:
    def __init__(self):
        self.cap = None
        self.running = False
        self.video_thread = None
        self.last_frame = None
        self.video_frame = None
        self.is_render_video = False
        self.render_thread = None  # Adicione uma referência à thread de renderização

    def start(self, sio):
        self.cap = cv2.VideoCapture(0)
        self.running = True
        self.video_thread = threading.Thread(target=self.capture_video, args=(sio,))
        self.video_thread.start()

    def capture_video(self, sio):
        while self.cap.isOpened() and self.running:
            ret, frame = self.cap.read()
            if not ret:
                break

            _, buffer = cv2.imencode('.jpg', frame)
            frame_data = base64.b64encode(buffer).decode('utf-8')
            sio.emit('video_frame', frame_data)
            self.display_frame(frame_data)

        self.cap.release()
        cv2.destroyAllWindows()

    def stop(self):
        self.running = False
        if self.video_thread is not None:
            self.video_thread.join()

    def display_frame(self, data):
        frame_data = base64.b64decode(data)
        np_array = np.frombuffer(frame_data, dtype=np.uint8)
        frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        cv2.imshow('Video Stream', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.is_render_video = False
            self.stop_render_video()
            self.stop()

    def render_video(self):
        self.is_render_video = True
        self.render_thread = threading.Thread(target=self._render_video_loop)
        self.render_thread.start()

    def _render_video_loop(self):
        while self.is_render_video:
            if self.last_frame != self.video_frame:
                self.display_frame(self.video_frame)
                self.last_frame = self.video_frame

        cv2.destroyAllWindows()

    def stop_render_video(self):
        self.is_render_video = False
        if self.render_thread is not None:
            self.render_thread.join()

