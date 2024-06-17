import pygame


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, img, top):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.speedx = 4
        self.bird_pass = False
        if top == True:
            self.rect.bottomleft = (x, y)
        else:
            self.rect.topleft = (x, y)
        self.last_pic_time = pygame.time.get_ticks()
        self.pipe_frequency = 1500

    def update(self):
        self.rect.x -= self.speedx
        if self.rect.right < 0:
            self.kill()


