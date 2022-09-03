
# Trivia App Project Documentation

### Project description
This is a Trivia App is a trivia game that was made to create a bonding experience between people be it in the workplace, family setting or amongst friends. In the game, players can choose to play by category where they can choose a particular category for their questions, or they can play a randomised set of questions where there will be questions from each category.  <br/>
#### Code Style
All backend code follows PEP8 style guidelines. <br/>

### Getting Started
To get started you will need to have this code on your local computer. Here are some steps to get you started.  

#### Prerequisites & Installation
To have the code on your computer, start by forking this repository and then cloning it onto your computer. <br/>
Once you have it downloaded, open it on a IDE of your choice e.g. Visual Studio Code.


Pre-requisites and Local Development
Developers using this project should already have Python3, pip and node installed on their local machines.


***Backend***  <br/>
From the terminal, make sure you are in the project direct and cd into the backend folder. <br/>

From the backend folder run we can start to install the dependecies that are needed to run the server.Tools you will need:  <br/>


- virtualenv as a tool to create isolated Python environments
- SQLAlchemy ORM to be our ORM library of choice
- PostgreSQL as our database of choice <br/>

Start your virtual environment From the backend folder run

##### Mac users
```
python3 -m venv venv
source venv/bin/activate
```
##### Windows users
```
 py -3 -m venv venv
 venv\Scripts\activate 
```

Next, you will  download and install the dependencies the other required packages which are included in the requirements file.:  <br/>
```
pip install requirements.txt. 
```

To run the application run the following commands:
```
export FLASK_APP=flaskr
export FLASK_DEBUG=true
flask run
```
***Start/Stop the PostgreSQL server*** <br/>
Mac users can follow the commands below: <br/>
```
which postgres
postgres --version
```
##### Start/stop
pg_ctl -D /usr/local/var/postgres start <br/>
pg_ctl -D /usr/local/var/postgres stop <br/>
Windows users can follow the commands below:<br/>

Find the database directory, it should be something like that: C:\Program Files\PostgreSQL\13.2\data <br/>
Then, in the command line, execute the folllowing command: <br/>
##### Start the server
```
pg_ctl -D "C:\Program Files\PostgreSQL\13.2\data" start 

```
##### Stop the server
```
pg_ctl -D "C:\Program Files\PostgreSQL\13.2\data" stop 
```
If it shows that the port already occupied error, run: <br/>
````
sudo su - 
ps -ef | grep postmaster | awk '{print $2}'
kill <PID> 

````
***Create and Populate the database*** <br/>


Create the database and a user
In your terminal, navigate to the project directory and run the following:

##### Connect to the PostgreSQL
psql postgres
#View all databases
\l
##### Create the database, create a user - `postgres`, grant all privileges to the postgres
\i setup.sql
##### Exit the PostgreSQL prompt
\q
Create tables
Once your database is created, you can create tables (questions,categories) and apply contraints <br/>
##### Mac users
```
psql -f trivia.psql -U student -d trivia
```
##### Linux users
```
su - postgres bash -c "psql trivia < /path/to/project/backend/trivia.psql"
```
You can even drop the database and repopulate it, if needed, using the commands above.



***Frontend*** <br/>
Now, change directories and cd into the frontend folder and run: <br/>
```
npm install  #run this only once!

```
and then this to start the server: <br/>
```
npm start

```
You should now see a browser window with app's UI. By default, the frontend will run on localhost:3000. <br/>

### API Reference

##### Getting Started
Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.

##### Authentication
This version of the application does not require authentication or API keys.

##### Error Handling
Errors are returned as JSON objects in the following format:

```json
  {
      "success": False, 
      "error": 400,
      "message": "bad request"
  }
```
The API will return these types when requests fails: <br/>
400: Bad Request  
404: Resource Not Found  
422: Not Processable  
405: Method Not Allowed  <br/>
##### Usage
API endpoints can be invoked using cURL <br/>
***Example of using cURL for GET request***: <br/>
```
curl http://127.0.0.1:5000/categories
```

##### Endpoints
`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs. <br/>
***Sample Output*** <br/>
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
    "success": true
}
```

---

`GET '/questions?page=${integer}'`  <br/>
***Example***: <br/>
```curl http://127.0.0.1:5000/questions?page=1
```


- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: `page` - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string  <br/>

***Sample Output*** <br/>
```json
  {"categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "Art",
  "questions": [
    {
      "answer": "This is an answer",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "This is a question"
    },
        {
      "answer": "This is an answer",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "This is a question"
    },

  
  ],
  "success": true,
  "total_questions": 30
}


```

---

`GET '/categories/${id}/questions'` <br/>
***Example***: <br/>
````
 curl http://127.0.0.1:5000/categories/4/questions
 ````


- Fetches questions for a cateogry specified by id request argument
- Request Arguments: `id` - integer
- Returns: An object with questions for the specified category, total questions, and current category string

***Sample Output***
```json
{
  "current_category": "History",
  "questions": [
    {
      "answer": "This is an answer",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "This is a question"
    },
    {
      "answer": "This is an answer",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "This is a question"
    }
  ],
  "total_questions": 2
}

```

---

`DELETE '/questions/${id}'`
***Example***: <br/>
```
curl http://127.0.0.1:5000/questions/17 -X DELETE
```


- Deletes a specified question using the id of the question
- Request Arguments: `id` - integer
- Returns:  id of the question that has been deleted anf total number of questions that are remaining in the question bank.
```json
{
  "deleted": 14,
  "success": true,
  "total_questions": 28
}

```

---

`POST '/quizzes'`

- Sends a post request in order to get the next question
- Request Body:

```json
{
    'previous_questions': [1, 4, 20, 15]
    quiz_category': 'current category'
 }
```

- Returns: a single new question object   <br/>

***Sample Output** <br/>
```json
{
  "question": {
    "id": 1,
    "question": "This is a question",
    "answer": "This is an answer",
    "difficulty": 5,
    "category": 4
  },
  "success": true
}
```

---

`POST '/questions'`  <br/>
***Example***:  <br/>
 ```
 curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"This is a question","answer":"This is an answer","category":"1","difficulty":"4"}'

 ````

- Sends a post request in order to add a new question
- In the request body you specify the question, the answer, the difficulty a number between 1-4(inclusive) where one is least difficult and 4 being very difficult.
- Request Body:

```json
{
  "question": "Heres a new question string",
  "answer": "Heres a new answer string",
  "difficulty": 1,
  "category": 3
}
```

- Returns: an object with the id of the question that has just been created and the total number of questions in the question bank <br/>
***Sample Output***
```json
{
  "created": 60,
  "success": true,
  "total_questions": 30
}


```

---

`POST '/questions/search'`  <br/>
***Example***:
```
curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"SearchTerm":"This is a search term for the question you are looking for"}'
```

- Sends a post request in order to search for a specific question by search term
- Request Body:

```json
{
  "searchTerm": "this is the term the user is looking for"
}
```

- Returns: any array of questions, a number of total_questions that met the search term and the current category string<br/>
***Sample Output*** <br/>
```json
  {"current_category": "Art",
  "questions": [
    {
      "answer": "This is an answer",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "This is a question"
    }
  ],
  "success": true,
  "total_questions": 1
}

```


### Deployment 
N/A <br/>

### Authors
Dumisile Mbuthuma and Udacity Team

### Acknowledgements
I'd like the Udacity team and all my fellow students who helped me through this project.






