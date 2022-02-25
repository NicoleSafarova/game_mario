import pygame
import os
import sys

FPS = 50
pygame.init()
n = input()
size = width, height = 800, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Инициализация игры")
screen.fill((0, 0, 0))
image = pygame.Surface([100, 100])
image.fill(pygame.Color("red"))
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpeg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename, m, place):
    if not m:
        filename = "data/" + filename
        # читаем уровень, убирая символы перевода строки
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        # и подсчитываем максимальную длину
        max_width = max(map(len, level_map))

        # дополняем каждую строку пустыми клетками ('.')
        lev = list(map(lambda x: x.ljust(max_width, '.'), level_map))
        for i in range(len(lev)):
            lev[i] = list(lev[i])
        return lev
    if place == "up":
        return [m[-1]] + m[:-1]
    elif place == "down":
        return m[1:] + [m[0]]
    elif place == "right":
        for i in range(len(m)):
            m[i] = m[i][1:] + [m[i][0]]
        return m
    elif place == "left":
        for i in range(len(m)):
            m[i] = [m[i][-1]] + m[i][:-1]
        return m


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

tile_width = tile_height = STEP = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)


# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def generate_level1(level):
    new_player = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)


world = load_level(n, [], "")
player, level_x, level_y = generate_level(world)


if __name__ == "__main__":
    start_screen()
    y = len(world) * 50
    x = len(world[0]) * 50
    screen = pygame.display.set_mode((x, y))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if player.rect.x - STEP > 0:
                        player.rect.x -= STEP
                    else:
                        world = load_level(n, world, "left")
                        generate_level1(world)

                if event.key == pygame.K_RIGHT:
                    if player.rect.x + STEP < x:
                        player.rect.x += STEP
                    else:
                        world = load_level(n, world, "right")
                        generate_level1(world)

                if event.key == pygame.K_UP:
                    if player.rect.y - STEP > 0:
                        player.rect.y -= STEP
                    else:
                        world = load_level(n, world, "up")
                        generate_level1(world)
                if event.key == pygame.K_DOWN:
                    if player.rect.y + STEP < y:
                        player.rect.y += STEP
                    else:
                        world = load_level(n, world, "down")
                        generate_level1(world)
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    terminate()