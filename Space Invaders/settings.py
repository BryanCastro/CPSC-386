class Settings():
    """A class to store all settings for Alien Invasion."""

    #Static Variable
    fps = None

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings. #Default Resolution 1200x800
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        
        # Ship settings.
        self.ship_limit = 3
            
        # Bullet settings.
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = 255, 0, 0
        self.bullets_allowed = 10
        
        # Alien settings.
        self.fleet_drop_speed = 10
        self.alien_bullets_allowed = 1
        self.alien_shoot_rng = 500
        self.alien_subtract_rng = 300
            
        # How quickly the game speeds up.
        self.speedup_scale = 1.1
        # How quickly the alien point values increase.
        self.score_scale = 1.5
    
        self.initialize_dynamic_settings()

        #FPS LIMIT
        Settings.fps = 60

        #special ship spawn rate
        self.special_ship_spawn_rate = 5

        #music
        self.first_switch = False
        self.second_switch = False


    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 5
        self.alien_speed_factor = 1
        
        # Scoring.
        self.alien_points = 50
        self.special_alien_points = 1000
    
        # fleet_direction of 1 represents right, -1 represents left.
        self.fleet_direction = 1
        
    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)
