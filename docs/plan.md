# Job Tracker Plan

This is the copy of original plan. Note: As with most projects, some of the elements have changed upon
further research.

Ex: Scraping information from Glassdoor/LinkedIn has been scraped due to limited usage of the APIs (Corporate/Paid API for Glassdoor
and LinkedIn API requires a brand page).

### Tech

Django, Database, Web scraping, React

### Basic Requirements

- Add/remove job points
- Map that displays all jobs as points (click on each point for popup info)
- Job Model
  - Job title (possibly description), Company Logo
  - Apply (platform) and Location
  - Reply (and date)
  - Mark as accepted, denied, no reply (different colored checkpt)
  - Notes for any additional info
- Location Model
  - Coordinates
  - City
  - State

### Additional/Optional:

- Website link
- From the specific company
- Average salary for Software devs (from Glassdoor, LinkedIn etc)
- Salary ask (if mentioned on application)
- Scrape company info from Glassdoor/Google/LinkedIn and display it

#### Notes

- Elements: Map, Map with Info, Job info page (develop a layout for it) -> ability to add/remove this info.
- Each user has a profile associated with them -> and subsequently one map with them (Users, profiles). Maps could be viewed in the “profile” page?
- Start with maps being displayed on the front page (modify it to be the profile page later; so no users/profiles for now).
- Jobs/points (attributes: job title, etc) as a view: Job info page is a full page with all the details (Similar to posts).
- Home page (logged out): Displays map
- Home page (logged in): Map with trackers
- All Jobs page: List of all jobs applied (similar to posts page; only for logged in users)
- Add job page: Formal; only for logged in users
- Register, login, logout pages: UserCreation, Userlogin forms
- Job page: Detailed page for each job applied; only for logged in users, specific users.
  - Filter based on user

## MVP stages:

- Initial setup
- Employer, title, apply date, location, user: DB setup
- Setup authenticated user (login, logout, registration pages)
- Edit or remove job remove functionality for authenticated user (One to many relationship between jobs and user)
- Add all jobs page
- Setup form to add job info on add jobs page
- Display map
- Integrate map with Job information
- grab latitude/longitude information for each job
- Add trackers to map
- Modify style
- Typography and colors as well as layout of the page
- Deploy as a web app (Heroku?)
- Make sure to go through deployment checklist (safety precautions)
- Redo frontend in React
- Deploy React version

### Following has been scraped:

- More attributes to form
- Platform (select from existing entries or add a new one)
- If Link: post link functionality
- Mark status: select no reply, replied, denied
- Add colored borders to map points depending on status
- Notes
- Salary ask (check -> yes/no)
- If the application asked for an expected salary, add that info. Otherwise empty.
- Employer logos
- Upload logos, display on jobs page (for each listing)
- server will use thumbnails as hover icons in map
- Initial scraper script
- scrapes salary for city based entry level software engineers from Glassdoor and LinkedIn
- Integrate script into app (runs when you add a company to a location that doesn’t already exist, fetches data and stores in DB).
- Modify scraper script to fetch logos from Glassdoor
  - Or from a url provided feature (multiple ways to implement; add URL attribute to employer attribute?)
- Modify scraper script to search for salaries within each company (If found for software engineers -> fetch it)
- Integrate modified scraper script into Job tracker

#### OPTIONAL FEATURES:

- Keywords feature
- Provided the JD, an algorithm will pull useful keywords (tech stack; required experience). Simplest solution is to use regex for pattern matching.
- Add a remind feature (reminds you to check up a week after applying)
- Remind as a blinking hover (or as an alert that you can dismiss? Workout later).
- Remind you to apply for jobs everyday
- FF extension that integrates with the app (uses regex to pull relevant information from JD websites)
