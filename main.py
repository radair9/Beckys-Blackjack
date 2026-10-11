# Welcome to your final project !!! thanks :)
import pygame
import os
import random

os.environ["SDL_AUDIODRIVER"] = "dsp"

pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 500
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Becky's Blackjack")

PLAYER_TOTAL = 0
PLAYER_CARDS = []
DEALER_TOTAL = 0
DEALER_CARDS = []

totalmoney = 500
betmoney = 10

game_started = False
waiting_for_hit = False
game_over = False
money_updated = False

name = ""
name_entered = False

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 150, 0)
RED = (200, 0, 0)
TABLE = (53, 101, 57)
GOLD = (230, 190, 60)
GREY = (100, 100, 100)

font = pygame.font.SysFont(None, 32)
smallfont = pygame.font.SysFont('Corbel', 30)
resultfont = pygame.font.SysFont(None, 50)
titlefont = pygame.font.SysFont(None, 42)

HIT_BUTTON = pygame.Rect(250, 410, 100, 45)
STAND_BUTTON = pygame.Rect(390, 410, 120, 45)
DEAL_BUTTON = pygame.Rect(50, 410, 100, 45)
MINUS_BUTTON = pygame.Rect(175, 410, 45, 45)
PLUS_BUTTON = pygame.Rect(355, 410, 45, 45)
PLAY_AGAIN_BUTTON = pygame.Rect(205, 410, 190, 45)
NAME_BOX = pygame.Rect(170, 250, 260, 45)

clock = pygame.time.Clock()
FPS = 60


def draw_text(text_to_draw, font, colour, x, y):
    text_surface = font.render(text_to_draw, True, colour)
    window.blit(text_surface, (x, y))

#hover ef/unavail button
def draw_button(rect, text, mouse_pos, enabled=True):
    if not enabled:
        button_colour = GREY
    elif rect.collidepoint(mouse_pos):
        button_colour = GREEN
    else:
        button_colour = TABLE

    pygame.draw.rect(window, button_colour, rect, border_radius=8)
    pygame.draw.rect(window, WHITE, rect, 2, border_radius=8)

    text_surface = smallfont.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    window.blit(text_surface, text_rect)


def draw_card(card, x, y):
    value = card[0]
    suit = card[1]

    pygame.draw.rect(window, WHITE, (x, y, 58, 78), border_radius=5)
    pygame.draw.rect(window, BLACK, (x, y, 58, 78), 2, border_radius=5)

    if suit == "H" or suit == "D":
        card_colour = RED
    else:
        card_colour = BLACK

    draw_text(str(value), smallfont, card_colour, x + 8, y + 5)
    draw_text(suit, smallfont, card_colour, x + 8, y + 38)


def create_deck():
    suits = ["C", "S", "H", "D"]
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

    deck = []

    for suit in suits:
        for value in values:
            deck.append((value, suit))

    random.shuffle(deck)
    return deck


def calculate_total(cards):
    total = 0
    aces = 0
#ace func
    for card in cards:
        value = card[0]

        if value == 1:
            total += 11
            aces += 1
        else:
            total += value

    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    return total


def start_game():
    global PLAYER_CARDS
    global DEALER_CARDS
    global PLAYER_TOTAL
    global DEALER_TOTAL
    global game_started
    global waiting_for_hit
    global game_over
    global money_updated
    global deck

    deck = create_deck()

    PLAYER_CARDS = []
    DEALER_CARDS = []

    PLAYER_CARDS.append(deck.pop())
    DEALER_CARDS.append(deck.pop())
    PLAYER_CARDS.append(deck.pop())
    DEALER_CARDS.append(deck.pop())

    PLAYER_TOTAL = calculate_total(PLAYER_CARDS)
    DEALER_TOTAL = calculate_total(DEALER_CARDS)

    game_started = True
    waiting_for_hit = True
    game_over = False
    money_updated = False


def dealer_play():
    global DEALER_TOTAL

    DEALER_TOTAL = calculate_total(DEALER_CARDS)

    while DEALER_TOTAL < 17:
        DEALER_CARDS.append(deck.pop())
        DEALER_TOTAL = calculate_total(DEALER_CARDS)


def update_money():
    global totalmoney
    global money_updated

    if money_updated:
        return

    if PLAYER_TOTAL > 21:
        totalmoney -= betmoney

    elif PLAYER_TOTAL == 21 and len(PLAYER_CARDS) == 2:
        totalmoney += int(betmoney * 1.5)

    elif DEALER_TOTAL > 21:
        totalmoney += betmoney

    elif PLAYER_TOTAL > DEALER_TOTAL:
        totalmoney += betmoney

    elif PLAYER_TOTAL == DEALER_TOTAL:
        totalmoney += 0

    else:
        totalmoney -= betmoney

    money_updated = True


def reset_game():
    global PLAYER_TOTAL
    global DEALER_TOTAL
    global PLAYER_CARDS
    global DEALER_CARDS
    global game_started
    global waiting_for_hit
    global game_over
    global money_updated

    PLAYER_TOTAL = 0
    DEALER_TOTAL = 0

    PLAYER_CARDS = []
    DEALER_CARDS = []

    game_started = False
    waiting_for_hit = False
    game_over = False
    money_updated = False


running = True

while running:
    window.fill(TABLE)

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #name entering out of console
        if not name_entered:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    if name.strip() != "":
                        name_entered = True

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                else:
                    if len(name) < 15:
                        name += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:

            if name_entered and not game_started:

                #betting sys
                if MINUS_BUTTON.collidepoint(event.pos):
                    if betmoney > 10:
                        betmoney -= 10

                if PLUS_BUTTON.collidepoint(event.pos):
                    if betmoney + 10 <= totalmoney:
                        betmoney += 10

                if DEAL_BUTTON.collidepoint(event.pos):
                    if totalmoney >= betmoney and totalmoney > 0:
                        start_game()

            elif waiting_for_hit:

                if HIT_BUTTON.collidepoint(event.pos):

                    if len(deck) > 0:
                        new_card = deck.pop()
                        PLAYER_CARDS.append(new_card)
                        PLAYER_TOTAL = calculate_total(PLAYER_CARDS)

                    if PLAYER_TOTAL > 21:
                        waiting_for_hit = False
                        game_over = True

                    elif PLAYER_TOTAL == 21:
                        waiting_for_hit = False
                        game_over = True

                elif STAND_BUTTON.collidepoint(event.pos):

                    dealer_play()

                    waiting_for_hit = False
                    game_over = True

            elif game_over:

                if PLAY_AGAIN_BUTTON.collidepoint(event.pos):
                    update_money()

                    if totalmoney > 0:
                        reset_game()

    if not name_entered:

        draw_text("BECKY'S BLACKJACK", titlefont, WHITE, 165, 80)
        draw_text("Enter your name to begin",font,WHITE,190,150)
        pygame.draw.rect(window,WHITE,NAME_BOX,border_radius=8)

        pygame.draw.rect(window,TABLE,NAME_BOX,3,border_radius=8)
        if name == "":
            draw_text("Name...", font, GREY, 185, 258)
        else:
            draw_text(name, font, BLACK, 185, 258)
            draw_text("Press ENTER to continue",smallfont,WHITE,200,330)

    else:

        draw_text("BECKY'S BLACKJACK",titlefont,WHITE,165,20)
        draw_text("Dealer",font,WHITE,40,78)
        draw_text("Balance: £" + str(totalmoney),font,WHITE,390,65)

        if not game_started:
            draw_text("Place your bet",font,WHITE,235,350)
            draw_button(DEAL_BUTTON,"DEAL",mouse_pos,totalmoney > 0)

            draw_button(MINUS_BUTTON,"-",mouse_pos,betmoney > 10)
            draw_button(PLUS_BUTTON,"+",mouse_pos,betmoney + 10 <= totalmoney)
            
            draw_text("BET: £" + str(betmoney),smallfont,WHITE,235,423)

           # if totalmoney <= 0:draw_text("GAME OVER - NO MONEY LEFT",font,RED,150,470)

        if game_started:

            #dcards pos
            for i in range(len(DEALER_CARDS)):
                x = 40 + (i * 62)
                #holecard
                if i == 1 and not game_over:

                    pygame.draw.rect(window,BLACK,(x, 105, 58, 78),border_radius=5)
                    pygame.draw.rect(window,WHITE,(x, 105, 58, 78),2,border_radius=5)

                    draw_text("?",font,WHITE,x + 20,125)

                else:
                    draw_card(DEALER_CARDS[i],x,105)

            #pcards positions
            for i in range(len(PLAYER_CARDS)):
                x = 40 + (i * 62)
                draw_card(PLAYER_CARDS[i],x,285)

            if game_over:
                draw_text(
                    "Dealer total: " + str(DEALER_TOTAL),font,WHITE,40,195)
            else:
                draw_text("Dealer total: ?",font,WHITE,40,195)

            draw_text(name,font,WHITE,40,260)
            draw_text("Your total: " + str(PLAYER_TOTAL),font,WHITE,40,370)

            if waiting_for_hit:
                draw_button(HIT_BUTTON,"HIT",mouse_pos)

                draw_button(STAND_BUTTON,"STAND",mouse_pos)

                draw_text(
                    "Bet: £" + str(betmoney),smallfont,WHITE,50,425)

            if game_over:

                update_money()

                pygame.draw.rect(
                    window,BLACK,(125, 135, 350, 115),border_radius=15)
                pygame.draw.rect(window,GOLD,(125, 135, 350, 115),3,border_radius=15)

                if PLAYER_TOTAL > 21:
                    draw_text("BUST!",resultfont,RED,250,160)
                    draw_text("-£" + str(betmoney),smallfont,WHITE,275,210)
                    if totalmoney <= 0:
                        draw_text("GAME OVER - NO MONEY LEFT",font,RED,150,470)
                    draw_button(PLAY_AGAIN_BUTTON,"PLAY AGAIN",mouse_pos,totalmoney > 0)
                elif PLAYER_TOTAL == 21 and len(PLAYER_CARDS) == 2:
                    draw_text("BLACKJACK!",resultfont,GOLD,205,160)
                    draw_text(
                    "+£" + str(int(betmoney * 1.5)),smallfont,WHITE,265,210)
                    draw_button(PLAY_AGAIN_BUTTON,"PLAY AGAIN",mouse_pos,totalmoney > 0)

                elif DEALER_TOTAL > 21:
                    draw_text("YOU WIN!",resultfont,WHITE,225,160)
                    draw_text("+£" + str(betmoney),smallfont,WHITE,275,210)
                    draw_button(PLAY_AGAIN_BUTTON,"PLAY AGAIN",mouse_pos,totalmoney > 0)

                elif PLAYER_TOTAL > DEALER_TOTAL:
                    draw_text("YOU WIN!",resultfont,WHITE,225,160)
                    draw_button(PLAY_AGAIN_BUTTON,"PLAY AGAIN",mouse_pos,totalmoney > 0)

                    draw_text("+£" + str(betmoney),smallfont,WHITE,275,210)
                elif PLAYER_TOTAL == DEALER_TOTAL:
                    draw_text("TIE!",resultfont,GOLD,255,160)
                    draw_text("£0",smallfont,WHITE,285,210)
                    draw_button(PLAY_AGAIN_BUTTON,"PLAY AGAIN",mouse_pos,totalmoney > 0)
                else:
                    draw_text("YOU LOSE!",resultfont,RED,215,160)
                    draw_text("-£" + str(betmoney),smallfont,WHITE,275,210)
                    if totalmoney <= 0:
                        draw_text("GAME OVER - NO MONEY LEFT",font,RED,150,470)
                    draw_button(PLAY_AGAIN_BUTTON,"PLAY AGAIN",mouse_pos,totalmoney > 0)

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()