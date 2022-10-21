import globals

from game.casting.actor import Actor
from game.casting.cast import Cast
from game.casting.fleet import Fleet

from game.directing.director import Director

from game.services.keyboard_service import KeyboardService
from game.services.video_service import VideoService

from game.shared.point import Point



def main():
    
    # create the cast
    cast = Cast()
    
    # create the banners - first the player's message area
    banner = Actor()
    banner.set_text("")
    banner.set_font_size(globals.FONT_SIZE)
    banner.set_color(globals.GREEN)
    banner.set_position(Point(globals.CELL_SIZE, globals.MAX_Y - globals.CELL_SIZE))
    cast.add_actor("banners", banner)

    # create the enemy banner area
    banner = Actor()
    banner.set_text("")
    banner.set_font_size(globals.FONT_SIZE)
    banner.set_color(globals.RED_BOLD)
    banner.set_position(Point(globals.MAX_X - (globals.CELL_SIZE * 15), globals.MAX_Y - globals.CELL_SIZE))
    cast.add_actor("banners", banner)
    
    # create the cursor position
    x = int(globals.MAX_X / 2)
    y = int(globals.MAX_Y / 4)
    position = Point(x, y)

    # create the cursor
    cursor = Actor()
    cursor.set_text("+")
    cursor.set_font_size(globals.FONT_SIZE)
    cursor.set_color(globals.WHITE)
    cursor.set_position(position)
    cast.add_actor("cursors", cursor)

    # creat the divider
    y = int(globals.MAX_Y / 2)
    for n in range(0, globals.MAX_X, globals.CELL_SIZE):
        divider = Actor()
        divider.set_text("-")
        divider.set_font_size(globals.FONT_SIZE)
        divider.set_color(globals.YELLOW)
        divider.set_position(Point(n, y))
        cast.add_actor("dividers", divider)

    # create the enemy fleet in top half of screen, color red (invisible)
    ships= Fleet(cast)
    enemies = ships.get_ships("enemy_ships")
    defenders = ships.get_ships("defense_ships")
    results = []
    for enemy in enemies:
        results.extend(enemy)
    for i in range(len(results)):
        cast.add_actor("enemy_ships", results[i])
    results = []
    for defender in defenders:
        results.extend(defender)
    for i in range(len(results)):
        cast.add_actor("defense_ships", results[i])
    
    # start the game
    keyboard_service = KeyboardService(globals.CELL_SIZE)
    video_service = VideoService(globals.CAPTION, globals.MAX_X, \
        globals.MAX_Y, globals.CELL_SIZE, globals.FRAME_RATE)
    director = Director(keyboard_service, video_service)
    director.start_game(cast)


if __name__ == "__main__":
    main()