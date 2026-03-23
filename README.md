# Food Waste Rescue Marketplace and Demand Forecaster

## Description

Our motivation for building this project was to help mitigate the the 10.7 million tonnes of food wasted annually in the UK. We built this project to benefit both sellers and consumers by providing a marketplace in which excess food can be posted to help businesses reduce waste and allow consumers to reserve this food for a cheap price. Through this project we learnt how to create an interactive frontend and how to intergrate it with responsive backend. We also learnt how data moves through these layers and how the database it interacted with.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Tech Stack](#tech-stack)
- [Credits](#credits)
- [Tests](#tests)
- [Licence](#licence)

## Installation

To run the program you will need to have install Docker.

 - Open docker desktop and ensure the Docker engine is running.
 - In your terminal navigate to the root folder and run docker compose up --build
 - This starts up the frontend, backend and database and installs any necessary dependencies.
 - You may get an error saying that start.sh is not executable. If this is the case run chmod +x backend/start.sh && ls -l backend/start.sh and try again.
 - Once the logs say the application is running open http://127.0.0.1:5173 on your web browser for the web app.
 - To access the API swagger documentation open http://127.0.0.1:8000/docs
 - To shut the program down press ctrl + c to exit the logs and run docker compose down in the terminal to remove the container.

## Usage

To navigate the project you will have to login as either a seller or consumer. As this is a prototype we have hardcoded these two for ease of use.

 - For the consumer log in with the credentials: consumer, 1
 - For the seller log in with the credentials: seller, 1

![Homepage Screenshot](images/consumerNavigation.png)

Consumer Pages Guide 

 Looking at all Bundles - Use the navigation buttons at the top of the screen to get to the "Discover" page. All the bundles and their information are displayed there.

 Purchasing and reserving a bundle - When on the discover page, click on a bundle to be taken to another page with only the selected bundles' information on it. From there click the pay button and then "confirm" to successfully reserve a bundle.

 Finding a consumers' current reservations - Use the navigation buttons at the top to navigate to the "Codes" page, there is all the current users reservations, and the code to collect the bundle with.

 Finding your current streak - Use the navigation buttons at the top of the screen to naviate to the "Streaks" page, there is a users current streak and the badges they have collected.

![Homepage Screenshot](images/sellersNavigation.png)

Sellers Pages Guide

 Looking at the sellers current bundles - Use the navigation buttons to get to the "current-bundles" page, from there, all the bundles that have been created by the current seller are displayed.

 Confirming a bundle has been collected - Enter the bundle code, from the consumers codes page, and press confirm to ensure a bundle has been successfully collected. 

 Creating a new bundle - Head to the "add_bundle" page via the navigation buttons, then enter the correct information, with a positive price, weight and number of bundles available. Then click the "Add Bundle" button, the new bundle should appear in the "current-bundles" page if the data entered is valid.

 Forecasting a new bundle - Head to the "add_bundle" page via the navigation buttons, then enter the correct information, with a positive price, weight and number of bundles available. Then click the "Forecast" button near the bottom to get an prediction on the number of reservations and the chance of a no-show based off the information entered.

 Viewing a sellers' analytics - Head to the "analytics" page with the navigation buttons, on this page all of the collected bundles are shown with lots of information. Such as number of reservations, no-shows and expiries. There is also a bar chart to visualise this information. 

 Viewing all previous forecasts - Head to the "forecasts" page with the navigation buttons. On this page all previous forecasts made will appear, allowing a seller to compare predictions with actaul results.






## Tech-Stack

| Category | Tools |
| :--- | :--- |
| Frontend | React |
| Backend | Python, FastAPI, PostgreSQL |
| DevOps | Docker |

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

### Prerequisites

* Python ≥ 3.12 and **pytest 9.0.2** installed (listed in `backend/requirements.txt`).

### Running Tests

```bash
# Run the full suite (105 tests)
python -m pytest .\backend\testing\ -v

# Run a single file
python -m pytest .\backend\testing\test_services\test_login.py -v

# Run a single test by name
python -m pytest .\backend\testing\ -k "test_check_streak_valid_this_week" -v
```

All tests use `unittest.mock` to replace the database session and CRUD layer, so no running database is needed.

---

### Test Files (105 tests total)

#### test_collections.py (6 tests)
Tests reservation creation (stock checks) and claim-code collection (valid code, invalid code, already-collected, no-show).
- `test_create_reservation_checks_availability_and_reserves`
- `test_create_reservation_rejects_zero_stock`
- `test_collect_already_collected_raises_400`
- `test_collect_no_show_raises_400`
- `test_collect_valid_reservation_succeeds`
- `test_collect_invalid_code_raises_404`

#### test_login.py (12 tests)
Tests password hashing, JWT token generation, SQL injection safety, and password changes.
- `test_hash_password_is_not_plaintext`
- `test_hash_password_is_bcrypt_format`
- `test_verify_password_correct`
- `test_verify_password_wrong`
- `test_same_password_hashes_differently`
- `test_jwt_token_contains_exp_claim`
- `test_jwt_token_contains_sub_claim`
- `test_jwt_token_expires_in_expected_window`
- `test_jwt_token_subject_matches`
- `test_query_uses_parameterized_statements`
- `test_update_user_hashes_password`
- `test_update_user_no_password_no_hash`

#### test_accout_creation.py (11 tests)
Tests seller and consumer registration, duplicate email rejection, display name validation, opening hours logic, and input whitespace trimming.
- `test_consumer_creation_does_not_need_location`
- `test_seller_needs_location_and_coordinates`
- `test_prevent_duplicate_emails`
- `test_consumer_duplicate_email_rejected`
- `test_consumer_empty_display_name_rejected`
- `test_consumer_display_name_too_long_rejected`
- `test_seller_opening_after_closing_rejected`
- `test_seller_valid_hours_accepted`
- `test_seller_invalid_hours_format_rejected`
- `test_email_whitespace_trimmed_on_user_create`
- `test_seller_name_whitespace_trimmed`

#### test_gamification.py (41 tests)
Tests weekly streak increment/reset logic and all sixteen badge unlock conditions (Good Start, First Rescue, On a Roll, Locked In, Relentless, Waste Warrior, Eco Advocate, Green Guardian, Punctual, Timekeeper, Unshakeable, Final Call, Weatherproof, Triple Threat, Familiar Face, Well Rounded), plus duplicate-badge prevention.
- `test_check_streak_valid_this_week`
- `test_check_streak_valid_last_week`
- `test_increment_streak_when_zero`
- `test_increment_streak_when_positive_and_last_week`
- `test_increment_streak_skips_if_same_week`
- `test_check_streak_resets_if_old`
- `test_check_streak_raises_if_no_reservations`
- `test_check_good_start_awards_badge`
- `test_check_good_start_no_reservations`
- `test_check_first_rescue_awards_badge`
- `test_check_first_rescue_no_collections`
- `test_check_on_a_roll_3_consecutive_days`
- `test_check_on_a_roll_not_consecutive`
- `test_check_on_a_roll_too_few`
- `test_check_locked_in_7_consecutive_days`
- `test_check_locked_in_too_few`
- `test_check_triple_threat_same_day`
- `test_check_triple_threat_different_days`
- `test_check_waste_warrior_over_1kg`
- `test_check_waste_warrior_under_1kg`
- `test_check_punctual_10_collected`
- `test_check_punctual_not_all_collected`
- `test_check_familiar_face_awards_badge`
- `test_check_familiar_face_not_enough`
- `test_check_well_rounded_awards_badge`
- `test_check_well_rounded_not_all_categories`
- `test_award_badge_skips_if_already_awarded`
- `test_award_badge_inserts_if_not_awarded`
- `test_award_badge_skips_if_badge_not_found`
- `test_check_relentless_awards_on_30_day_streak`
- `test_check_relentless_skips_when_fewer_than_30`
- `test_check_eco_advocate_awards_over_10kg`
- `test_check_eco_advocate_skips_under_10kg`
- `test_check_green_guardian_awards_over_25kg`
- `test_check_green_guardian_skips_under_25kg`
- `test_check_timekeeper_awards_on_25_collected`
- `test_check_timekeeper_skips_fewer_than_25`
- `test_check_unshakeable_awards_on_50_collected`
- `test_check_unshakeable_fails_with_no_show`
- `test_check_final_call_awards_within_5_minutes`
- `test_check_final_call_skips_when_not_close`
- `test_check_weatherproof_awards_on_5_rainy`
- `test_check_weatherproof_skips_under_5_rainy`

#### test_seller_dashboard.py (11 tests)
Tests bundle creation and update validation (price, time-window), ownership authorisation, cascade deletion of child rows, and pickup-window range generation.
- `test_bundle_negative_price_rejected`
- `test_bundle_zero_price_rejected`
- `test_bundle_end_before_start_rejected`
- `test_update_bundle_wrong_owner_raises_403`
- `test_update_bundle_correct_owner_succeeds`
- `test_delete_bundle_clears_reservations`
- `test_delete_bundle_with_no_reservations`
- `test_create_bundle_generates_pickup_range`
- `test_time_window_validation_end_before_start`
- `test_time_window_equal_start_end_rejected`
- `test_time_window_valid_update_passes`

#### test_forecasting.py (8 tests)
Tests forecast schema validation (non-negative reservations, probability bounds), create_forecast orchestration, and the ML pipeline's normalisation logic (clamping, divide-by-zero guard).
- `test_forecast_create_valid`
- `test_forecast_create_negative_reservations_rejected`
- `test_forecast_create_no_show_over_1_rejected`
- `test_forecast_create_no_show_negative_rejected`
- `test_forecast_create_zero_reservations_accepted`
- `test_create_forecast_stores_prediction`
- `test_get_forecast_returns_normalised_prediction`
- `test_get_forecast_zero_predicted_reservations_yields_zero_no_show`

#### test_issue_reports.py (4 tests)
Tests issue-report ownership enforcement: seller response (with 403 for wrong owner) and consumer resolution (with 403 for wrong owner). Regression-tests the fixed missing-`raise` bugs.
- `test_respond_to_issue_report_success`
- `test_respond_to_issue_report_wrong_seller_raises_403`
- `test_set_issue_report_resolved_success`
- `test_set_issue_report_resolved_wrong_consumer_raises_403`

#### test_records.py (10 tests)
Tests record schema validation (end > start, positive weight, non-negative counts), the partial-update validator (fires only when both times present), service-layer time-window merging, and coordinate extraction.
- `test_record_create_valid`
- `test_record_create_end_before_start_raises`
- `test_record_create_zero_weight_rejected`
- `test_record_create_negative_reservations_rejected`
- `test_admin_update_both_times_valid`
- `test_admin_update_both_times_invalid_raises`
- `test_admin_update_only_start_time_skips_validation`
- `test_update_record_valid_times`
- `test_update_record_end_before_start_raises_400`
- `test_create_record_passes_seller_coordinates`

## Licence

This project is licensed under the MIT License - see the [LICENCE](LICENCE) file for details.




