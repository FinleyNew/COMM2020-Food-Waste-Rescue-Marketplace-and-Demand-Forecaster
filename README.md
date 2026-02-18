# Food Waste Rescue Marketplace and Demand Forecaster

## Description

Our motivation for building this project was to help mitigate the the 10.7 million tonnes of food wasted annually in the UK. We built this project to benefit both sellers and consumers by providing a marketplace in which excess food can be posted to help businesses reduce waste and allow consumers to reserve this food for a cheap price. Through this project we learnt how to create an interactive frontend and how to intergrate it with responsive backend. We also learnt how data moves through these layers and how the database it interacted with.

## Table of Contents (Optional)

- [Installation](#installation)
- [Usage](#usage)
- [Credits](#credits)
- [Tests](#tests)

## Installation

To run the program you will need to have install Docker.

 - Open docker desktop and ensure the Docker engine is running.
 - In your terminal run docker compose up --build.
 - This starts up the frontend, backend and database and installs any neccessary dependencies.
 - Once the logs say the application is running navigate to 127.0.0.1:5173.

## Usage

To navigate the project you will have to login as either a seller or consumer. As this is a prototype we have hardcoded these two for ease of use.

 - For the consumer log in with the credentials: consumer, 1
 - For the seller log in with the credentials: seller, 1

Consumer Pages Guide 

 Looking at all Bundles - Use the navigation buttons at the top of the screen to get to the "Discover" page. All the bundles and their information are displayed there.

 Purchasing and reserving a bundle - When on the discover page, click on a bundle to be taken to another page with only the selected bundles' information on it. From there click the pay button and then "confirm" to successfully reserve a bundle.

 Finding a consumers' current reservations - Use the navigation buttons at the top to navigate to the "Codes" page, there is all the current users reservations, and the code to collect the bundle with.

 Finding your current streak - Use the navigation buttons at the top of the screen to naviate to the "Streaks" page, there is a users current streak and the badges they have collected.


Sellers Pages Guide

 Looking at the sellers current bundles - Use the navigation buttons to get to the "current-bundles" page, from there, all the bundles that have been created by the current seller are displayed.

 Confirming a bundle has been collected - Enter the bundle code, from the consumers codes page, and press confirm to ensure a bundle has been successfully collected. 

 Creating a new bundle - Head to the "add_bundle" page via the navigation buttons, then enter the correct information, with a positive price, weight and number of bundles available. Then click the "Add Bundle" button, the new bundle should appear in the "current-bundles" page if the data entered is valid.

 Forecasting a new bundle - Head to the "add_bundle" page via the navigation buttons, then enter the correct information, with a positive price, weight and number of bundles available. Then click the "Forecast" button near the bottom to get an prediction on the number of reservations and the chance of a no-show based off the information entered.

 Viewing a sellers' analytics - Head to the "analytics" page with the navigation buttons, on this page all of the collected bundles are shown with lots of information. Such as number of reservations, no-shows and expiries. There is also a bar chart to visualise this information. 

 Viewing all previous forecasts - Head to the "forecasts" page with the navigation buttons. On this page all previous forecasts made will appear, allowing a seller to compare predictions with actaul results.




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
To run specific test files add the file on the end of the command eg python -m pytest .\backend\testing\test_Reservation.py
