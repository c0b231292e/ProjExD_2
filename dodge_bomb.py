import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650  # 幅、高さを設定
DELTA = {pg.K_UP: (0,-5),
         pg.K_DOWN: (0,+5),
         pg.K_LEFT: (-5,0),
         pg.K_RIGHT: (+5,0),
         }  # 各キーの増減を設定
saccs = [a for a in range(1, 11)]
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct: pg.Rect) -> tuple[bool,bool]:
    """
    引数：こうかとん,または,爆弾のRect
    戻り値：真理値タプル（横判定の結果、縦判定の結果）
    画面内ならTrue,画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def gameover(screen:pg.Surface) -> None:
    """
    ゲームオーバーの設定
    
    """
    over_img = pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(over_img,(0,0,0),pg.Rect(0,0,WIDTH,HEIGHT))
    over_img.set_alpha(150)
    over_rct =over_img.get_rect()
    screen.blit(over_img,over_rct)
    
    font = pg.font.Font(None,80) #  文字の部分
    txt = font.render("Game Over",True,(255,255,255))
    txt_rct = txt.get_rect(center = (WIDTH//2,HEIGHT//2))
    screen.blit(txt,txt_rct)
    
    
    for i in range(2):
        sad_img = pg.image.load("fig/8.png")  # 画像Surfaceを作成
        sad1_img= pg.transform.rotozoom(sad_img, 0, 1.0) #  拡大縮小などを設定
        sad1_rct = sad1_img.get_rect()
        sad1_rct.center = (750+(-400*i),HEIGHT//2)
        screen.blit(sad1_img,sad1_rct)
        
        
    pg.display.update()
    time.sleep(5)
        
        
def accsel():
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
    return  


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20))  # 空のsurface
    bb_img.set_colorkey((0,0,0))  # 黒に設定
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_rct = bb_img.get_rect()  # 爆弾のrectの抽出
    bb_rct.centerx = random.randint(0,WIDTH)  # x座標のランダム取り出し
    bb_rct.centery = random.randint(0,HEIGHT)  # y座標のランダム取り出し
    vx , vy = +5,-5  # 増加量を設定
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
             #  こうかとんと爆弾が重なっていたら
            return 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]  #横座標、縦座標の順
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key, tpl in DELTA.items(): 
            if key_lst[key]:
                sum_mv[0] += tpl[0]  # 横方向
                sum_mv[1] += tpl[1]  # 縦方向
                
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx,vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
