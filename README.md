# ESPN Cricinfo stats scraper
Scrape stats of a particular player from ESPN Cricinfo and store them in an CSV file


## Steps

* To get the stats go to player profile url and copy the id, Example: 

  ` https://www.espncricinfo.com/india/content/player/398438.html`
  
   In the following url `398438` is the player id



1.
    ```bash
    git clone https://github.com/sandyjswl/cricinfo-stats-scraper.git
    ```
    
    
2. ```bash
    cd cricinfo-stats-scraper
    ```
2. ```bash
    pip install -r requirements.txt
    ```
3. ```bash 
    python batting_history.py
    ```
4.  ```bash 
    python batting_summary.py
    ```
    
* To get the entire history for a particular format use command 4
* To get the carrer summary use command 5
