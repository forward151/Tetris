import pygame
import sys
from tetris_logic import main
from datetime import datetime
pygame.init()
pygame.font.init()
pygame.mixer.init()


FPS = 60
width = 400
height = 600
volume = True
fs_font = pygame.font.Font(None, 36)
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.mixer.music.load("37543.mp3")
pygame.mixer.music.play()
pygame.mixer.music.play(-1)
pygame.display.update()


class But(pygame.sprite.Sprite):
    def __init__(self, filename, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        # self.image.set_alpha(100)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


BackGround1 = Background('images/first_bg.png', [-100, 0])
BackGround2 = Background('images/second_bg.png', [-100, 0])
recBackGround = Background('images/record_bg.png', [-99, 1])
contBackGround = Background('images/main_bg.png', [-100, 0])
bpoff = But('images/play_off.png', 106, 181)
bpon = But('images/play_on.png', 106, 181)
voloff = But('images/vol_off.png', 169, 500)
volon = But('images/vol_on.png', 169, 500)
contron = But('images/cont_on.png', 17, 500)
controff = But('images/cont_off.png', 17, 500)
recon = But('images/rec_on.png', 249, 500)
recoff = But('images/rec_off.png', 249, 500)


def first_screen():
    global volume

    play = False
    rec = False
    cont = False
    in_play = False
    in_contr = False
    in_rec = False

    def base_update():
        screen.fill([0, 0, 0])
        screen.blit(BackGround1.image, BackGround1.rect)
        if in_play:
            screen.blit(bpon.image, bpon.rect)
        else:
            screen.blit(bpoff.image, bpoff.rect)
        if in_contr:
            screen.blit(contron.image, contron.rect)
        else:
            screen.blit(controff.image, controff.rect)
        if in_rec:
            screen.blit(recon.image, recon.rect)
        else:
            screen.blit(recoff.image, recoff.rect)
        if not volume:
            screen.blit(voloff.image, voloff.rect)
            pygame.mixer.music.set_volume(0)
        else:
            screen.blit(volon.image, volon.rect)
            pygame.mixer.music.set_volume(1)

    while not play and not rec and not cont:
        clock.tick(FPS)

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()
            elif i.type == pygame.MOUSEMOTION:
                if bpon.rect.collidepoint(i.pos):
                    in_play = True
                    in_contr = False
                    in_rec = False
                elif contron.rect.collidepoint(i.pos):
                    in_contr = True
                    in_play = False
                    in_rec = False
                elif recon.rect.collidepoint(i.pos):
                    in_contr = False
                    in_play = False
                    in_rec = True
                else:
                    in_contr = False
                    in_play = False
                    in_rec = False

            elif i.type == pygame.MOUSEBUTTONDOWN:
                if bpon.rect.collidepoint(i.pos):
                    play = True
                elif voloff.rect.collidepoint(i.pos):
                    volume = not volume
                elif recon.rect.collidepoint(i.pos):
                    rec = True
                elif contron.rect.collidepoint(i.pos):
                    cont = True

        base_update()
        pygame.display.update()
    if play:
        sc = main()
        last_screen(sc)
    elif rec:
        record_screen()
    elif cont:
        control_screen()


def last_screen(score):
    file = open('records.txt', 'r')
    old_score = file.read()
    file.close()
    old_score = int(old_score)
    if old_score < score:
        file = open('records.txt', 'w')
        file.write(str(score))
        file.close()
    fnt = pygame.font.Font(None, 30)
    fnt2 = pygame.font.Font(None, 40)
    gmvon = But('images/GmOv_on.png', 105, 180)
    gmvoff = But('images/GmOv_off.png', 105, 180)
    menoff = But('images/menu_on.png', 16, 500)
    menon = But('images/menu_off.png', 16, 500)
    exoff = But('images/exit_on.png', 249, 500)
    exon = But('images/exit_off.png', 249, 500)
    men = False
    ex = False
    play = False
    gm = False
    score_txt = fnt.render('Your score:', True, (255, 255, 255))
    score2_txt = fnt2.render(str(score), True, (255, 0, 255))

    def base_update():
        screen.fill([0, 0, 0])
        screen.blit(BackGround2.image, BackGround2.rect)
        if gm:
            screen.blit(gmvon.image, gmvon.rect)
        else:
            screen.blit(gmvoff.image, gmvoff.rect)
        screen.blit(score_txt, (200 - score_txt.get_width() // 2, 242))
        screen.blit(score2_txt, (200 - score2_txt.get_width() // 2, 270))
        if men:
            screen.blit(menoff.image, menoff.rect)
        else:
            screen.blit(menon.image, menon.rect)

        if ex:
            screen.blit(exoff.image, exoff.rect)
        else:
            screen.blit(exon.image, exon.rect)

    old_sec = datetime.now().second
    while not play:
        clock.tick(FPS)
        new_sec = datetime.now().second
        if new_sec != old_sec:
            old_sec = new_sec
            gm = not gm
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()
            elif i.type == pygame.MOUSEMOTION:
                if menon.rect.collidepoint(i.pos):
                    men = True
                    ex = False
                elif exon.rect.collidepoint(i.pos):
                    ex = True
                    men = False
                else:
                    ex = False
                    men = False
            elif i.type == pygame.MOUSEBUTTONDOWN:
                if menon.rect.collidepoint(i.pos):
                    play = True
                elif exon.rect.collidepoint(i.pos):
                    sys.exit()

        base_update()
        pygame.display.update()
    first_screen()


def control_screen():
    bck = False
    play = False
    bckon = But('images/back_on.png', 17, 499)
    bckoff = But('images/back_off.png', 17, 499)

    def base_update():
        screen.fill([0, 0, 0])
        screen.blit(contBackGround.image, contBackGround.rect)
        if bck:
            screen.blit(bckon.image, bckon.rect)
        else:
            screen.blit(bckoff.image, bckoff.rect)

    while not play:
        clock.tick(FPS)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()
            elif i.type == pygame.MOUSEMOTION:
                if bckon.rect.collidepoint(i.pos):
                    bck = True
                else:
                    bck = False

            elif i.type == pygame.MOUSEBUTTONDOWN:
                if bckon.rect.collidepoint(i.pos):
                    play = True

        base_update()
        pygame.display.update()
    first_screen()


def record_screen():
    fnt = pygame.font.Font(None, 30)
    fnt2 = pygame.font.Font(None, 40)
    play = False
    gm = True
    bck = False
    bckon = But('images/back_on.png', 17, 500)
    bckoff = But('images/back_off.png', 17, 500)
    file = open('records.txt', 'r')
    sc = file.read()
    file.close()
    txt_sc = fnt2.render(sc, True, (255, 128, 0))
    txt2 = fnt.render('YOUR RECORD', True, (255, 0, 0))
    txt3 = fnt.render('YOUR RECORD', True, (0, 255, 0))

    def base_update():
        screen.fill([0, 0, 0])
        screen.blit(recBackGround.image, recBackGround.rect)
        if bck:
            screen.blit(bckon.image, bckon.rect)
        else:
            screen.blit(bckoff.image, bckoff.rect)
        if gm:
            screen.blit(txt2, (200 - txt2.get_width() // 2, 202))
        else:
            screen.blit(txt3, (200 - txt3.get_width() // 2, 202))

        screen.blit(txt_sc, (200 - txt_sc.get_width() // 2, 250))

    old_sec = datetime.now().second
    while not play:
        clock.tick(FPS)
        new_sec = datetime.now().second
        if new_sec != old_sec:
            old_sec = new_sec
            gm = not gm
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()
            if i.type == pygame.MOUSEMOTION:
                if bckon.rect.collidepoint(i.pos):
                    bck = True
                else:
                    bck = False
            elif i.type == pygame.MOUSEBUTTONDOWN:
                if bckon.rect.collidepoint(i.pos):
                    play = True

        base_update()
        pygame.display.update()
    first_screen()


first_screen()
