
import pygame
import random
import time
import math
import networkx as nx

pygame.init()

x_ = 20
y_ = 40

white = 255,255,255
black = 0,0,0
red = 255,0,0
blue = 0,0,255
green  =0,255,0



#SET THE PYGAME PARAMETERS
window_size = [500,550]
screen = pygame.display.set_mode(window_size)
screen.fill(white)

#Start= (419,83)
#End = (427,316)

dist_x = 10
dist_y = 10




class Button:
    def __init__ (self, colour, x, y, width, height,text):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
    def create(self,screen):
        pygame.draw.rect(screen, self.colour, [self.x, self.y,self.width ,self.height])
        font = pygame.font.SysFont('Arial', 14)
        text = font.render(self.text, True, white)
        textRect = text.get_rect()
        textRect.center = (int(self.x +self.width/2) ,int(self.y + self.height/2))
        screen.blit(text, textRect)

def is_is_obstacle(point):
    x,y = point[0],point[1]

    if screen.get_at((x,y)) == black:
        return True
    return False    

def is_inside_game(x,y):
    if (x>x_) and (x<x_ + 440) and (y>y_) and  (y < y_ + 400):
        return True 
    else:
        return False 


def random_point():
    random_x = random.randint(x_, x_ + 440  - 1)
    random_y = random.randint(y_, y_ + 400  - 1 )
    return (random_x, random_y)

def point_inside_rec(xr,yr,wr,hr,x,y):
    if (x> xr) and (x < xr + wr) and (y > yr) and (y < yr + hr):
        return True 
    else:
        return False

    
def dist(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)     


def Nearest(G,point):
    shortest_dist = 100000000000000;
    shortest_node = (0,0)
    for node in G.nodes():
        distance = dist(node,point)
        if distance <= shortest_dist:
            shortest_dist = distance
            shortest_node = node  

    return  shortest_node    




def New_node(nearest_node,random_node):
    y = random_node[1]-nearest_node[1]
    if y > 0:
        y = 1
    else:
        y = -1    
    x = random_node[0]-nearest_node[0]
    if x > 0:
        x = 1
    else:
        x = -1 

    new_node = (nearest_node[0]+ x*dist_x , nearest_node[1]+y*dist_y)
    return new_node

def goal_reached(node):
    x,y = node
    if screen.get_at((x,y)) == green:
        return True

    return False



pygame.draw.rect(screen,black,(x_,y_,440,400),3)

B = Button(black, 210, 470, 100, 50, "Aceptar entorno")
B.create(screen)

running = True
level = 1

Start = 0
End = 0
parent = dict()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if running==False:
            break

        m = pygame.mouse.get_pressed()
        x,y = pygame.mouse.get_pos()

        if m[0]==1:
            if point_inside_rec(B.x,B.y, B.width, B.height,x,y):
                if level==1 and Start == 0:
                    print('Entorno dibujado')
                    level+=1
                    B.colour=red
                    B.text = "Aceptar inicio"
                elif level==2 and Start:
                    print('Inicio dibujada')
                    level+=1
                    B.colour=green
                    B.text = "Aceptar meta"
                elif level==3 and End!=0:
                    print('Meta dibujada')
                    level+=1
                    B.colour=white
                    B.text = ""
                B.create(screen)

            elif level==1:
                if is_inside_game(x,y):
                    pygame.draw.rect(screen, black, (x, y,20,20), 0)
            elif level == 2 and Start == 0:
                if is_inside_game(x,y):
                    Start=(x,y)
                    pygame.draw.rect(screen, red, (x, y,20,20), 0)
                    font = pygame.font.SysFont('Arial', 20)
                    text = font.render("Inicio = ("+str(x)+","+str(y)+")", True, red)
                    textRect = text.get_rect()
                    textRect.center = (90, 490)
                    screen.blit(text, textRect)

            elif level == 3 and End == 0:
                if is_inside_game(x,y):
                    End = (x,y)
                    pygame.draw.rect(screen, green, (x, y,20,20), 0)
                    font = pygame.font.SysFont('Arial', 20)
                    text = font.render("Meta = ("+str(x)+","+str(y)+")", True, green)
                    textRect = text.get_rect()
                    textRect.center = (410, 490)
                    screen.blit(text, textRect)

        if level>=4:
            running = False
            break

    pygame.display.update()


parent[Start]=(-1,-1)
G = nx.Graph()
G.add_node(Start) 
running = True
lastnode = 0

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    random_node  = random_point()
    if is_is_obstacle(random_node):
        continue
    nearest_node = Nearest(G,random_node) 
    new_node = New_node(nearest_node,random_node)
    if not is_is_obstacle(new_node) and is_inside_game(new_node[0],new_node[1]) and new_node not in parent:
        G.add_node(new_node)
        parent[new_node] = nearest_node
        if not goal_reached(new_node):
            pygame.draw.circle(screen, blue, (new_node), 2)    
            pygame.draw.line(screen, blue, (nearest_node), (new_node), 2)
            pygame.display.update()
        else:
            pygame.draw.circle(screen, blue, (new_node), 2)    
            pygame.draw.line(screen, blue, (nearest_node), (new_node), 2)
            pygame.display.update()
            running = False 
            lastnode = new_node  
            break




   

running = True
print("Generando camino")

while (lastnode != Start):
    pygame.draw.circle(screen, green, (lastnode), 2)
    pygame.draw.line(screen, green, parent[lastnode], lastnode, 2)
    lastnode = parent[lastnode]
    pygame.display.update()


font_ = pygame.font.SysFont('Arial', 20)
text_ = font_.render("Camino encontrado", True, black)
textRect_ = text_.get_rect()
textRect_.center = (240, 490)
screen.blit(text_, textRect_)
pygame.display.update()


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break



pygame.quit()