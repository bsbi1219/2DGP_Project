from pico2d import load_image

class TileSet:
    def __init__(self, image_path, tile_w, tile_h):
        self.image = load_image(image_path)
        self.tile_w = tile_w
        self.tile_h = tile_h
        self.cols = max(1, self.image.w // tile_w)
        self.rows = max(1, self.image.h // tile_h)

    def draw(self, index, x, y):
        if index is None or index < 0:
            return
        col = index % self.cols
        row = index // self.cols
        left = col * self.tile_w
        bottom = self.image.h - (row + 1) * self.tile_h
        cx = x + self.tile_w // 2
        cy = y + self.tile_h // 2
        self.image.clip_draw(left, bottom, self.tile_w, self.tile_h, cx, cy)



class TileSetManager:
    def __init__(self):
        # tilesets: name -> TileSet
        self.tilesets = {}
        # index_map: list of (start, end, name) for global index resolution
        self.index_map = []
        self.total_tiles = 0

    def add_tileset(self, name, image_path, tile_w, tile_h):
        """
        등록하면 해당 타일셋의 전역 시작 인덱스(start)를 반환합니다.
        """
        ts = TileSet(image_path, tile_w, tile_h)
        start = self.total_tiles
        count = ts.cols * ts.rows
        self.tilesets[name] = ts
        self.index_map.append((start, start + count - 1, name))
        self.total_tiles += count
        return start

    def resolve_index(self, global_index):
        """
        전역 인덱스를 (TileSet, local_index)로 변환.
        """
        if global_index is None or global_index < 0:
            return None, None
        for start, end, name in self.index_map:
            if start <= global_index <= end:
                local = global_index - start
                return self.tilesets[name], local
        raise ValueError(f"global_index {global_index} out of range")

    def resolve_entry(self, entry):
        """
        entry는 다음 중 하나:
         - None 또는 음수 -> 비어있음
         - 정수 -> 전역 인덱스
         - (tileset_name, local_index) 튜플 -> 직접 지정
        반환: (TileSet or None, local_index or None)
        """
        if entry is None:
            return None, None
        if isinstance(entry, int):
            return self.resolve_index(entry)
        if (isinstance(entry, (tuple, list)) and len(entry) == 2):
            name, idx = entry
            ts = self.tilesets.get(name)
            if ts is None:
                raise KeyError(f"tileset '{name}' not registered")
            return ts, idx
        raise TypeError("map entry must be None, int, or (tileset_name, local_index)")



class TileMap:
    def __init__(self, manager: TileSetManager, map_grid, tile_w=None, tile_h=None):
        """
        manager: TileSetManager 인스턴스
        map_grid: 2D 리스트. 각 항목은 None, int(전역 인덱스), 또는 (tileset_name, local_index)
        tile_w, tile_h: (선택) 기본 타일 크기. 단, 각 타일셋이 자체 크기를 사용함.
        """
        self.manager = manager
        self.map = map_grid
        self.rows = len(map_grid)
        self.cols = len(map_grid[0]) if self.rows else 0
        self.tile_w = tile_w
        self.tile_h = tile_h

    def draw(self, cam_x=0, cam_y=0):
        for r, row in enumerate(self.map):
            for c, entry in enumerate(row):
                try:
                    ts, local_idx = self.manager.resolve_entry(entry)
                except (KeyError, ValueError, TypeError):
                    continue
                if ts is None or local_idx is None:
                    continue
                # 각 타일셋의 크기대로 그리기. 화면 y는 맵의 0행이 최상단이라 가정
                screen_x = c * ts.tile_w - cam_x
                screen_y = (self.rows - 1 - r) * ts.tile_h - cam_y
                ts.draw(local_idx, screen_x, screen_y)
