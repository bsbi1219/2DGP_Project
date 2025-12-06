world = [[] for _ in range(5)] # layers for game objects

def add_object(o, depth = 0):
    world[depth].append(o)


def add_objects(ol, depth = 0):
    world[depth] += ol

def all_objects():
    for layer in world:
        for o in layer:
            yield o

def update():
    for layer in world:
        for o in layer:
            o.update()


def render():
    for layer in world:
        for o in layer:
            o.draw()

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            return
    raise ValueError('Cannot delete non existing object')


def clear():
    global world

    for layer in world:
        layer.clear()


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

collision_pairs = {}
def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        print(f'Added new group {group}')
        collision_pairs[group] = [ [], [] ]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)


def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                # hero_attack 그룹은 attack_bb로 판정
                if group.startswith('hero_attack'):
                    # a 가 hero (공격자) 라고 가정
                    if not hasattr(a, 'get_attack_bb') or not hasattr(b, 'get_bb'):
                        continue

                    attack_bb = a.get_attack_bb()
                    if attack_bb is None:
                        continue  # 공격 프레임이 아닐 때

                    ax1, ay1, ax2, ay2 = attack_bb
                    bx1, by1, bx2, by2 = b.get_bb()

                    # 사각형 겹침 체크
                    if ax1 > bx2 or ax2 < bx1 or ay2 < by1 or ay1 > by2:
                        continue

                    # 여기까지 왔으면 "공격 박스와 슬라임 박스가 겹친 상태"
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)
                else:
                    # 나머지 그룹은 기존 body bb로 처리
                    if not hasattr(a, 'get_bb') or not hasattr(b, 'get_bb'):
                        continue
                    if collide(a, b):
                        a.handle_collision(group, b)
                        b.handle_collision(group, a)

# collision pair에 들어있는 모든 o를 제거
def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)