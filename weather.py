import os
from time import sleep, localtime, strftime
import urllib

import pygame
import xmltodict

def main():
    renderer = Renderer()

    while True:
        renderer.clear()

        try:
            parsed = fetch()
        except Exception as e:
            sleep(60 * 60)
            continue

        temperature = parsed['siteData']['currentConditions']['temperature']['#text']
        renderer.draw_text("Now: %s C" % temperature, "big", "center", 60, 40)

        if 'windChill' in parsed['siteData']['currentConditions']:
            wind_chill = parsed['siteData']['currentConditions']['windChill']['#text']
            renderer.draw_text("%s C" % wind_chill, "medium", "center", 60, 70)

        conditions = parsed['siteData']['currentConditions']['condition']
        renderer.draw_text(conditions, "medium", "topleft", 20, 100)

        forecast = parsed['siteData']['forecastGroup']['forecast'][0]['abbreviatedForecast']['textSummary']
        renderer.draw_text("Later: %s" % forecast, "medium", "topleft", 20, 140)

        image_code = parsed['siteData']['forecastGroup']['forecast'][0]['abbreviatedForecast']['iconCode']['#text']
        renderer.draw_image(image_code)

        # Will be wrong at night, need to go only one forward
        tomorrow_forecast = parsed['siteData']['forecastGroup']['forecast'][2]['abbreviatedForecast']['textSummary']
        renderer.draw_text("Tomorrow: %s" % tomorrow_forecast, "small", "topleft", 20, 200)

        time = strftime("%H:%M", localtime())
        renderer.draw_text(time, "small", "topleft", 260, 220)

        renderer.draw()
        sleep(60 * 60)

def fetch():
    remote = urllib.request.urlopen(
        'http://dd.weather.gc.ca/citypage_weather/xml/ON/s0000430_e.xml'
    )
    # remote = open('sample.xml', 'r')
    raw = remote.read()
    remote.close()

    parsed = xmltodict.parse(raw)
    return parsed

class Renderer:
    white = (255, 255, 255)
    black = (0, 0, 0)

    def __init__(self):
        if os.path.isfile("/sys/firmware/devicetree/base/model"):
            os.putenv('SDL_FBDEV', '/dev/fb1')

        pygame.init()
        pygame.mouse.set_visible(False)
        self.lcd = pygame.display.set_mode((320, 240))
        self.lcd.fill((0, 0, 0))
        pygame.display.update()

        self.font_big = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)

    def clear(self):
        self.lcd.fill(self.black)

    def draw(self):
        pygame.display.update()

    def draw_text(self, text, size, align, x, y):
        if size == "big":
            text_surface = self.font_big.render(text, True, self.white)
        elif size == "medium":
            text_surface = self.font_medium.render(text, True, self.white)
        elif size == "small":
            text_surface = self.font_small.render(text, True, self.white)
        else:
            raise "Unknown size"

        if align == "center":
            rect = text_surface.get_rect(center=(x,y))
        elif align == "topleft":
            rect = text_surface.get_rect(topleft=(x,y))

        self.lcd.blit(text_surface, rect)

    def draw_image(self, code):
        image_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'images/%s.gif' % code
        )
        image = pygame.image.load(image_path)
        rect = image.get_rect(topleft=(240, 20))
        self.lcd.blit(image, rect)

if __name__ == "__main__":
    main()
