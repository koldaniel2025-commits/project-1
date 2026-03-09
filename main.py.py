import pygame
import sys

WIDTH, HEIGHT = 450, 600
BOARD_SIZE = 450
SQUARE_SIZE = BOARD_SIZE // 3
LINE_WIDTH = 10

BG_COLOR = (5, 5, 15)
GRID_COLOR = (25, 25, 50)
X_COLOR = (255, 0, 120)
X_GLOW = (80, 0, 40)
O_COLOR = (0, 255, 255)
O_GLOW = (0, 60, 80)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# שימוש בפונט מערכת ברירת מחדל למניעת שגיאות טעינה
font = pygame.font.SysFont(None, 40, bold=True)
small_font = pygame.font.SysFont(None, 25, bold=True)

board = [[None]*3 for _ in range(3)]
player = 'X'
game_over = False
winner = None
win_line = None
settings_active = False
scores = {'X': 0, 'O': 0}

settings_btn = pygame.Rect(10, 540, 110, 40)
resume_btn = pygame.Rect(125, 200, 200, 60)
restart_btn = pygame.Rect(125, 280, 200, 60)

def check_winner():
    global winner, win_line, game_over
    for r in range(3):
        if board[r][0] == board[r][1] == board[r][2] and board[r][0]:
            winner, win_line, game_over = board[r][0], ('h', r), True
            scores[winner] += 1
            return
    for c in range(3):
        if board[0][c] == board[1][c] == board[2][c] and board[0][c]:
            winner, win_line, game_over = board[0][c], ('v', c), True
            scores[winner] += 1
            return
    if board[0][0] == board[1][1] == board[2][2] and board[0][0]:
        winner, win_line, game_over = board[0][0], ('d1', 0), True
        scores[winner] += 1
        return
    if board[0][2] == board[1][1] == board[2][0] and board[0][2]:
        winner, win_line, game_over = board[0][2], ('d2', 0), True
        scores[winner] += 1
        return
    if all(all(row) for row in board):
        winner, game_over = 'Draw', True

def draw_neon_marker(r, c, type):
    center = (c*SQUARE_SIZE + SQUARE_SIZE//2, r*SQUARE_SIZE + SQUARE_SIZE//2)
    if type == 'X':
        off = 50
        p1 = (c*SQUARE_SIZE+off, r*SQUARE_SIZE+off)
        p2 = (c*SQUARE_SIZE+SQUARE_SIZE-off, r*SQUARE_SIZE+SQUARE_SIZE-off)
        p3 = (c*SQUARE_SIZE+off, r*SQUARE_SIZE+SQUARE_SIZE-off)
        p4 = (c*SQUARE_SIZE+SQUARE_SIZE-off, r*SQUARE_SIZE+off)
        pygame.draw.line(screen, X_GLOW, p1, p2, 22)
        pygame.draw.line(screen, X_GLOW, p3, p4, 22)
        pygame.draw.line(screen, X_COLOR, p1, p2, 10)
        pygame.draw.line(screen, X_COLOR, p3, p4, 10)
    else:
        pygame.draw.circle(screen, O_GLOW, center, SQUARE_SIZE//2 - 40, 18)
        pygame.draw.circle(screen, O_COLOR, center, SQUARE_SIZE//2 - 40, 8)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            settings_active = not settings_active
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_pos = event.pos
            if settings_btn.collidepoint(m_pos):
                settings_active = not settings_active
            elif settings_active:
                if resume_btn.collidepoint(m_pos): settings_active = False
                if restart_btn.collidepoint(m_pos):
                    board = [[None]*3 for _ in range(3)]
                    player, game_over, winner, win_line, settings_active = 'X', False, None, None, False
            elif not game_over and m_pos[1] < BOARD_SIZE:
                r, c = m_pos[1]//SQUARE_SIZE, m_pos[0]//SQUARE_SIZE
                if r < 3 and c < 3 and board[r][c] is None:
                    board[r][c] = player
                    check_winner()
                    player = 'O' if player == 'X' else 'X'

    screen.fill(BG_COLOR)
    
    for i in range(1, 3):
        pygame.draw.line(screen, GRID_COLOR, (0, i*SQUARE_SIZE), (BOARD_SIZE, i*SQUARE_SIZE), 4)
        pygame.draw.line(screen, GRID_COLOR, (i*SQUARE_SIZE, 0), (i*SQUARE_SIZE, BOARD_SIZE), 4)
    
    for r in range(3):
        for c in range(3):
            if board[r][c]: draw_neon_marker(r, c, board[r][c])

    if win_line:
        t, p = win_line
        mid = p*SQUARE_SIZE+SQUARE_SIZE//2
        if t == 'h': pygame.draw.line(screen, WHITE, (20, mid), (BOARD_SIZE-20, mid), 6)
        elif t == 'v': pygame.draw.line(screen, WHITE, (mid, 20), (mid, BOARD_SIZE-20), 6)
        elif t == 'd1': pygame.draw.line(screen, WHITE, (30, 30), (BOARD_SIZE-30, BOARD_SIZE-30), 6)
        elif t == 'd2': pygame.draw.line(screen, WHITE, (BOARD_SIZE-30, 30), (30, BOARD_SIZE-30), 6)

    pygame.draw.rect(screen, (20, 20, 40), (0, 450, WIDTH, 150))
    pygame.draw.rect(screen, YELLOW, settings_btn, border_radius=8)
    st_label = small_font.render("SETTINGS", True, BLACK)
    screen.blit(st_label, (settings_btn.x+15, settings_btn.y+10))
    
    screen.blit(small_font.render(f"X SCORE: {scores['X']}", True, X_COLOR), (20, 470))
    screen.blit(small_font.render(f"O SCORE: {scores['O']}", True, O_COLOR), (WIDTH-140, 470))
    
    msg = "DRAW!" if winner == 'Draw' else f"{winner} WINS!" if winner else f"NEXT: {player}"
    color = YELLOW if winner else (X_COLOR if player == 'X' else O_COLOR)
    txt_surf = font.render(msg, True, color)
    screen.blit(txt_surf, txt_surf.get_rect(center=(WIDTH//2, 520)))

    if settings_active:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        screen.blit(overlay, (0,0))
        for btn, txt in [(resume_btn, "RESUME"), (restart_btn, "RESTART")]:
            pygame.draw.rect(screen, YELLOW, btn, border_radius=15)
            btn_txt = font.render(txt, True, BLACK)
            screen.blit(btn_txt, btn_txt.get_rect(center=btn.center))

    pygame.display.flip()