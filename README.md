# 🔥 Ultimate Facebook Scrapper


[![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](#)
[![GitHub Forks](https://img.shields.io/github/forks/vigilantee/Ultimate-Facebook-Scraper.svg?style=social&label=Fork&maxAge=2592000)](https://www.github.com/vigilantee/Ultimate-Facebook-Scraper/fork)
[![Build Status](https://semaphoreapp.com/api/v1/projects/d4cca506-99be-44d2-b19e-176f36ec8cf1/128505/badge.svg)](#)
[![GitHub Issues](https://img.shields.io/github/issues/vigilantee/Ultimate-Facebook-Scraper.svg?style=flat&label=Issues&maxAge=2592000)](https://www.github.com/vigilantee/Ultimate-Facebook-Scraper/issues)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat&label=Contributions&colorA=red&colorB=black	)](#)


A bot which scrapes almost everything about a facebook user's profile including

* uploaded photos
* tagged photos
* videos
* friends list and their profile photos (including Followers, Following, Work Friends, College Friends etc)
* and all public posts/statuses available on the user's timeline.

The best thing about this scraper is that the data is scraped in an organized format so that it can be used for educational/research purpose by researchers. Moreover, this scraper does not use Facebook's Graph API so there are no rate limiting issues as such. 

## Sample
<p align="middle">
  <img src="../master/images/main.png" width="700"/>
 </p>


## Screenshot
<p align="middle">
  <img src="../master/images/screenshot.png" width="700"/>
 </p>


----------------------------------------------------------------------------------------------------------------------------------------
## Usage

### Installation
You will need to install latest version of [Google Chrome](https://www.google.com/chrome/). Moreover, you need to install selenium module as well using

```
pip install selenium
```

Run the code using Python 3. Also, the code is multi-platform and is tested on both Windows and Linux.
The tool uses latest version of [Chrome Web Driver](http://chromedriver.chromium.org/downloads). I have placed the webdriver along with the code but if that version doesn't work then replace the chrome web driver with the latest one.

### How to Run
There's a file named "input.txt". You can add as many profiles as you want in the following format with each link on a new line:

```
https://www.facebook.com/andrew.ng.96
https://www.facebook.com/zuck
```

Make sure the link only contains the username or id number at the end and not any other stuff. Make sure its in the format mentioned above.

Note: There are two modes to download Friends Profile Pics and the user's Photos: Large Size and Small Size. You can change the following variables. By default they are set to Small Sized Pics because its really quick while Large Size Mode takes time depending on the number of pictures to download

```
# whether to download the full image or its thumbnail (small size)
# if small size is True then it will be very quick else if its False then it will open each photo to download it
# and it will take much more time
friends_small_size = True
photos_small_size = True
```

----------------------------------------------------------------------------------------------------------------------------------------

## Note
This tool is for research purposes only. Hence, the developers of this tool won't be responsible for any misuse of data collected using this tool. 

----------------------------------------------------------------------------------------------------------------------------------------

## Author
You can get in touch with me on my LinkedIn Profile: [![LinkedIn Link](https://img.shields.io/badge/Connect-vigilantee-blue.svg?logo=linkedin&longCache=true&style=social&label=Connect
)](https://www.linkedin.com/in/abhishekjha007)

You can also follow my GitHub Profile to stay updated about my latest projects: [![GitHub Follow](https://img.shields.io/badge/Connect-vigilantee-blue.svg?logo=Github&longCache=true&style=social&label=Follow)](https://github.com/vigilantee)

If you liked the repo then kindly support it by giving it a star ⭐!

## Contributions Welcome
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](#)

If you find any bug in the code or have any improvements in mind then feel free to generate a pull request.

## Issues
[![GitHub Issues](https://img.shields.io/github/issues/vigilantee/Ultimate-Facebook-Scraper.svg?style=flat&label=Issues&maxAge=2592000)](https://www.github.com/vigilantee/Ultimate-Facebook-Scraper/issues)

If you face any issue, you can create a new issue in the Issues Tab and I will be glad to help you out.

## License
[![MIT](https://img.shields.io/cocoapods/l/AFNetworking.svg?style=style&label=License&maxAge=2592000)](../master/LICENSE)

Copyright (c) 2018-present, abhishek jha, vigilantee                                                        
