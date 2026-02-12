# **WEATHER APP**

### Description

The weather app is a simple web application for getting the hourly temperature for seven days in up to four locations. It is not user specific and saves the four locations to the database. When there are already four locations and a new location is added the oldest location will be removed. 

---

### Layout

The weather app is a single page web application. From top to bottom the sections are:  

<ol>
    <li>The locations that have already been selected and stored in the database are at the top of the page. The name and high and low for the current day are listed.</li>
    <li>The next section contains a form for adding a new location.</li>
    <li>The final section is where the full forecasts are displayed for the selected locations</li> 
</ol>

---

### Use

There are only two things the user can do:

<ol>
    <li>They can add a new location by City, State using the "Add" button in the "Final A Location" section.</li>
    <li>They can delete a location using the "Delete" button in the locations section at the top of the page.</li>
</ol>

---

### Technologies Used

<ul>
    <li>Python</li>
    <li>Django</li>
    <li>HTML/CSS</li>
    <li>Ubuntu</li>
    <li>Docker</li>
    <li>Bash</li>
    <li>Nginx</li>
    <li>PostgreSQL</li>
</ul>

---

### Build

The application is built using Docker on Ubuntu. Nginx is on the host server while the database and python code are containerized. All of the complexities of building and running the app are abstracted away in [run_dev.sh](./run_dev.sh) for development and [run_prod.sh](./run_prod.sh) for production. run_prod.sh does the following:

- Pulls the latest version from GitHub
- Manipulates files and permissions as necessary to enable persistent storage.
- Builds the containers and deploys using `docker compose up --build -d`

---

### API Sources

- [Zippopotam](https://api.zippopotam.us): Searches and geocodes using City, ST.
- [Open-Meto](https://open-meteo.com): Gets the seven day forecast based on the latitude and longitude.

---

### Links

- [Production App](https://weather.programmingondemand.com)
- [GitHub Code](https://github.com/packardjc2024/weather)
- [Portfolio](https://www.programmingondemand.com)


