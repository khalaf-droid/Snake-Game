import pygame  # import pygame library to create the game interface
import sys  # import sys to handle system exit and windows
from queue import PriorityQueue  # import PriorityQueue for A* algorithm f(n)=g(n)+h(n)
import random  # import random to place food in different places

pygame.init()  # initialize all imported pygame modules

WIDTH = 800  # set the width of the game window
HEIGHT = 600  # set the height of the game window
GRID_SIZE = 20  # set the size of one square cell
GRID_WIDTH = WIDTH // GRID_SIZE  # calculate how many cells in width
GRID_HEIGHT = HEIGHT // GRID_SIZE  # calculate how many cells in height

BLACK = (0, 0, 0)  # define black color using RGB
WHITE = (255, 255, 255)  # define white color using RGB
GREEN = (0, 255, 0)  # define green color for snake border
RED = (255, 0, 0)  # define red color for food
BLUE = (0, 120, 255)  # define blue color for snake head
DARK_GREEN = (0, 180, 0)  # define dark green for snake body
GRAY = (40, 40, 40)  # define gray color for grid lines
YELLOW = (255, 255, 0)  # define yellow color for AI hints

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # create the display window
pygame.display.set_caption("Snake AI EELU - User & AI")  # set window title
clock = pygame.time.Clock()  # create a clock object to control game speed

class Node:  # start defining Node class for A* pathfinding
    def __init__(self, position, parent=None):  # initialize node with position and parent
        self.position = position  # store the (x, y) coordinate
        self.parent = parent  # store the previous node to trace back path
        self.g = 0  # g(n): actual cost from start to current node
        self.h = 0  # h(n): estimated distance to food
        self.f = 0  # f(n) = g + h: total cost of the node
        
    def __eq__(self, other):  # define equality to compare node positions
        return self.position == other.position   
    
    def __lt__(self, other):  # define "less than" to compare nodes in PriorityQueue
        return self.f < other.f 

class Snake:  # start defining Snake class
    def __init__(self):  # constructor for Snake
        self.reset()  # call reset to set initial values
        
    def reset(self):  # function to restart snake properties
        self.length = 3  # set starting length of snake
        self.positions = [(GRID_WIDTH//2, GRID_HEIGHT//2)]  # place snake in middle
        self.direction = (1, 0)  # set initial movement to the right
        self.score = 0  # initialize score to zero
        self.grow_to = 3  # set initial growth target
        self.path_hint = []  # create empty list for AI path hints
        self.is_alive = True  # set snake state to alive
        
    def get_head_position(self):  # function to get coordinates of head
        return self.positions[0]  # head is always the first element in list
    
    def turn(self, point):  # function to change snake direction
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:  # check if turning backwards
            return  # do nothing if it tries to reverse
        else:  # if turn is valid
            self.direction = point  # update the direction vector
    
    def move(self):  # function to update snake position
        if not self.is_alive:  # check if snake is dead
            return  # stop movement
        head = self.get_head_position()  # get current head x, y
        x, y = self.direction  # get current direction x, y
        new_x = (head[0] + x) % GRID_WIDTH  # calculate new x with screen wrap
        new_y = (head[1] + y) % GRID_HEIGHT  # calculate new y with screen wrap
        new_position = (new_x, new_y)  # combine to new position tuple
        if new_position in self.positions[1:]:  # check if head hits body
            self.is_alive = False  # kill the snake
            return  # exit move function
        self.positions.insert(0, new_position)  # add new position to start of list
        if len(self.positions) > self.grow_to:  # if snake is longer than allowed
            self.positions.pop()  # remove the last part of tail

    def draw(self, surface):  # function to render snake and hints
        for pos in self.path_hint:  # loop through AI path coordinates
            hint_rect = pygame.Rect(pos[0]*GRID_SIZE + 7, pos[1]*GRID_SIZE + 7, 6, 6)  # create small hint box
            pygame.draw.rect(surface, YELLOW, hint_rect)  # draw yellow hint dots
        for i, p in enumerate(self.positions):  # loop through snake body parts
            color = BLUE if i == 0 else DARK_GREEN  # head is blue, body is green
            rect = pygame.Rect((p[0]*GRID_SIZE, p[1]*GRID_SIZE), (GRID_SIZE-2, GRID_SIZE-2))  # create body box
            pygame.draw.rect(surface, color, rect)  # draw the body part

class Food:  # start defining Food class
    def __init__(self):  # constructor for food
        self.position = (0, 0)  # initialize position
        self.randomize_position()  # place food randomly at start
    def randomize_position(self, obstacles=[]):  # function to find new food spot
        while True:  # keep looking until valid spot found
            self.position = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))  # get random x, y
            if self.position not in obstacles:  # check if spot is not on snake
                break  # stop loop when spot is clear
    def draw(self, surface):  # function to render food
        rect = pygame.Rect((self.position[0]*GRID_SIZE, self.position[1]*GRID_SIZE), (GRID_SIZE, GRID_SIZE))  # create food box
        pygame.draw.rect(surface, RED, rect)  # draw red food

class GameAI:  # start defining AI logic class
    def __init__(self, snake, food):  # link AI to snake and food
        self.snake = snake  # store snake reference
        self.food = food  # store food reference
    def heuristic(self, a, b):  # calculate estimated distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # return Manhattan distance
    def a_star_search(self):  # main A* pathfinding function
        start_node = Node(self.snake.get_head_position())  # create start node at head
        end_node = Node(self.food.position)  # create target node at food
        obstacles = set(self.snake.positions)  # treat snake body as walls
        open_list = PriorityQueue()  # create list for nodes to explore
        open_list.put((0, start_node))  # add start node with zero cost
        closed_list = set()  # create set for explored positions
        while not open_list.empty():  # while there are nodes to check
            current_node = open_list.get()[1]  # get node with lowest f(n)
            if current_node.position == end_node.position:  # if food reached
                path = []  # create list for final path
                while current_node:  # backtrack through parents
                    path.append(current_node.position)  # add position to path
                    current_node = current_node.parent  # move to parent
                return path[::-1]  # return reversed path (start to end)
            closed_list.add(current_node.position)  # mark current node as explored
            for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:  # check 4 directions
                neighbor_pos = (current_node.position[0]+dx, current_node.position[1]+dy)  # get neighbor x, y
                if (0 <= neighbor_pos[0] < GRID_WIDTH and 0 <= neighbor_pos[1] < GRID_HEIGHT  # check boundaries
                    and neighbor_pos not in obstacles):  # check if not hitting body
                    if neighbor_pos in closed_list: continue  # skip if already explored
                    neighbor = Node(neighbor_pos, current_node)  # create neighbor node
                    neighbor.g = current_node.g + 1  # update step cost
                    neighbor.h = self.heuristic(neighbor.position, end_node.position)  # calculate distance to food
                    neighbor.f = neighbor.g + neighbor.h  # calculate total cost
                    open_list.put((neighbor.f, neighbor))  # add to exploration list
        return []  # return empty if no path found

def main():  # main game loop function
    snake = Snake()  # create snake object
    food = Food()  # create food object
    ai = GameAI(snake, food)  # create AI object
    show_hint = True  # toggle for AI help
    while True:  # start infinite loop
        if show_hint:  # if AI help is enabled
            snake.path_hint = ai.a_star_search()  # update path hint dots
        for event in pygame.event.get():  # check for user inputs
            if event.type == pygame.QUIT:  # if user closes window
                pygame.quit(); sys.exit()  # shut down game
            elif event.type == pygame.KEYDOWN:  # if user presses key
                if event.key == pygame.K_UP: snake.turn((0, -1))  # turn up
                elif event.key == pygame.K_DOWN: snake.turn((0, 1))  # turn down
                elif event.key == pygame.K_LEFT: snake.turn((-1, 0))  # turn left
                elif event.key == pygame.K_RIGHT: snake.turn((1, 0))  # turn right
                elif event.key == pygame.K_h: show_hint = not show_hint  # toggle AI on/off
                elif event.key == pygame.K_r: snake.reset()  # restart game
        if snake.is_alive:  # if game is running
            snake.move()  # update snake position
            if snake.get_head_position() == food.position:  # if food eaten
                snake.score += 10  # add 10 points
                snake.grow_to += 1  # increase snake length
                food.randomize_position(snake.positions)  # move food to new spot
        screen.fill(BLACK)  # clear screen with black
        for x in range(0, WIDTH, GRID_SIZE):  # loop for vertical lines
            pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))  # draw line
        for y in range(0, HEIGHT, GRID_SIZE):  # loop for horizontal lines
            pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))  # draw line
        food.draw(screen)  # render food
        snake.draw(screen)  # render snake and AI hints
        font = pygame.font.SysFont('Arial', 20)  # set font for text
        score_txt = font.render(f"Score: {snake.score} | H: AI Hint | Arrows to Move", True, WHITE)  # create text surface
        screen.blit(score_txt, (10, 10))  # display score on screen
        if not snake.is_alive:  # if player lost
            over_txt = font.render("GAME OVER - Press 'R' to Restart", True, RED)  # create game over text
            screen.blit(over_txt, (WIDTH//2 - 120, HEIGHT//2))  # display text in center
        pygame.display.flip()  # update the full display surface
        clock.tick(10)  # control frames per second (speed)

if __name__ == "__main__":  # check if script is run directly
    main()  # start the game