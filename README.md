```
 _            ___  ___,  ______,      ___  , __  
(_|   |   |_// (_)/   | (_) | /|   | / (_)/|/  \ 
  |   |   |  \__ |    |     |  |___| \__   |___/ 
  |   |   |  /   |    |   _ |  |   |\/     | \   
   \_/ \_/   \___/\__/\_/(_/   |   |/\___/ |  \_/
                                                 
```

Display the current weather from the Government of Canada on a Raspberry Pi (or any machine running PyGame)

![example image](./example.png)

## Installation

### Raspberry Pi

`sudo apt-get install python3-pygame python3-xmltodict`

Set up the [PiTFT](https://www.adafruit.com/product/2298) using [these instructions form Adafruit](https://learn.adafruit.com/adafruit-pitft-28-inch-resistive-touchscreen-display-raspberry-pi/easy-install-2)

Open up `/etc/rc.local` and add

`sudo python3 /home/pi/weather/weather.py &`

### Everything Else

`pip install -r requirements.txt`


                                                 
