# Flask Journal

![image](https://img.shields.io/badge/license-MIT%20License-green)

## Table of Contents

1. <a href="#description">Description</a>
2. <a href="#installation">Installation</a>
3. <a href="#code">Code Discussion</a>
4. <a href="#contributions">Contributions</a>
5. <a href="#license">License</a>
6. <a href="#questions">Issues and Questions</a>
<hr><h3 id='description'>Description</h3>
This app allows users to log in and keep a journal of writings and moods. Users may view all entries sorted by date, update entries, or delete entries. The app has been designed with HTML/CSS, with vanilla JavaScript and jQuery providing some interactivity. Python/Flask are used for back-end routing functions, with Jinja providing HTML templating. User authentication state is also tracked through Flask. Journal entries are recorded in a SQL database, which is interfaced with using the SQLAlchemy ORM for Python.

![image](https://user-images.githubusercontent.com/64618290/101844700-e81aab00-3b01-11eb-91dd-49f5a1b6fdc1.png)

<h3 id='installation'>Installation</h3>
The app may be run on a local host using the command 'flask run' in a terminal. The app will be accessible in a browser at 'localhost:5000'. This, of course, assumes that Python 3 is installed, and Flask is installed from pip. Sass is used to pre-process CSS files, and may be installed using instructions from the Sass website. Scripts are available in package.json for watching files for updates, but require nodemon and Sass to be installed. Scripts may also have to be edited depending on a particular installation. Nodemon and Sass may be installed locally by using the commands 'npm install nodemon' and 'npm install sass', respectively.

<h3 id='code'>Code Discussion</h3>
A similar journal, also programmed by me, may be found at <a href='https://github.com/Koldenblue/redux-journal'>this repository</a>. This alternative journal was programmed using React/Redux with JavaScript for frontend presentation, MongoDB for database functionality, and Express.js and Node.js for backend functionality. Although the two apps are similar in outcome and functionality, there are major differences in coding languages and performance. React clearly has a large performance advantage over the more traditional routing style of Flask. Upon receiving a routing request, Flask returns an entire Jinja HTML template and reloads the page. On the other hand, since React utilizes a virtual DOM, actions such as viewing all entries on the React site don't require an entirely new HTML page to be loaded. With React, only individual changed components in the DOM are re-rendered. The current Flask app quite noticeably loads pages more slowly. This is despite the fact that the pages between the Flask and React apps are similar. Again, the performance difference is due to the different ways that the Flask app and the React app handle frontend presentation. Flask must handle the re-rendering of an entire HTML template every time a route is traversed. With React handling frontend and Express handling backend routing, page loading times are superior.

<h3 id='contributions'>Contributions</h3>
Contact the author through GitHub or email.

<h3 id='license'>License</h3>
This project is licensed under the MIT License.

<h3 id='questions'>Issues and Questions</h3>
Issues and questions may be emailed to 'kmillergit' at the domain 'outlook.com'. The author's GitHub profile may be found at https://github.com/Koldenblue.<p><sub><sup>This readme was generated with the help of the readme generator program at https://github.com/Koldenblue/readme-generator.</sup></sub></p>