# Fliks.xyz

This is a simple Flask app that I built for myself. I needed something minimal and straightforward to search for things.
There is also a What's New section to check the latest releases on Netflix. 
The app runs on Heroku. Checks with multiple API's.
I am caching some information to avoid making multiple API calls, and it also helps to speed up the application.

~~I configured for the UK because it is where I live.
On ```app/functions/whats_new.py``` line 8, you can change the country parameter to your one.~~
~~There are 34 countries, and you can find the country list at the end of this file.
Perhaps I should have added a dropdown for selecting countries. I'll look more into that later.~~

---

**Update 1**
OK. I listened some feedbacks. What's New part is now giving the information based on your IP address. I also added the country list dropdown.

**Update 2**
I added the saving feature on the search bar during the user session. Thanks for the feedback stranger.

**Update 3**
IP feature is completed for across services too. It now works everywhere in the app.

---

## Images

### Search Across Services
![Search across services](https://i.imgur.com/eZSKfRJ.png)

### Netflix Search
![Netflix search](https://i.imgur.com/hsjwgf0.png)

### Checking Available Countries
![Available countries](https://i.imgur.com/hnz60F2.png)

### What's New on Netflix
![New on Netflix](https://i.imgur.com/1G6QNva.png)

The ```app/functions/instance/config.py``` is storing the credentials (it's the only file missing from this repo), for which services I use feel free to drop me a line.
