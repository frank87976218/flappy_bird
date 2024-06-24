import pygame
import random
from bird import Bird
from pipe import Pipe

pygame.init()


def generate_pipes(last_pipe_time, pipe_frequency, pipe_group):
    now = pygame.time.get_ticks()
    if now - last_pipe_time >= pipe_frequency:
        random_height = random.randint(-100, 100)
        pipe_btm = Pipe(SCREEN_WIDTH, SCREEN_HIEGHT / 2 + pipe_gap / 2 + random_height, pipe_img, False)
        pipe_top = Pipe(SCREEN_WIDTH, SCREEN_HIEGHT / 2 - pipe_gap / 2 + random_height, flap_pipe_img, True)
        pipe_group.add(pipe_btm)
        pipe_group.add(pipe_top)
        return now
    return last_pipe_time


def draw_score():
    score_text = score_font.render(str(score), True, WHITE)
    window.blit(score_text, (SCREEN_WIDTH/2 - score_text.get_width()/2, 20))


def draw_delay():
    for i in range(delay_time, 0, -1):
        window.blit(bg_img, (0, 0))  # 重绘背景图
        pipe_group.draw(window)  # 重绘管道
        window.blit(ground_img, (ground_x, ground_top))  # 重绘地面
        bird_group.draw(window)  # 重绘鸟
        draw_score()  # 重绘分数
        delay_text = delay_font.render(str(i), True, WHITE)
        window.blit(delay_text, (SCREEN_WIDTH / 2 - delay_text.get_width() / 2, SCREEN_HIEGHT / 2 - delay_text.get_height() / 2))
        pygame.display.update()
        pygame.time.wait(1000)


# 設定常數
FPS = 60
SCREEN_WIDTH = 780
SCREEN_HIEGHT = 600
WHITE = (255, 255, 255)

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIEGHT))
pygame.display.set_caption("Flappy_Bird")
clock = pygame.time.Clock()


# 導入圖片
bg_img = pygame.image.load("img/bg.png")
bg_img = pygame.transform.scale(bg_img, (780, 600))
ground_img = pygame.image.load("img/ground.png")
pipe_img = pygame.image.load("img/pipe.png")
restart_img = pygame.image.load("img/restart.png")
restart_img = pygame.transform.scale(restart_img, (192, 57))
restart_img_rect = restart_img.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HIEGHT/2))
flap_pipe_img = pygame.transform.flip(pipe_img, False, True)
bird_imgs = []
for i in range(1, 4):
    bird_imgs.append(pygame.image.load(f"img/bird{i}.png"))
pygame.display.set_icon(bird_imgs[0])

# 載入字體
score_font = pygame.font.Font("微軟正黑體.ttf", 60)
delay_font = pygame.font.Font("微軟正黑體.ttf", 100)

# 遊戲變數
ground_speed = 4
ground_x = 0
pipe_gap = 150
pipe_frequency = 1500
last_pipe_time = pygame.time.get_ticks() - pipe_frequency
ground_top = SCREEN_HIEGHT - 100
score = 0
delay_time = 3
game_over = False

bird = Bird(100, SCREEN_HIEGHT/2, bird_imgs)
bird_group = pygame.sprite.Group()
bird_group.add(bird)

pipe_group = pygame.sprite.Group()


run = True
while run:
    clock.tick(FPS)  # 一秒最多執行"FPS"次

    # 取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # 只能判斷一次滑鼠是否按了
            if event.button == 1 and not game_over:
                bird.jump()
            if restart_img_rect.collidepoint(event.pos) and game_over:
               draw_delay()
               game_over = False
               score = 0
               last_pipe_time = pygame.time.get_ticks() - pipe_frequency
               bird.reset()
               pipe_group.empty()
    # 更新遊戲
    bird_group.update(ground_top)
    if not game_over:
        pipe_group.update()
        last_pipe_time = generate_pipes(last_pipe_time, pipe_frequency, pipe_group)
        first_pipe = pipe_group.sprites()[0]
        if not first_pipe.bird_pass:
            if first_pipe.rect.right < bird.rect.left:
                score += 1
                first_pipe.bird_pass = True

        # 移動底板
        ground_x -= ground_speed
        if ground_x < -100:
            ground_x = 0
    # 碰撞判斷
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or\
        bird.rect.top <= 0 or\
        bird.rect.bottom >= ground_top:
        game_over = True
        bird.game_over()

    # 畫面顯示
    window.blit(bg_img, (0, 0))
    pipe_group.draw(window)
    window.blit(ground_img, (ground_x, ground_top))
    bird_group.draw(window)
    draw_score()
    if game_over:
        window.blit(restart_img, (SCREEN_WIDTH/2 - restart_img.get_width()/2, SCREEN_HIEGHT/2 -
                                  restart_img.get_height()/2))
    pygame.display.update()

pygame.quit()
