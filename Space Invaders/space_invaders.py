import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from sprite_sheet import SpriteSheet
import game_functions as gf
from explosion import Explosion
from main_menu import Main_Menu
from special_ship import Special_Ship
from sounds import Sounds


def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #create clock
    clock = pygame.time.Clock()

    # Make the Play button.
    play_button = Button(ai_settings, screen, "Play")

    # Load Sprite Sheet
    sprite_sheet = SpriteSheet("images/SpriteSheet/Space_Invaders_SS.png", 7, 3)

    # Create an instance to store game statistics, and a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats, sprite_sheet)
    
    # Set the background color.
    bg_color = (0, 0, 0)

    # Make a ship, a group of bullets, and a group of aliens.
    ship = Ship(ai_settings, screen, sprite_sheet)
    bullets = Group()
    aliens = Group()
    alien_bullets = Group()
    explosions = []
    #special_ship = Special_Ship(screen, sprite_sheet)
    special_ships = Group()

    #make main menu
    main_menu = Main_Menu(screen, sprite_sheet)

    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens, sprite_sheet)

    # Start the main loop for the game.
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
            aliens, bullets, sprite_sheet)


        if stats.game_active:
            gf.update_screen(ai_settings, screen, stats, sb, ship, aliens,
                             bullets, play_button, explosions, sprite_sheet, alien_bullets, main_menu, special_ships)
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                bullets, explosions, sprite_sheet, special_ships)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,
                bullets, sprite_sheet, special_ships)
        else:
            screen.fill(bg_color)
            #special_ship.movement()
            #special_ship.blit_special_ship()
            main_menu.render_menu()

        clock.tick(Settings.fps)


run_game()


###Left off alien class, shoot_function