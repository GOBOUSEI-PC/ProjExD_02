import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900


delta = {  # 移動量辞書
    pg.K_UP: (0, -5),
    pg.K_RIGHT: (5, 0),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
}
kk_img0 = pg.image.load("ex02/fig/3.png")
kk_img0 = pg.transform.rotozoom(kk_img0, 0, 2.0)
kk_img4 = pg.transform.flip(kk_img0,True, False)



def make(muki,kk_img0):
    img_file = { #画像の向きを変えるための辞書
    
    (-5, 5):pg.transform.rotozoom(kk_img0, -45, 1.0),
    (-5, 0):pg.transform.rotozoom(kk_img0, 0, 1.0),
    (-5, -5):pg.transform.rotozoom(kk_img0, 45, 1.0),
    
    (0, -5):pg.transform.rotozoom(kk_img4, 90, 1.0),
    (5, -5):pg.transform.rotozoom(kk_img4, 45, 1.0),
    (5, 0):pg.transform.rotozoom(kk_img4, 0, 1.0),
    (5, 5):pg.transform.rotozoom(kk_img4, -45, 1.0),
    (0, 5):pg.transform.rotozoom(kk_img4, 90, 1.0),
    (0, 0):pg.transform.rotozoom(kk_img0, 90, 1.0),
    } 
    return img_file[muki]

def check_bound(obj_rct: pg.Rect):
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue，画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right: # 横方向判定
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom: # 縦方向判定
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    """こうかとん"""
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = (900, 400)  #こうかとんの初期座標を設定する
    """ばくだん"""
    bd_img = pg.Surface((20, 20))  #爆弾Surfaceを作成する
    bd_img.set_colorkey((0, 0, 0))  #黒い部分を透明にする
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    bd_rct = bd_img.get_rect()  #SurfaceからRectを抽出する
    x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bd_rct.center = (x, y)  #Rectにランダムな座標を設定する
    vx, vy = +5, +5  #爆弾の速度

    clock = pg.time.Clock()
    tmr = 0
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bd_rct):
            print("ゲームオーバー")
            return
            
        screen.blit(bg_img, [0, 0])

        """こうかとん"""
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in delta.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  #横方向の合計移動量
                sum_mv[1] += mv[1]  #縦方向の合計移動量
        kk_rct.move_ip(sum_mv[0], sum_mv[1])  #移動させる
        if check_bound(kk_rct) != (True, True):  #はみだし判定
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) 
        screen.blit(kk_img, kk_rct)  #移動後の座標に表示させる
        """"ばくだん"""
        bd_rct.move_ip(vx, vy)  #爆弾を移動させる
        yoko, tate = check_bound(bd_rct)
        if not yoko:  #横方向にはみ出たら
            vx *= -1
        if not tate:  #縦方向にはみ出たら
            vy *= -1
        screen.blit(bd_img, bd_rct)  #Rectを使って試しにblit
        
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()