# python
# 파일: `camera.py`

from pico2d import *

class Camera:
    def __init__(self, viewport_w, viewport_h, world_w=None, world_h=None, scale=1.0, lag=0.15):
        self.vw = float(viewport_w)
        self.vh = float(viewport_h)
        self.world_w = float(world_w) if world_w is not None else None
        self.world_h = float(world_h) if world_h is not None else None
        self.scale = float(scale)
        self.lag = float(lag)

        self.x = self.vw / 2.0 / self.scale
        self.y = self.vh / 2.0 / self.scale

    def set_scale(self, s):
        if s <= 0: return
        cx, cy = self.x, self.y
        self.scale = float(s)
        self.x, self.y = cx, cy
        self._clamp_position()

    def update(self, target_x, target_y):
        # 보정된 목표 (center)
        tx = float(target_x)
        ty = float(target_y)
        self.x += (tx - self.x) * self.lag
        self.y += (ty - self.y) * self.lag
        self._clamp_position()

    def _clamp_position(self):
        if self.world_w is None or self.world_h is None:
            return
        half_w = (self.vw / self.scale) / 2.0
        half_h = (self.vh / self.scale) / 2.0
        min_x = half_w
        max_x = max(self.world_w - half_w, min_x)
        min_y = half_h
        max_y = max(self.world_h - half_h, min_y)
        if self.x < min_x: self.x = min_x
        if self.x > max_x: self.x = max_x
        if self.y < min_y: self.y = min_y
        if self.y > max_y: self.y = max_y

    def world_to_screen(self, x, y):
        sx = (x - self.x) * self.scale + self.vw / 2.0
        sy = (y - self.y) * self.scale + self.vh / 2.0
        return sx, sy

    def screen_to_world(self, sx, sy):
        wx = (sx - self.vw / 2.0) / self.scale + self.x
        wy = (sy - self.vh / 2.0) / self.scale + self.y
        return wx, wy

    def scale_size(self, w, h):
        return w * self.scale, h * self.scale

    def draw_image(self, image, src_x, src_y, src_w, src_h, world_x, world_y, dest_w, dest_h):
        sx, sy = self.world_to_screen(world_x, world_y)
        dw, dh = self.scale_size(dest_w, dest_h)
        image.clip_draw(src_x, src_y, src_w, src_h, sx, sy, dw, dh)
