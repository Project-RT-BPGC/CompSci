import pygame
import pygame.locals
import webbrowser
import RAD
import os


pygame.init()

# screen resolution
'''InfoObject = pygame.display.Info()
screen_width = int(InfoObject.current_w/2)
screen_height = int(InfoObject.current_h/2)'''

# images
bits_logo = pygame.image.load(r"images\bits_2.jpg")
ncra_logo = pygame.image.load(r"images\NCRA.png")
rt_logo = pygame.image.load(r"images\rt_2.png")
bim = pygame.image.load(r"images\Space.jpg")
black_image = pygame.image.load(r"images\black.png")
black_spcae = pygame.image.load(r"images\black_space.jpg")


# screen resolution
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))


# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (50, 50, 50)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)


# Game Framerate
clock = pygame.time.Clock()
FPS = 30

# mouse_click detection
'''def on_click(x, y, button, pressed):
    if pressed:
        click = 1
    else: 
        click = 0
with Listener (on_click=on_click) as listener:
    listener.join()'''

# font


def font(text_size):
    newFont = pygame.font.SysFont("david", text_size)
    return newFont


'''class text:
    newText = ' '
    def __init__(self, message, text_size, text_colour, pos_width, pos_height):
        self.message = message
        self.text_size = text_size
        self.text_colour = text_colour
        self.pos_width = pos_width
        self.pos_height = pos_height
        #self.get_dimensions()
        self.draw()


    # text_format function
    def text_format(self, message, text_size, text_colour):
        newFont = font(self.text_size)
        self.newText = newFont.render(self.message, 0, self.text_colour)

    def draw(self):
        #text_rect = self.get_dimensions()
        screen.blit(screen, self.newText, (int(self.pos_width - self.newText.get_rect()[2]/2), int(self.pos_height)))

    def get_dimensions(self):
        text_rect = self.newText.get_rect()
        return text_rect'''


def text_format(message, text_size, text_colour):
    newFont = pygame.font.SysFont("david", text_size)
    newText = newFont.render(message, 0, text_colour)
    return newText


# sending RA_dec and Alt_az data
def send_data():
    return
    # main menu


def main_menu():
    menu = True
    selected = "Track"
    welcome_message = text_format("Welcome to Project RT!", 60, white)

    while menu:

        pressed = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()
        clicked = 0

        pygame.display.set_caption("Project RT")
        screen.fill(white)
        screen.fill(black, (0.4*screen_width, 0,
                            screen.get_width(), screen.get_height()))
        screen.blit(rt_logo, (0.05*screen_width, 0.0625*screen_height))
        screen.blit(bits_logo, (0.25*screen_width, 0.09375*screen_height))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if selected == "Track":
                        selected = "Map"
                    elif selected == "Map":
                        selected = "RAT"
                    elif selected == "RAT":
                        selected = "History"
                    elif selected == "History":
                        selected = "ATP"
                    elif selected == "ATP":
                        selected = "Track"

                elif event.key == pygame.K_UP:
                    if selected == "Track":
                        selected = "ATP"
                    elif selected == "Map":
                        selected = "Track"
                    elif selected == "RAT":
                        selected = "Map"
                    elif selected == "History":
                        selected = "RAT"
                    elif selected == "ATP":
                        selected = "History"

            if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN:
                if selected == "ATP":
                    webbrowser.open(
                        'https://projectrtbits.wordpress.com/', new=2)
                elif selected == "RAT":
                    RAT()

            if pygame.Rect(0.25*screen_width, 0.09375*screen_height, bits_logo.get_rect()[2], bits_logo.get_rect()[3]).collidepoint(pos) and event.type == pygame.MOUSEBUTTONDOWN:
                webbrowser.open("https://www.bits-pilani.ac.in/Goa/", new=2)

        # text rendering
        track_text = text_format("Track", 40, black)
        map_text = text_format("Map", 40, black)
        RAT_text = text_format("RA-Dec To ALT-Az", 40, black)
        history_text = text_format("History", 40, black)
        ATP_text = text_format("About the project", 40, black)

        welcome_message_rect = welcome_message.get_rect()
        track_rect = track_text.get_rect()
        map_rect = map_text.get_rect()
        RAT_rect = RAT_text.get_rect()
        history_rect = history_text.get_rect()
        ATP_rect = ATP_text.get_rect()

        # Mouse input
        if pygame.Rect((0.2*screen_width - int(track_rect[2] / 2)), 0.3125*screen_height, track_rect[2], track_rect[3]).collidepoint(pos) and pressed or selected == "Track":
            track_text = text_format("Track", 40, black)
            pygame.draw.rect(screen, black, ((0.2*screen_width - int(track_rect[2] / 2)), int(
                0.3125*screen_height), track_rect[2], track_rect[3]), 2)
            selected = "Track"
        if pygame.Rect((200 - int(map_rect[2] / 2)), 330, map_rect[2], map_rect[3]).collidepoint(pos) and pressed or selected == "Map":
            map_text = text_format("Map", 40, black)
            pygame.draw.rect(screen, black, ((
                195 - int(map_rect[2] / 2)), 330, map_rect[2] + 10, map_rect[3]), 2)
            selected = "Map"
        if pygame.Rect((200-int(RAT_rect[2] / 2)), 410, RAT_rect[2], RAT_rect[3]).collidepoint(pos) and pressed or selected == "RAT":
            RAT_text = text_format("RA-Dec to ALT-Az", 40, black)
            pygame.draw.rect(screen, black, ((
                195-int(RAT_rect[2] / 2)), 410, RAT_rect[2] + 10, RAT_rect[3]), 2)
            selected = "RAT"
        if pygame.Rect((200-int(history_rect[2]/2)), 490, history_rect[2], history_rect[3]).collidepoint(pos) and pressed or selected == "History":
            history_text = text_format("History", 40, black)
            pygame.draw.rect(screen, black, ((
                195-int(history_rect[2]/2)), 490, history_rect[2] + 10, history_rect[3]), 2)
            selected = "History"
        if pygame.Rect((200 - int(ATP_rect[2] / 2)), 570, ATP_rect[2], ATP_rect[3]).collidepoint(pos) and pressed or selected == "ATP":
            ATP_text = text_format("About the Project", 40,  black)
            pygame.draw.rect(screen, black, ((
                195 - int(ATP_rect[2] / 2)), 570, ATP_rect[2] + 10, ATP_rect[3]), 2)
            selected = "ATP"

        screen.blit(
            welcome_message, ((700-int(welcome_message_rect[2]/2)), int(screen_height/4)))
        screen.blit(track_text, ((200 - int(track_rect[2] / 2)), 250))
        screen.blit(map_text, ((200 - int(map_rect[2] / 2)), 330))
        screen.blit(RAT_text, ((200 - int(RAT_rect[2] / 2)), 410))
        screen.blit(history_text, ((200 - int(history_rect[2] / 2)), 490))
        screen.blit(ATP_text, ((200 - int(ATP_rect[2] / 2)), 570))
        pygame.display.update()
        clock.tick(FPS)


def RAT():
    RAT = True
    text_RAT = text_format("RA-Dec to Alt-Az converter", 70, white)
    text_RAT_rect = text_RAT.get_rect()

    lat_text = text_format("Enter the Latitude(in degrees):", 40, white)
    lat_rect = lat_text.get_rect()

    long_text = text_format(
        "Enter the current Longitude(in degrees):", 40, white)
    long_rect = long_text.get_rect()
    io_rect = pygame.Rect(
        (int(screen_width/4 + lat_rect[2]/2), int(screen_height/8 + 100), 200, lat_rect[3]))

    convert_text = text_format("CONVERT", 80, gray)
    convert_text_rect = convert_text.get_rect()

    # get converted values
    get_values = text_format('Get Values', 80, gray)
    get_values_text_rect = get_values.get_rect()

    active = 0
    convert = 0

    text_lat_render = text_format('', 30, white)
    text_long_render = text_format('', 30, white)

    text_lat = '0.0'
    text_long = '0.0'

    while RAT:
        pos = pygame.mouse.get_pos()
        screen.fill(black)
        screen.blit(black_spcae, (0, 0))

        lat_rect_io = pygame.Rect(
            (int(screen_width/4 + lat_rect[2]/2 + 5), int(screen_height/8 + 100), 200, lat_rect[3]))
        long_rect_io = pygame.Rect(
            (int(screen_width/4 - lat_rect[2]/2 + long_rect[2] + 5), int(screen_height/8 + 200), 200, long_rect[3]))
        convert_rect = pygame.Rect((int(screen_width/4 - convert_text_rect[2]/2), int(
            screen_height/2 + 200), int(convert_text_rect[2]+10), int(convert_text_rect[3]+10)))
        get_values_rect = pygame.Rect((int(screen_width/4 + get_values_text_rect[2]), int(
            screen_height/2 + 200), int(get_values_text_rect[2]+10), int(get_values_text_rect[3]+10)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if lat_rect_io.collidepoint(pos):
                    active = 1
                    #io_rect = lat_rect_io
                elif long_rect_io.collidepoint(pos):
                    active = 2
                    #io_rect = long_rect_io
                elif convert_rect.collidepoint(pos):
                    convert = 1
                elif get_values_rect.collidepoint(pos):
                    send_data()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if active == 1:
                        active = 2
                    else:
                        convert = 1  # UNDO THIS COMMENT TO EXECUTE CONVERT ON PRESSING ENTER

                elif event.key == pygame.K_BACKSPACE:
                    if active == 1:
                        text_lat = text_lat[:-1]
                    else:
                        text_long = text_long[:-1]
                elif event.key == pygame.K_ESCAPE:
                    main_menu()
                else:
                    if active == 1:
                        text_lat += event.unicode
                    else:
                        text_long += event.unicode

        if active == 1:
            text_lat_render = text_format(text_lat, 30, white)
        elif active == 2:
            text_long_render = text_format(text_long, 30, white)

        if convert == 1:
            RAD.convert(float(text_lat), float(text_long))

        lat_rect_io.w = max(200, text_lat_render.get_width()+10)
        long_rect_io.w = max(200, text_long_render.get_width()+10)

        pygame.draw.rect(screen, white, lat_rect_io, 2)
        pygame.draw.rect(screen, white, long_rect_io, 2)
        pygame.draw.rect(screen, gray, convert_rect, 2)
        pygame.draw.rect(screen, gray, get_values_rect, 2)

        if convert_rect.collidepoint(pos):
            pygame.draw.rect(screen, white, convert_rect, 2)
            convert_text = text_format("CONVERT", 80, white)
        else:
            convert_text = text_format("CONVERT", 80, gray)

        screen.blit(
            text_RAT, (int(screen_width/2 - text_RAT_rect[2]/2), int(screen_height/8)),)
        screen.blit(
            lat_text, (int(screen_width/4 - lat_rect[2]/2), int(screen_height/8 + 100)))
        screen.blit(
            long_text, (int(screen_width/4 - lat_rect[2]/2), int(screen_height/8 + 200)))
        screen.blit(convert_text, (convert_rect.x+5, convert_rect.y+5))
        screen.blit(text_lat_render, (lat_rect_io.x+5, lat_rect_io.y+5))
        screen.blit(text_long_render, (long_rect_io.x+5, long_rect_io.y+5))

        screen.blit(get_values, (get_values_rect.x+5, get_values_rect.y+5))

        # writing the values to a new file
        file = open("rad_dec_values.txt", "a")
        file.write(text_lat+" "+text_long+'\n')
        file.close()

        pygame.display.update()
        clock.tick(FPS)


main_menu()
pygame.quit()
quit()
