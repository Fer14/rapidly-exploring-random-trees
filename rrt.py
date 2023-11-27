import pygame
import random
import math
import networkx as nx
import numpy
import typer


white = 255, 255, 255
black = 81, 85, 93
red = 255, 87, 87
blue = 82, 113, 255
green = 126, 217, 87


class Button:
    def __init__(self, colour, x, y, width, height, text, text_colour, screen):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_colour = text_colour
        self.screen = screen

    def display(self):
        pygame.draw.rect(
            self.screen,
            self.colour,
            [self.x, self.y, self.width, self.height],
            border_top_left_radius=10,
            border_top_right_radius=10,
            border_bottom_left_radius=10,
            border_bottom_right_radius=10,
        )
        font = pygame.font.SysFont("Roboto", 30)
        text = font.render(self.text, True, self.text_colour)
        textRect = text.get_rect()
        textRect.center = (int(self.x + self.width / 2), int(self.y + self.height / 2))
        self.screen.blit(text, textRect)

    def update(self, color, text, text_color):
        self.colour = color
        self.text = text
        self.text_colour = text_color
        self.display()

    def is_clicked(self, x, y):
        if (
            (x > self.x)
            and (x < self.x + self.width)
            and (y > self.y)
            and (y < self.y + self.height)
        ):
            return True
        else:
            return False


class Enviroment:
    def __init__(self, x, y, width, height, screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen

    def display(self):
        pygame.draw.rect(
            self.screen,
            white,
            (self.x, self.y, self.width, self.height),
            3,
            border_top_left_radius=10,
            border_top_right_radius=10,
            border_bottom_left_radius=10,
            border_bottom_right_radius=10,
        )

    def is_clicked(self, x, y):
        if (
            (x > self.x)
            and (x < self.x + self.width)
            and (y > self.y)
            and (y < self.y + self.height)
        ):
            return True
        else:
            return False

    def random_point(self):
        random_x = random.randint(self.x, self.x + self.width - 1)
        random_y = random.randint(self.y, self.y + self.height - 1)
        return (random_x, random_y)

    @staticmethod
    def draw_point(screen, x, y, color):
        pygame.draw.rect(
            screen,
            color,
            (x, y, 20, 20),
            0,
            border_top_left_radius=10,
            border_top_right_radius=10,
            border_bottom_left_radius=10,
            border_bottom_right_radius=10,
        )


class Instuction:
    def __init__(self, text, screen):
        self.screen = screen
        self.text = text

    def update(self, text):
        self.text = text
        self.display()

    def display(self):
        pygame.draw.rect(self.screen, black, (0, 0, 1000, 60), 0)
        font = pygame.font.SysFont("Roboto", 30)
        text_ = font.render(self.text, True, white)
        textRect_ = text_.get_rect()
        textRect_.center = (500, 30)
        self.screen.blit(text_, textRect_)


class NodeUtils:
    def __init__(self, type):
        self.type = type

    def is_is_obstacle(point, screen):
        x, y = point[0], point[1]
        if screen.get_at((x, y)) == white:
            return True
        return False

    @staticmethod
    def distance(p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    @staticmethod
    def nearest(G, point):
        shortest_dist = 100000000000000
        shortest_node = (0, 0)
        for node in G.nodes():
            dist = NodeUtils.distance(node, point)
            if dist <= shortest_dist:
                shortest_dist = dist
                shortest_node = node

        return shortest_node

    @staticmethod
    def goal_reached(node, screen):
        x, y = node
        if screen.get_at((x, y)) == green:
            return True

        return False

    def new_node(self, nearest_node, random_node):
        if self.type == "normal":
            return self.new_node_normal(nearest_node, random_node)
        else:
            return self.new_node_simplified(nearest_node, random_node)

    def new_node_normal(self, nearest_node, random_node):
        s = []
        s.append(random_node[0] - nearest_node[0])
        s.append(random_node[1] - nearest_node[1])
        signos = numpy.sign(s)
        if signos[1] == -1:
            y = random.randint(-10, 0)
        else:
            y = random.randint(0, 10)
        x = math.sqrt(100 - (y**2))
        if signos[0] == -1:
            x = x * -1
        return (int(nearest_node[0] + x), int(nearest_node[1] + y))

    def new_node_simplified(self, nearest_node, random_node):
        dist_x = 10
        dist_y = 10

        y = random_node[1] - nearest_node[1]
        if y > 0:
            y = 1
        else:
            y = -1
        x = random_node[0] - nearest_node[0]
        if x > 0:
            x = 1
        else:
            x = -1

        new_node = (nearest_node[0] + x * dist_x, nearest_node[1] + y * dist_y)
        return new_node


def build_enviroment(screen, enviroment, button, instruction):
    phase = 1
    start = -1
    goal = -1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if running == False:
                break

            m = pygame.mouse.get_pressed()
            x, y = pygame.mouse.get_pos()

            if m[0] == 1:
                x, y = pygame.mouse.get_pos()
                if button.is_clicked(x, y):
                    if phase == 1 and start == -1:
                        phase += 1
                        button.update(red, ">>", white)
                        instruction.update("Click starting point")
                    elif phase == 2 and start != -1:
                        phase += 1
                        button.update(green, ">>", white)
                        instruction.update("Click goal point")
                    elif phase == 3 and goal != -1:
                        phase += 1
                        button.update(white, "...", black)
                        instruction.update("Finding path...")
                elif phase == 1:
                    if enviroment.is_clicked(x, y):
                        pygame.draw.rect(
                            screen,
                            white,
                            (x, y, 20, 20),
                            0,
                            border_top_left_radius=10,
                            border_top_right_radius=10,
                            border_bottom_left_radius=10,
                            border_bottom_right_radius=10,
                        )
                elif phase == 2 and start == -1:
                    if enviroment.is_clicked(x, y):
                        start = (x, y)
                        enviroment.draw_point(screen, x, y, red)
                elif phase == 3 and goal == -1:
                    if enviroment.is_clicked(x, y):
                        goal = (x, y)
                        enviroment.draw_point(screen, x, y, green)

            if phase == 4:
                running = False
                break

        pygame.display.update()

    return start, goal, enviroment


def run_path_finding(screen, enviroment, start, goal, nodeutils):
    parent = {}
    parent[start] = (-1, -1)
    G = nx.Graph()
    G.add_node(start)
    running = True
    lastnode = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        random_node = enviroment.random_point()
        if NodeUtils.is_is_obstacle(random_node, screen):
            continue
        nearest_node = NodeUtils.nearest(G, random_node)
        new_node = nodeutils.new_node(nearest_node, random_node)

        if (
            not NodeUtils.is_is_obstacle(new_node, screen)
            and enviroment.is_clicked(new_node[0], new_node[1])
            and new_node not in parent
        ):
            G.add_node(new_node)
            parent[new_node] = nearest_node
            if not NodeUtils.goal_reached(new_node, screen):
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

    while lastnode != start:
        pygame.draw.circle(screen, green, (lastnode), 2)
        pygame.draw.line(screen, green, parent[lastnode], lastnode, 2)
        lastnode = parent[lastnode]
        pygame.display.update()

    pygame.display.update()


def wait_restart(button, instruction):
    button.update(white, "Restart", black)
    instruction.update("")
    pygame.display.update()

    inner_running = True
    running = True

    while inner_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inner_running = False
                running = False
                break

            m = pygame.mouse.get_pressed()
            x, y = pygame.mouse.get_pos()

            if m[0] == 1:
                x, y = pygame.mouse.get_pos()
                if button.is_clicked(x, y):
                    inner_running = False
                    break
    return running


def main(
    type: str = typer.Option(
        "normal", help="Type of the simulation type: normal or simplified"
    )
):
    pygame.init()

    window_size = [1000, 550]
    x_ = 20
    y_ = 60

    env_width = 950
    env_height = 400

    nodeutils = NodeUtils(type=type)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Rapidly Exploring Random Trees")
        screen.fill(black)
        button = Button(
            white, 820, 470, 150, 50, ">>", text_colour=black, screen=screen
        )
        button.display()
        instruction = Instuction(
            "Draw enviroment...",
            screen,
        )
        instruction.display()
        enviroment = Enviroment(x_, y_, env_width, env_height, screen)
        enviroment.display()
        start, goal, enviroment = build_enviroment(
            screen, enviroment, button, instruction
        )
        run_path_finding(screen, enviroment, start, goal, nodeutils)
        running = wait_restart(button, instruction)

    pygame.quit()
    print("Thank you for playing the simulator,we look forward to your see you again! ")


if __name__ == "__main__":
    typer.run(main)
