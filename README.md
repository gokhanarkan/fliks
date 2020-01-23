# Fliks.xyz

This is a simple Flask app that I built for myself. I needed something minimal and straightforward to search for things.
There is also a What's New section to check the latest releases on Netflix. 

~~I configured for the UK because it is where I live.
On ```app/functions/whats_new.py``` line 8, you can change the country parameter to your one.~~
~~There are 34 countries, and you can find the country list at the end of this file.
Perhaps I should have added a dropdown for selecting countries. I'll look more into that later.~~

The app runs on Heroku. Checks with multiple API's.
This was the first time I use Redis. I loved it.
I am caching some information to avoid making multiple API calls, and it also helps to speed up the application.

---

**Update 1**
OK. I listened some feedbacks. What's New part is now giving the information based on your IP address. I also added the country list dropdown.

**Update 2**
I added the saving feature on the search bar during the user session. Thanks for the feedback stranger.

---

The ```app/functions/instance/config.py``` is storing the credentials (it's the only file missing from this repo), for which services I use feel free to drop me a line.

---

Supported countries:
```
Countries = {
'Argentina': 'ar',
'Australia': 'au',
'Belgium': 'be',
'Brazil': 'br',
'Canada': 'ca',
'CzechRepublic': 'cz',
'France': 'fr',
'Germany': 'de',
'Greece': 'gr',
'HongKong': 'hk',
'Hungary': 'hu',
'Iceland': 'is',
'India': 'in',
'Israel': 'il',
'Italy': 'it',
'Japan': 'jp',
'Lithuania': 'lt',
'Mexico': 'mx',
'Netherlands': 'nl',
'Poland': 'pl',
'Portugal': 'pt',
'Romania': 'ro',
'Russia': 'ru',
'Singapore': 'sg',
'Slovakia': 'sk',
'SouthAfrica': 'za',
'SouthKorea': 'kr',
'Spain': 'es',
'Sweden': 'se',
'Switzerland': 'ch',
'Thailand': 'th',
'Turkey': 'tr',
'UnitedKingdom': 'gb',
'UnitedStates': 'us'
}

```
