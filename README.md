# Food Waste Rescue Marketplace and Demand Forecaster

## Description

Our motivation for building this project was to help mitigate the the 10.7 million tonnes of food wasted annually in the UK. We built this project to benefit both sellers and consumers by providing a marketplace in which excess food can be posted to help businesses reduce waste and allow consumers to reserve this food for a cheap price. Through this project we learnt how to create an interactive frontend and how to intergrate it with responsive backend. We also learnt how data moves through these layers and how the database it interacted with.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Credits](#credits)
- [Tests](#tests)

## Installation

To run the program you will need to have install Docker.

 - Open docker desktop and ensure the Docker engine is running.
 - In your terminal navigate to the root folder and run docker compose up --build
 - This starts up the frontend, backend and database and installs any neccessary dependencies.
 - You may get an error saying that start.sh is not executable. If this is the case run chmod +x backend/start.sh && ls -l backend/start.sh and try again.
 - Once the logs say the application is running open http://127.0.0.1:5173 on your web browser for the web app.
 - To access the API swagger documentation open http://127.0.0.1:8000/docs

## Usage

To navigate the project you will have to login as either a seller or consumer. As this is a prototype we have hardcoded these two for ease of use.

 - For the consumer log in with the credentials: harryConsumer, Lewis
 - For the seller log in with the credentials: harrySeller, Lewis

To add a screenshot, create an `assets/images` folder in your repository and upload your screenshot to it. Then, using the relative filepath, add it to your README using the following syntax:

    ```md
    ![alt text](assets/images/screenshot.png)
    ```

## Tech Stack

| Category | Tools |
| :--- | :--- |
| Frontend | React |
| Backend | Python, FastAPI, PostgreSQL |
| DevOps | Docker |

## Features and Roadmap

## Credits

Collaborators

 - Finley New https://github.com/FinleyNew
 - Harry Lewis https://github.com/harrylewis200
 - James Hickson https://github.com/JamesHickson
 - Tom Lambe https://github.com/TomLambe23
 - Cody Miller https://github.com/CMiller838
 - Jacob Shrive https://github.com/Jegs201
 - George Shrive https://github.com/George4tee

## Tests

Go the extra mile and write tests for your application. Then provide examples on how to run them here.
Must have pytest 9.0.2 installed.

To run all tests, use command python -m pytest .\backend\testing\ in the terminal

To run specific test files add the file on the end of the command eg python -m pytest .\backend\testing\test_Reservation.

All prototype tests used unittest.mock to mimic a database to fully test the backend code without using the real database


**test_Reservation.py**

test_collection_with_valid_code_success()

tests the collection feature using a valid code - Pass indicates the collection can be made with a correct code

test_collection_with_invalid_code()

tests the collection feature using a invalid code - Pass indicates the collection cannot be made with a correct code

test_no_show_count()

test the amount of no shows is correctly calculated - Pass indicates the count of no shows is correct

**test_Streak**

test_streak_reset_after_7_days()

tests the streak successfully resets after 7 days - Pass indicates the streak successfully resets after the specified time 

test_streak_persists_when_active()

tests the streak reamins when a reservation has been made in the last 7 days - Pass indicates the streak will  not reset if a reservation is made within 7 days

test_no_reservations()

trests that a newly created user with no streak or reservation has a streak of 0 - Pass indicates new users with no reservations have the correct starting streak

## License

MIT License




