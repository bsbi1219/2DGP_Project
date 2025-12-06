from pico2d import *

import game_framework
import game_world

from hero import Hero
from map_1 import Map
from map_2 import Map2
from camera import Camera
from slime import Slime
from goblin import Goblin
from flower import Flower
from wall import Wall
from interact import InteractZone
from sheep import Sheep
import ui

hero = None
boss = None
camera = None
map = None
map2 = None
ui_state = None

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            import pause_state
            game_framework.push_mode(pause_state)
        else:
            hero.handle_event(event)

def go_to_map(map_id):
    global map, camera, hero

    for obj in list(game_world.world[1]):
        from slime import Slime
        from goblin import Goblin
        from flower import Flower
        from sheep import Sheep
        from interact import InteractZone
        from boss import Boss

        if isinstance(obj, (Slime, Goblin, Flower, Sheep, InteractZone)):
            game_world.remove_collision_object(obj)
            game_world.remove_object(obj)

    for obj in list(game_world.world[0]):  # 맵 + 벽 삭제
        game_world.remove_collision_object(obj)
        game_world.remove_object(obj)

    if map_id == 1:
        map = Map()
    elif map_id == 2:
        map = Map2()

    game_world.map = map
    game_world.add_object(map, 0)

    hero = game_world.hero

    game_world.collision_pairs.clear()
    game_world.add_collision_pair('hero_body:wall', hero, None)

    game_world.interacts = []
    if map_id == 1:
        zones = [
            InteractZone(89, 655, 30, 50, "'보스방 열쇠'를 얻었다!", after_message="이미 얻은 열쇠이다.", give_item=lambda: hero.get_key()),
            InteractZone(1170, 661, 35, 45, "상자를 열었다. 30G를 얻었다!", after_message="상자는 비어있다.", give_item=lambda: hero.get_gold(30)),
            InteractZone(640, 20, 40, 30, "상자를 열었다. 70G를 얻었다!", after_message="상자는 비어있다.", give_item=lambda: hero.get_gold(70)),
            InteractZone(1164, 845, 40, 40, "수상한 인형을 발견했다... 조금 강해진 기분이다.", after_message="평범한 인형이다.", give_item=lambda: hero.get_atk(10)),
            InteractZone(215, 307, 20, 40, "무엇을 사러 왔어?", open_store=True),
            InteractZone(975, 239, 20, 40, "보스방 열쇠를 사용했다.", after_message="열쇠가 필요한 것 같다...",
                         condition=lambda hero: hero.item_boss_key, on_pass=lambda hero: (hero.open_boss_door(), go_to_map(2), hero.set_pos(630, 50)))
        ]

        for iz in zones:
            game_world.interacts.append(iz)
            game_world.add_object(iz, 1)

    if map_id == 1:
        # 슬라임 생성
        game_world.add_collision_pair('slime:wall', None, None)
        slimes = [Slime() for _ in range(20)]
        game_world.add_objects(slimes, 1)
        for s in slimes:
            game_world.add_collision_pair('slime:wall', s, None)

        # 고블린 생성
        game_world.add_collision_pair('goblin:wall', None, None)
        goblins = [Goblin() for _ in range(20)]
        game_world.add_objects(goblins, 1)
        for g in goblins:
            game_world.add_collision_pair('goblin:wall', g, None)

        # 양(상점) 생성
        sheep = Sheep()
        game_world.add_object(sheep, 1)

        # 식인꽃
        flowers = [Flower() for _ in range(20)]
        game_world.add_objects(flowers, 1)

        # hero vs 몬스터 충돌쌍
        for slime in slimes:
            game_world.add_collision_pair('hero_body:slime', hero, slime)
            game_world.add_collision_pair('hero_attack:slime', hero, slime)

        for goblin in goblins:
            game_world.add_collision_pair('hero_body:goblin', hero, goblin)
            game_world.add_collision_pair('hero_attack:goblin', hero, goblin)

        for flower in flowers:
            game_world.add_collision_pair('hero_body:flower', hero, flower)
            game_world.add_collision_pair('hero_attack:flower', hero, flower)

    if map_id == 2:
        ui_boss_hp = ui.BossHPUI()
        game_world.add_object(ui_boss_hp, 3)
        boss = Boss()
        game_world.boss = boss
        game_world.add_object(boss, 1)
        game_world.add_collision_pair('boss:wall', boss, None)
        game_world.add_collision_pair('goblin:wall', None, None)
        goblins = [Goblin() for _ in range(20)]
        game_world.add_objects(goblins, 1)
        game_world.add_collision_pair('hero_body:boss', hero, boss)
        game_world.add_collision_pair('hero_attack:boss', hero, boss)
        for g in goblins:
            game_world.add_collision_pair('boss:wall', g, None)
            game_world.add_collision_pair("hero_body:goblin", hero, g)
            game_world.add_collision_pair("hero_attack:goblin", hero, g)

    game_world.add_collision_pair('hero_body:wall', hero, None)
    for left, bottom, right, top in map.collision_rects:
        wall = Wall(left, bottom, right, top)
        game_world.add_object(wall, 0)
        game_world.add_collision_pair('hero_body:wall', None, wall)

        if map_id == 1:
            game_world.add_collision_pair('slime:wall', None, wall)
            game_world.add_collision_pair('goblin:wall', None, wall)

        if map_id == 2:
            game_world.add_collision_pair('boss:wall', None, wall)
            game_world.add_collision_pair('goblin:wall', None, wall)

    camera = Camera(get_canvas_width(), get_canvas_height(),
                    world_w=map.map_width, world_h=map.map_height, scale=6.0)

    game_world.camera = camera

def init():
    global hero, map, map2, camera, ui_state

    hero = Hero()
    game_world.add_object(hero, 1)
    game_world.hero = hero

    ui_state = ui.StateUI()
    game_world.add_object(ui_state, 3)

    go_to_map(1)

def update():
    game_world.update()
    game_world.handle_collisions()
    camera.update(hero.x, hero.y)

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()

def pause(): pass

def resume():
    game_world.hero.keys_pressed.clear()
    game_world.hero.vx = 0
    game_world.hero.vy = 0