import pygame
from random import randint

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60 #КОНТРОЛЬ КАДРОВ ВЫВОДИМЫХ В СЕКУНДУ
TILE = 32  #у нас квадратные картинки 32на32

window = pygame.display.set_mode((WIDTH, HEIGHT)) #создание окна
clock = pygame.time.Clock() #контроль  кол-ва кадров в сек

fontUI = pygame.font.Font(None, 30) #шрифт

imgBrick = pygame.image.load('images/block_brick.png') #картинка блока
imgTanks = [
    pygame.image.load('images/tank1.png'),
    pygame.image.load('images/tank2.png'),
    pygame.image.load('images/tank3.png'),
    pygame.image.load('images/tank4.png'),
    pygame.image.load('images/tank5.png'),
    pygame.image.load('images/tank6.png'),
    pygame.image.load('images/tank7.png'),
    pygame.image.load('images/tank8.png'), #картинка танка
]
imgBangs = [
    pygame.image.load('images/bang1.png'),
    pygame.image.load('images/bang2.png'),
    pygame.image.load('images/bang3.png'), #картинка взыва
]

DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]] #направление х,у


class UI:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self): #отрисовка жизней
        i = 0
        for obj in objects:
            if obj.type == 'tank':
                pygame.draw.rect(window, obj.color, (5 + i * 70, 5, 22, 22))

                text = fontUI.render(str(obj.hp), 1, obj.color)
                rect = text.get_rect(center=(5 + i * 70 + 32, 5 + 11))
                window.blit(text, rect)
                i += 1


class Tank:
    def __init__(self, color, px, py, direct, keyList):
        objects.append(self) #добавляет себя в объекты
        self.type = 'tank'

        self.color = color
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct #направление
        self.moveSpeed = 2 #скорость движения данных
        self.hp = 5

        self.shotTimer = 0 #таймер выстрела
        self.shotDelay = 60 #задержка, тк ФПС = 60
        self.bulletSpeed = 5
        self.bulletDamage = 1

        self.keyLEFT = keyList[0]
        self.keyRIGHT = keyList[1]
        self.keyUP = keyList[2]
        self.keyDOWN = keyList[3]
        self.keySHOT = keyList[4]

        self.rank = 0 #ранг танка
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90) #поворот картинки в нужное напавление
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 5, self.image.get_height() - 5)) #меньшаем размер танка, что бы он пролез
        self.rect = self.image.get_rect(center=self.rect.center)

        oldX, oldY = self.rect.topleft #сохранение старых позиций
        if keys[self.keyLEFT]: #движение танка
            self.rect.x -= self.moveSpeed
            self.direct = 3 #направление -1,0
        elif keys[self.keyRIGHT]:
            self.rect.x += self.moveSpeed
            self.direct = 1 # направление 1,0
        elif keys[self.keyUP]:
            self.rect.y -= self.moveSpeed
            self.direct = 0 # направление 0,-1
        elif keys[self.keyDOWN]:
            self.rect.y += self.moveSpeed
            self.direct = 2 #направление 0,1

        for obj in objects: #столконовение с блоками
            if obj != self and obj.type == 'block' and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY

        if keys[self.keySHOT] and self.shotTimer == 0: #стрельба
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
            self.shotTimer = self.shotDelay

        if self.shotTimer > 0: self.shotTimer -= 1

    def draw(self):
        pygame.draw.rect(window, self.color, self.rect)
        window.blit(self.image, self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)
            print(self.color, 'dead')


class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        bullets.append(self)
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage

    def update(self):
        self.px += self.dx
        self.py += self.dy

        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self) #пуля удаляется, если вылетит за поле
        else:
            for obj in objects:  # если сталкивается с объектом
                if obj != self.parent and obj.type != 'bang' and obj.rect.collidepoint(self.px, self.py):
                    obj.damage(self.damage)
                    bullets.remove(self)
                    Bang(self.px, self.py)
                    break

    def draw(self):
        pygame.draw.circle(window, 'yellow', (self.px, self.py), 2)


class Bang:
    def __init__(self, px, py):
        objects.append(self)
        self.type = 'bang'

        self.px, self.py = px, py
        self.frame = 0 #номер кадра

    def update(self):
        self.frame += 0.2 #обновление кадров взрыва
        if self.frame >= 3: objects.remove(self)

    def draw(self):
        image = imgBangs[int(self.frame)]
        rect = image.get_rect(center=(self.px, self.py))
        window.blit(image, rect)


class Block:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'block'

        self.rect = pygame.Rect(px, py, size, size) #за столкновение
        self.hp = 1

    def update(self):
        pass

    def draw(self):
        window.blit(imgBrick, self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0: objects.remove(self)


bullets = []
objects = [] #в списке будут храниться все объекты
Tank('blue', 100, 275, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))
Tank('red', 650, 275, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_o))
ui = UI()

for _ in range(150): #генерация блоков
    while True:
        x = randint(0, WIDTH // TILE - 1) * TILE #позиция строго вровнена по сетке
        y = randint(1, HEIGHT // TILE - 1) * TILE
        rect = pygame.Rect(x, y, TILE, TILE) #не сталкиваетлся ли наш блок с другими объектами
        fined = False
        for obj in objects:
            if rect.colliderect(obj.rect): fined = True #нашли столкновение

        if not fined: break

    Block(x, y, TILE)

play = True
while play: #обработчик событий
    for event in pygame.event.get(): #возвращает все события, которые произошли
        if event.type == pygame.QUIT: #означает, что пользователь закрыл
            play = False
    # перехватывание состояния кнопок перед обновлением
    keys = pygame.key.get_pressed()

    for bullet in bullets: bullet.update()
    for obj in objects: obj.update()
    ui.update()

    window.fill('black')
    for bullet in bullets: bullet.draw()
    for obj in objects: obj.draw()
    ui.draw()

    pygame.display.update()
    clock.tick(FPS) #контролирование ФПС

pygame.quit()