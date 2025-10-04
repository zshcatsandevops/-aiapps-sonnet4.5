# ================================================================
# program.py — Moonlit Bridge Boss Battle  (CatOS 64 / files = off)
# ================================================================
import pygame, random, math
pygame.init()

W, H = 256, 240
SCALE = 3
FPS = 60
GRAVITY = 0.3

screen = pygame.display.set_mode((W*SCALE, H*SCALE))
pygame.display.set_caption("Moonlit Bridge Boss Battle")
surf = pygame.Surface((W, H))
clock = pygame.time.Clock()

# Palette
BLACK=(0,0,0); WHITE=(248,248,248); RED=(228,92,16)
ORANGE=(252,152,56); YELLOW=(248,216,120); GREEN=(0,168,0)
PURPLE=(136,20,176); BLUE=(0,88,248); GRAY=(112,112,112)

# ----------------------------------------------------------------
class Hero:
    def __init__(self): self.x=40; self.y=160; self.vx=self.vy=0; self.on_ground=False
    def update(self,keys,plats):
        self.vx=(keys[pygame.K_RIGHT]-keys[pygame.K_LEFT])*2
        if keys[pygame.K_SPACE] and self.on_ground: self.vy=-7; self.on_ground=False
        self.vy+=GRAVITY; self.x+=self.vx; self.y+=self.vy
        self.on_ground=False
        for p in plats:
            if (self.x+8>p[0] and self.x<p[0]+p[2] and
                self.y+16>=p[1] and self.y+16<=p[1]+8 and self.vy>=0):
                self.y=p[1]-16; self.vy=0; self.on_ground=True
        self.x=max(0,min(W-8,self.x))
    def draw(self,s): pygame.draw.rect(s,BLUE,(self.x,self.y,8,16)); pygame.draw.rect(s,RED,(self.x,self.y-3,8,3))

class FireOrb:
    def __init__(self,x,y,a):
        self.x,self.y=x,y; self.vx=math.cos(a)*2; self.vy=math.sin(a)*2; self.life=180
    def update(self): self.x+=self.vx; self.y+=self.vy; self.life-=1
    def draw(self,s): c=random.choice([RED,ORANGE,YELLOW]); pygame.draw.circle(s,c,(int(self.x),int(self.y)),3)
    def alive(self): return 0<self.life and 0<self.x<W and 0<self.y<H

class BabyDrake:
    def __init__(self): self.x=180; self.y=100; self.vx=0; self.vy=0; self.hp=12; self.timer=0; self.phase=1
    def update(self,hero):
        self.timer+=1
        if self.hp<=8: self.phase=2
        if self.hp<=4: self.phase=3
        self.vy+=GRAVITY; self.y+=self.vy
        if self.y>120: self.y=120; self.vy=0
        self.vx=(math.sin(self.timer*0.02))*self.phase
        self.x+=self.vx
    def attack(self):
        if self.timer%90==0:
            shots=[]
            spread={1:[0],2:[-0.2,0,0.2],3:[-0.4,-0.2,0,0.2,0.4]}[self.phase]
            for ang in spread: shots.append(FireOrb(self.x,self.y,math.pi+ang))
            return shots
        return []
    def hit(self): self.hp-=1
    def draw(self,s):
        color=ORANGE if self.phase==1 else (RED if self.phase==2 else YELLOW)
        pygame.draw.circle(s,color,(int(self.x),int(self.y)),16)
        pygame.draw.circle(s,BLACK,(int(self.x-6),int(self.y-4)),3)
        pygame.draw.circle(s,BLACK,(int(self.x+6),int(self.y-4)),3)
        pygame.draw.rect(s,GREEN,(self.x-12,self.y+10,24,6))

# ----------------------------------------------------------------
def draw_background(surf):
    surf.fill(BLACK)
    # Gradient sky
    for i in range(120):
        c=int(32+i*1.5); pygame.draw.line(surf,(c//2,0,c),(0,i),(W,i))
    pygame.draw.circle(surf,YELLOW,(200,40),20)  # moon
    for i in range(0,W,32): pygame.draw.rect(surf,GRAY,(i,200,32,8))
    pygame.draw.rect(surf,PURPLE,(0,208,W,32))

# ----------------------------------------------------------------
def main():
    hero=Hero(); boss=BabyDrake()
    plats=[(0,200,W,8)]
    fireballs=[]
    state="intro"; intro=180; victory=0
    running=True
    while running:
        dt=clock.tick(FPS)
        for e in pygame.event.get():
            if e.type==pygame.QUIT or (e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE): running=False
        keys=pygame.key.get_pressed()
        draw_background(surf)

        if state=="intro":
            intro-=1
            f=pygame.font.Font(None,18)
            t=f.render("A shadow rises...",True,WHITE)
            surf.blit(t,t.get_rect(center=(W//2,H//2)))
            if intro<=0: state="battle"
        elif state=="battle":
            hero.update(keys,plats)
            boss.update(hero)
            fireballs.extend(boss.attack())
            for f in fireballs[:]:
                f.update()
                if not f.alive(): fireballs.remove(f)
                elif abs(hero.x-f.x)<6 and abs(hero.y-f.y)<6:
                    fireballs.remove(f)
            if keys[pygame.K_z] and abs(hero.x-boss.x)<20 and abs(hero.y-boss.y)<16:
                boss.hit()
                if boss.hp<=0: state="victory"; victory=180
            hero.draw(surf); boss.draw(surf)
            for p in plats: pygame.draw.rect(surf,GRAY,p)
            for f in fireballs: f.draw(surf)
        elif state=="victory":
            victory-=1
            hero.draw(surf)
            msg=pygame.font.Font(None,20).render("Boss Defeated!",True,YELLOW)
            surf.blit(msg,msg.get_rect(center=(W//2,80)))
            if victory<=0: running=False

        scaled=pygame.transform.scale(surf,(W*SCALE,H*SCALE))
        screen.blit(scaled,(0,0)); pygame.display.flip()
    pygame.quit()

if __name__=="__main__": main()
