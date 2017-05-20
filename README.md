# drafthouse-victory-scraper
Scrapes alamo drafthouse order history and generates a csv

```bash
$ python victory.py --help

usage: victory.py [-h] [--csv CSV] email password

Scrape drafthouse order history

positional arguments:
  email       Victory email address
  password    Victory password

optional arguments:
  -h, --help  show this help message and exit
  --csv CSV   Filename for csv output
```

### Example Output

```bash
$ python victory.py <email> <password>
Fetching login page...  success
Getting csrf token...  success
Logging in...  success
Fetching page 0...  got 200 status code. found 10 items
Fetching page 1...  got 200 status code. found 10 items
Fetching page 2...  got 200 status code. found 10 items
Fetching page 3...  got 200 status code. found 10 items
Fetching page 4...  got 200 status code. found 10 items
Fetching page 5...  got 200 status code. found 10 items
Fetching page 6...  got 200 status code. found 10 items
Fetching page 7...  got 200 status code. found 10 items
Fetching page 8...  got 200 status code. found 10 items
Fetching page 9...  got 200 status code. found 2 items
Fetching page 10...  got 200 status code. found 0 items

Total Visits: 92
Current Visits: 45
Amount rolling off at the end of the month: 3
```

### Generated csv purchase_history.csv
```
date;tickets;location;film;time
Sunday, May 21 2017;2 x Admission;Lakeline;ALIEN: COVENANT;11:45 AM
Wednesday, May 17 2017;2 x Admission;Village;2D GUARDIANS OF THE GALAXY VOL. 2;8:00 PM
Monday, May 15 2017;2 x Admission;Lakeline;2D GUARDIANS OF THE GALAXY VOL. 2;7:25 PM
Friday, Apr 28 2017;2 x Admission Single w/;Ritz;Master Pancake: TITANIC;7:00 PM
Saturday, Apr 22 2017;2 x Admission;Village;FREE FIRE;7:30 PM
Tuesday, Apr 18 2017;6 x Admission;South Lamar;YOUR NAME. (Subtitled);6:40 PM
Friday, Apr 07 2017;2 x Admission;Lakeline;POWER RANGERS;7:00 PM
Wednesday, Mar 15 2017;2 x Admission;Lakeline;2D KONG: SKULL ISLAND;7:00 PM
Thursday, Apr 13 2017;4 x Admission;Village;THE FATE OF THE FURIOUS;7:00 PM
Sunday, Mar 05 2017;4 x Admission;Mason Park;LOGAN;12:00 PM
...
```