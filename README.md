<h1>Spotify Time Machine</h1>
<h3>Overview</h3>
<p>This project is from day 46 of Angela Yu's 100 Days of Code on Udemy. The purpose of this project was to cement the use of web scraping and APIs to make a practical application. 
  
<h3>How it works</h3>
<ol>
  <li>The user is prompted to input a date in a specified format of YYYY-MM-DD</li>
  <li>A connection is made to the Spotify API for my user account</li>
  <li>A playlist is created with the input date included in the name</li>
  <li>The Billboard 100 website is scraped for the list of top 100 songs from the date.</li>
  <li>A list of songs is made by finding all song titles from their divs scraped from the website</li>
  <li>The song URIs are found by searching spotify for each of the song names</li>
  <li>The songs are then added to the playlist created earlier</li>
</ol>
