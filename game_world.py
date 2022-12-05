# objects[0] : 바닥 계층
# objects[1] : 상위 계층
objects = [[], [], []]

collision_group = dict()


def add_object(o, depth):
    objects[depth].append(o)

def add_objects(ol, depth):
    objects[depth] += ol

def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            # 충돌그룹에서도 지워야 한다. 오브젝트를
            remove_collision_object(o)
            del o
            return

def all_objects():
    for layer in objects:
        for o in layer:
            yield o  # 제네레이터, 모든 객체들을 하나씩 넘겨준다.

def enemy_clear():
    while True:
        flag = False
        for o in all_objects():
            if o.type == 2 or o.type == 3 or o.type == 4 or o.type == 6:
                remove_object(o)
                flag = True
                break
        if flag == False:
            break

def clear():
    for o in all_objects():
        del o
    for layer in objects:
        layer.clear()


def add_collision_pairs(a, b, group):
    if group not in collision_group:
        collision_group[group] = [[], []]

    if a:
        if type(a) == list:
            collision_group[group][0] += a
        else:
            collision_group[group][0].append(a)

    if b:
        if type(b) == list:
            collision_group[group][1] += b
        else:
            collision_group[group][1].append(b)


def all_collision_pairs():
    for group, pairs in collision_group.items():
        for a in pairs[0]:
            for b in pairs[1]:
                yield a, b, group


def remove_collision_object(o):
    for pairs in collision_group.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        elif o in pairs[1]: pairs[1].remove(o)