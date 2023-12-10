import pygame
import sys
import time

from minesweeper import Minesweeper, MinesweeperAI

HEIGHT = 16
WIDTH = 16
MINES = 30

# Colors
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)
BLUE = (95, 162, 170)
BLUE2 = (169, 216, 214)
PINK = (255, 192, 203)
RED = (255, 0, 0)

# Create game
pygame.init()
size = width, height = 1200, 720
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Minesweeper")

# Fonts
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
GAMEFONT = "assets/fonts/04B_30__.TTF"
smallFont = pygame.font.Font(OPEN_SANS, 18)
mediumFont = pygame.font.Font(GAMEFONT, 24)
largeFont = pygame.font.Font(GAMEFONT, 32)

# Compute board size
BOARD_PADDING = 20
board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)

# Add images
flag = pygame.image.load("assets/images/flag.png")
flag = pygame.transform.scale(flag, (cell_size, cell_size))
mine = pygame.image.load("assets/images/mine1.png")
mine = pygame.transform.scale(mine, (cell_size, cell_size))
mine_red = pygame.image.load("assets/images/mine-red2.png")
mine_red = pygame.transform.scale(mine_red, (cell_size, cell_size))
minesweeper = pygame.image.load("assets/images/minesweeper.png")
minesweeper = pygame.transform.scale(minesweeper, (300, 300))

# Detonated mine
mine_detonated = None

# Create game and AI agent
game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
ai = MinesweeperAI(height=HEIGHT, width=WIDTH)

# Keep track of revealed cells, flagged cells, and if a mine was hit
revealed = set()
flags = set()
lost = False

# Show instructions initially
instructions = True

# Show Safe and Mine Cells
showInference = True

while True:

    # Check if game quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BLUE2)

    # Show game instructions
    if instructions:
        # Title
        title = largeFont.render("Play Minesweeper", True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Rules
        rules = [
            "Click a cell to reveal it.",
            "Right-click a cell to mark it as a mine.",
            "Mark all mines successfully to win!"
        ]
        for i, rule in enumerate(rules):
            line = mediumFont.render(rule, True, WHITE)
            lineRect = line.get_rect()
            lineRect.center = ((width / 2), 150 + 30 * i)
            screen.blit(line, lineRect)
        
        screen.blit(minesweeper, (width/2-150, height/2-100))

        # Play game button
        buttonRect = pygame.Rect((width / 4), (3 / 4) * height+50, width / 2, 50)
        buttonText = mediumFont.render("Play Game", True, WHITE)
        buttonTextRect = buttonText.get_rect()
        buttonTextRect.center = buttonRect.center
        pygame.draw.rect(screen, BLUE, buttonRect)
        screen.blit(buttonText, buttonTextRect)

        # Check if play button clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if buttonRect.collidepoint(mouse):
                instructions = False
                time.sleep(0.3)

        pygame.display.flip()
        continue

    # Draw board
    cells = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):

            # Draw rectangle for cell
            rect = pygame.Rect(
                board_origin[0] + j * cell_size,
                board_origin[1] + i * cell_size,
                cell_size, cell_size
            )
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLUE2, rect, 3)

            # Add a mine, flag, or number if needed
            if game.is_mine((i, j)) and lost:
                if (i,j) == mine_detonated:
                    screen.blit(mine_red, rect)
                else:
                    screen.blit(mine, rect)
            elif (i, j) in flags:
                screen.blit(flag, rect)
            elif (i, j) in revealed:
                color = BLACK
                if game.nearby_mines((i, j)) > 0:
                    if game.nearby_mines((i, j)) == 1:
                        color = (0, 0, 255)
                    elif game.nearby_mines((i, j)) == 2:
                        color = (143, 26, 216)
                    elif game.nearby_mines((i, j)) >= 3:
                        color = (255, 0, 0)
                neighbors = smallFont.render(
                    str(game.nearby_mines((i, j))),
                    True, color
                )
                neighborsTextRect = neighbors.get_rect()
                neighborsTextRect.center = rect.center
                screen.blit(neighbors, neighborsTextRect)
            elif (i, j) in ai.safes and showInference:
                pygame.draw.rect(screen, PINK, rect)
                pygame.draw.rect(screen, BLUE2, rect, 3)
            elif (i, j) in ai.mines and showInference:
                pygame.draw.rect(screen, RED, rect)
                pygame.draw.rect(screen, BLUE2, rect, 3)
            row.append(rect)
        cells.append(row)

    
    # Reset button
    resetButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, BOARD_PADDING + 10,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    buttonText = mediumFont.render("Reset", True, WHITE)
    buttonRect = buttonText.get_rect()
    buttonRect.center = resetButton.center
    pygame.draw.rect(screen, BLUE, resetButton)
    screen.blit(buttonText, buttonRect)

# Show Safes and Mines button
    safesMinesButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, BOARD_PADDING + 100,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    bText = "Show Inference" if not showInference else "Hide Inference"
    buttonText = mediumFont.render(bText, True, WHITE)
    buttonRect = buttonText.get_rect()
    buttonRect.center = safesMinesButton.center
    pygame.draw.rect(screen, BLUE, safesMinesButton)
    screen.blit(buttonText, buttonRect)

    move = None

    left, _, right = pygame.mouse.get_pressed()

    # Display text
    text = "You Lose" if lost else "You Won!!" if game.mines == flags else ""
    text = mediumFont.render(text, True, WHITE)
    textRect = text.get_rect()
    textRect.center = ((5 / 6) * width, BOARD_PADDING + 400)
    screen.blit(text, textRect)

    #screen.blit(gopal, ((2 / 3) * width + BOARD_PADDING, BOARD_PADDING + 200))

    # Check for a right-click to toggle flagging
    if right == 1 and not lost:
        mouse = pygame.mouse.get_pos()
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if cells[i][j].collidepoint(mouse) and (i, j) not in revealed:
                    if (i, j) in flags:
                        flags.remove((i, j))
                    else:
                        flags.add((i, j))
                    time.sleep(0.2)

    elif left == 1:
        mouse = pygame.mouse.get_pos()

        # Reset game state
        if resetButton.collidepoint(mouse):
            game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
            ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
            revealed = set()
            flags = set()
            lost = False
            mine_detonated = None
            continue

        # If Inference button clicked, toggle showInference
        elif safesMinesButton.collidepoint(mouse):
            showInference = not showInference
            time.sleep(0.2)

        # User-made move
        elif not lost:
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if (cells[i][j].collidepoint(mouse)
                            and (i, j) not in flags
                            and (i, j) not in revealed):
                        move = (i, j)

    # Make move and update AI knowledge
    if move:
        if game.is_mine(move):
            lost = True
            mine_detonated = move
        else:
            nearby = game.nearby_mines(move)
            revealed.add(move)
            ai.add_knowledge(move, nearby)

    pygame.display.flip()
