import pygame
from random import randint
pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60 #КОНТРОЛЬ КАДРОВ ВЫВОДИМЫХ В СЕКУНДУ
TILE = 32 #у нас квадратные картинки 32на32

window = pygame.display.set_mode((WIDTH, HEIGHT)) #создание окна
clock = pygame.time.Clock() #контроль  кол-ва кадров в сек

DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]  #направление х,у


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

    def update(self):
        oldX, oldY = self.rect.topleft #сохранение старых позиций
        if keys[self.keyLEFT]: #движение танка
            self.rect.x -= self.moveSpeed
            self.direct = 3 #направление -1,0
        elif keys[self.keyRIGHT]:
            self.rect.x += self.moveSpeed
            self.direct = 1  # направление 1,0
        elif keys[self.keyUP]:
            self.rect.y -= self.moveSpeed
            self.direct = 0 # направление 0,-1
        elif keys[self.keyDOWN]:
            self.rect.y += self.moveSpeed
            self.direct = 2 #направление 0,1

        for obj in objects: #столконовение с блоками
            if obj != self and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY


        if keys[self.keySHOT] and self.shotTimer == 0: #стрельба
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
            self.shotTimer = self.shotDelay

        if self.shotTimer > 0: self.shotTimer -= 1

    def draw(self):
        pygame.draw.rect(window, self.color, self.rect)

        x = self.rect.centerx + DIRECTS[self.direct][0] * 30 #дуло
        y = self.rect.centery + DIRECTS[self.direct][1] * 30
        pygame.draw.line(window, 'white', self.rect.center, (x, y), 4) #рисуем дуло

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
            for obj in objects: # если сталкивается с объектом
                if obj != self.parent and obj.rect.collidepoint(self.px, self.py):
                    obj.damage(self.damage)
                    bullets.remove(self)
                    break

    def draw(self):
        pygame.draw.circle(window, 'yellow', (self.px, self.py), 2) #пуля

class Block:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'blocks'

        self.rect = pygame.Rect(px, py, size, size) #за столкновение
        self.hp = 1

    def update(self):
        pass

    def draw(self):
        pygame.draw.rect(window, 'green', self.rect)
        pygame.draw.rect(window, 'gray20', self.rect, 2) #обводка блоков

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0: objects.remove(self)

bullets = []
objects = [] #в списке будут храниться все объекты
Tank('blue', 100, 275, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))
Tank('red', 650, 275, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_o))

for _ in range(150): #генерация блоков
    while True:
        x = randint(0, WIDTH // TILE - 1) * TILE #позиция строго вровнена по сетке
        y = randint(0, HEIGHT // TILE - 1) * TILE
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

    window.fill('black')
    for bullet in bullets: bullet.draw()
    for obj in objects: obj.draw()

    pygame.display.update()
    clock.tick(FPS)  #контролирование ФПС

pygame.quit()



