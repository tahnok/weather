import pygame
import os
import urllib.request, urllib.error, urllib.parse
import xmltodict
from time import sleep, localtime, strftime

def fetch():
    remote = urllib.request.urlopen('http://dd.weather.gc.ca/citypage_weather/xml/ON/s0000430_e.xml')
    # remote = open('sample.xml', 'r')
    raw = remote.read()
    remote.close()

    parsed = xmltodict.parse(raw)
    return parsed

if os.path.isfile("/sys/firmware/devicetree/base/model"):
    os.putenv('SDL_FBDEV', '/dev/fb1')

pygame.init()
pygame.mouse.set_visible(False)
lcd = pygame.display.set_mode((320, 240))
lcd.fill((0,0,0))
pygame.display.update()

font_big = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)


while True:
    lcd.fill((0,0,0))

    try:
        parsed = fetch()
    except Exception as e:
        sleep(60 * 60)
        next

    temperature = parsed['siteData']['currentConditions']['temperature']['#text']
    temperature_surface = font_big.render("%s C" % temperature, True, (255,255,255))
    rect = temperature_surface.get_rect(center=(60,40))
    lcd.blit(temperature_surface, rect)

    if 'windChill' in parsed['siteData']['currentConditions']:
        wind_chill = parsed['siteData']['currentConditions']['windChill']['#text']
        wind_chill_surface = font_large.render("%s C" % wind_chill, True, (255,255,255))
        rect = wind_chill_surface.get_rect(center=(60,70))
        lcd.blit(wind_chill_surface, rect)

    conditions = parsed['siteData']['currentConditions']['condition']
    conditions_surface = font_medium.render("%s" % conditions, True, (255,255,255))
    rect = conditions_surface.get_rect(topleft=(20,100))
    lcd.blit(conditions_surface, rect)

    forecast = parsed['siteData']['forecastGroup']['forecast'][0]['abbreviatedForecast']['textSummary']
    forecast_surface = font_small.render("%s" % forecast, True, (255,255,255))
    rect = forecast_surface.get_rect(topleft=(20,140))
    lcd.blit(forecast_surface, rect)

    image_code = parsed['siteData']['forecastGroup']['forecast'][0]['abbreviatedForecast']['iconCode']['#text']
    image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images/%s.gif' % image_code)
    image = pygame.image.load(image_path)
    rect = image.get_rect(topleft=(240,20))
    lcd.blit(image, rect)

    # Will be wrong at night, need to go only one forward
    tomorrow_forecast = parsed['siteData']['forecastGroup']['forecast'][2]['abbreviatedForecast']['textSummary']
    tomorrow_forecast_surface = font_small.render("Tomorrow: %s" % tomorrow_forecast, True, (255,255,255))
    rect = tomorrow_forecast_surface.get_rect(topleft=(20,200))
    lcd.blit(tomorrow_forecast_surface, rect)

    time = strftime("%H:%M", localtime())
    time_text = font_small.render("%s" % time, True, (255,255,255))
    rect = time_text.get_rect(topleft=(260,220))
    lcd.blit(time_text, rect)

    pygame.display.update()
    sleep(60 * 60)

