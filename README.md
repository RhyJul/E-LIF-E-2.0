# ✔️ E-life(e) – Habit Tracker

This project is intended to:

- Practice the complete process from **problem analysis to implementation**
- Apply basic **Python** programming concepts learned in the Programming Foundations module
- Demonstrate the use of **console interaction, data validation, and file processing**
- Produce clean, well-structured, and documented code
- Prepare students for **teamwork and documentation** in later modules
- Use this repository as a starting point by importing it into your own GitHub account.  
- Work only within your own copy — do not push to the original template.  
- Commit regularly to track your progress.

# ✔️ TEMPLATE for documentation
## 📝 Analysis

**Problem**
💡 In a busy lifestyle, individuals often lack a simple, consolidated way to track and assess their daily wellness habits (e.g., sleep, stress, water, exercise). This lack of immediate feedback makes it difficult to maintain awareness, identify patterns, and make necessary adjustments to achieve their health and habit goals. 

**Scenario**
💡 The E-lif(e) Tracker is designed for quick, end-of-day use. The user runs the application from the console, is prompted with quick questions about their day’s habits, and, upon completion, automatically generates a clear status report with a personalized wellness score and actionable advice. This provides an immediate, clear overview without complex setup or extensive data entry. 1 User will log her/his daily data’s into the program. 

**User stories:**
1. As a User, I want to track my daily habits by answering simple, quick questions in order to stay strong and healthy. 
2. As a User, I want to quickly add information about my lifestyle (nutrition, sport, sleep) in order to get decisive and valuable information for improvement. 
3. As a User, I want to receive a daily status report that gives personalized advice based on my input in order to keep me motivated. 
4. As a User, I want the history of my daily reports to be saved so I can view my progress over time in order to track my improvement and development. 

**Use cases:**
1. Enter daily wellness data (sleep, stress, exercise, etc.) 
2. Validate each entry to prevent invalid input
3. Save all inputs to a file (e.g., ‘weekly_data.txt’). Saving inputs for 28 days 
4. Generate a weekly status report (‘report.txt’) with advice and summaries 

---

## ✅ Project Requirements

Each app must meet the following three criteria in order to be accepted (see also the official project guidelines PDF on Moodle):

1. Interactive app (console input)
2. Data validation (input checking)
3. File processing (read/write)

---

### 1. Interactive App (Console Input)

---
The application interacts with the user via the console. Users can:
- View all the habits 
- Select habit and answer the question 
- See the results of each habit - Receive a daily/weekly overview of the habits

---


### 2. Data Validation 

To ensure the application collects accurate and meaningful information, every user input is validated before it is stored or used for calculations. The program uses predefined categories, data types, and validation rules to prevent invalid values and keep the dataset consistent.

All validation is implemented directly in main.py, mainly through the helper functions ask_choice() and ask_number(). These functions repeatedly prompt the user until valid input is provided.

**Sleep quality validation:**
```python
Category: Sleep rating
Data type: String (input) → mapped to Integer (stored)
Validation rule: Must be one of: good, medium, bad
Storage: sleep is saved as a numeric score using SLEEP_MAP


	def ask_choice(prompt, mapping):
    while True:
        value = input(prompt).lower().strip()
        if value in mapping:
            return mapping[value]
        print("Invalid input.")

Example usage:

	day["sleep"] = ask_choice("Sleep (good/medium/bad): ", SLEEP_MAP)
```

**Stress level validation:**

```python
When the user enters their daily stress level, the program ensures that the input is a number between 1 and 5:
Category: Daily stress measurement (1–5)
Data type: Integer
Validation rule: Must be an integer between 1 and 5

	
	def ask_number(prompt, min_val=None, max_val=None, is_float=False):
    while True:
        try:
            value = float(input(prompt)) if is_float else int(input(prompt))
            if (min_val is None or value >= min_val) and \
               (max_val is None or value <= max_val):
                return value
        except:
            pass
        print("Invalid input.")

Example usage:

	day["stress"] = ask_number("Stress (1-5): ", 1, 5)
```

- **Yes/No questions (friends, exercise, hobbies, medication):** 

```python
For binary inputs, the program checks if the user enters only yes or no:
Category: Social & health habits (friends, exercise, hobbies, meds)
Data type: String (input) → mapped to Integer (stored)
Validation rule: Must be yes or no
Storage: Stored as numeric values using YES_NO_MAP

day["exercise"] = ask_choice("Exercise? (yes/no): ", YES_NO_MAP)
day["friends"] = ask_choice("Hung out with friends? (yes/no): ", YES_NO_MAP)
```

- **Water intake validation:** 

```python
Water intake is checked to confirm that the input is numeric and within realistic limits:
Category: Daily water consumption (liters)
Data type: Float (input) → categorized to Integer (stored)
Validation rule: Must be a non-negative number
Storage rule: liters are categorized into 3 levels

	def classify_water():
    w = ask_number("Water (liters): ", 0, None, True)
    return 1 if w < 1 else 2 if w <= 1.5 else 3
```

- **Step count validation:**

```python
The number of steps is verified to be a positive integer:
Category: Physical activity measurement
Data type: Integer (input) → categorized to Integer (stored)
Validation rule: Must be a non-negative integer
Storage rule: categorized into 3 levels

	def classify_steps():
    s = ask_number("Steps: ", 0)
    return 1 if s < 4000 else 2 if s < 10000 else 3
```

**Date Validation (Optional Change):**

```python
After input collection, users can manually overwrite the automatically generated date. The entered date must match the format YYYY/MM/DD.

	new = input("Enter date (yyyy/mm/dd): ").strip()
	datetime.datetime.strptime(new, "%Y/%m/%d")
```

These validation checks ensure that:

- the program does not crash due to invalid input,
- stored data remains consistent across days,
- summaries and score calculations remain reliable.


### 3. File Processing 

The application uses JSON files for persistent storage and reporting.

- **Input file/ Storage File:** 

File name: girlypop_data.json
Purpose: Stores all logged days
Format: A list of dictionaries (one dictionary per day)

Each entry contains standardized numeric values for all tracked metrics plus the computed total score.

Example structure:

	```json
				[
  {
    "date": "2025/12/13",
    "sleep": 3,
    "stress": 2,
    "friends": 2,
    "water": 2,
    "exercise": 1,
    "mood": 3,
    "work_hours": 8.0,
    "hobbies": 2,
    "steps": 2,
    "meds": 2,
    "score": 22
  }
]
```
- The application reads this file to generate a weekly or monthly summary and give personalized advice.
- Loading and saving: the file (example implementation):

	```python
	def load_data():
    return json.load(open(DATA_FILE)) if os.path.exists(DATA_FILE) else []

	def save_data(data):
    json.dump(data, open(DATA_FILE, "w"), indent=4)


- **Output file(Monthly/Weekly Reports):** 
When the user selects “Generate monthly report”, the program creates two files:

1. JSON report file
Filename format: monthly_report_YYYY_MM.json
Contains: month/year, days logged, total score, average score, and averages per metric.

2. TXT report file
Filename format: monthly_report_YYYY_MM.txt
Human-readable summary including the same key statistics.

Writing output:

	```python
		json_name = f"monthly_report_{today.year}_{today.month:02d}.json"
		json.dump(report, open(json_name, "w"), indent=4)

		txt_name = f"monthly_report_{today.year}_{today.month:02d}.txt"
		with open(txt_name, "w") as f:
		```


## ⚙️ Implementation

### Technology
- Python 3.x
- Environment: GitHub Codespaces
- OpenAI
- No external libraries

### 📂 Repository Structure
	```text
	e_life_project/
├─ data_storage.py      # handles loading and saving data from/to json files
├─ input_validation.py  # handles user input and validates it
├─ main.py              # main entry point (this file)
├─ menu.py              # in order to select the menu before starting the questionary and report
├─ reports.py           # report generation module, generates weekly and monthy reports with analyses and advice
├─ weekly_data.txt      # weekly data entry in numbers
└─ wellness_score.py    # calculation module for the scoring system
```

### How to Run
1. Open the repository in **GitHub Codespaces**
2. Open the **Terminal**
3. Run:
	```bash
	python3 main.py
	```

### Libraries Used

- `os`: Check if files exist and handle paths.
- `datetime` → Add timestamps or weekly summaries.
- `json`: Used for data storage

### Project Modules
- `from menu import`: main_menu

All external dependencies used in this project come from Python’s standard library, so no additional installation is required. In addition, the project uses custom modules created within the codebase (e.g. for menu handling) to improve structure and readability. These components were chosen for their simplicity and effectiveness in managing data, files, and user interaction in a console application.

## Project Management

| Name       	   | Contribution (Before Project started)        |Contribution after Projectstart                          |
|------------------|----------------------------------------------|---------------------------------------------------------|
| da Costa Inês    | Menu reading (file input) and displaying menu|1.) Created input_validation.py                          |
|                  |                                              |2.) Read.me (exception project management)               |
|                  |                                              |3.) PPT -> Live demo                                     |
|                  |                                              |                                                         |
| Haefliger Sarah  | Order logic and data validation              |1.) created menu.py and data storage.py                  |
|                  |                                              |2.) putting all codes to main.py and testing             |
|                  |                                              |3.) Read.me -> Project Management & Limitations          |
|                  |                                              |4.) PPT -> Project management                            |
|                  |                                              |                                                         |
| Jegge Lara 	   | Invoice generation (file output) and slides  |1.) created reports.py and wellness_score.py             |
|                  |                                              |2.) PPT -> a.Rationale for the topic chosen              |
|                  |                                              |           b.Project for the topic chosen                |
----------------------------------------------------------------------------------------------------------------------------------------------------------

**Highlight: Data Validation & Storage Design**

One major highlight of our project was the structured validation and storage of user input.
Initially, user inputs were entered as strings (e.g. good, medium, bad). By introducing mapping dictionaries that convert these string inputs into numeric values, we were able to standardize the data and evaluate it numerically.

This approach enabled a clear and consistent scoring system, simplified calculations, and reduced repetitive conditional logic. As a result, the overall code became shorter, more readable, and easier to maintain.

**Problems**
1. Project Management & Time Management

One of the main challenges of the project was project management, particularly task distribution and time management. During the first phase of the project, progress was slower than expected, and for several weeks no concrete implementation or clear technical approach had been defined. This was partly due to uncertainty about how to translate the lecture content, which was taught step by step, into a complete and independent project.

As a result, a significant portion of the development work had to be completed closer to the submission deadline. This required increased coordination, parallel work, and fast decision-making within the team.

Through this experience, the team learned the importance of:

- defining a clear project structure early on,
- assigning responsibilities at an earlier stage,
- and aligning implementation steps more closely with lecture progress.

Despite these challenges, the team successfully reorganized tasks, focused on core functionality, and delivered a working and well-structured application.

2. Limitations

Due to the late start of the implementation phase and limited remaining time before submission, it was not possible to go into greater technical depth in all parts of the code. While the core functionality, validation, and data storage were implemented successfully, some areas could not be refined as thoroughly as initially intended.

- As a result, the project’s limitations mainly concern:
- limited time for deeper refactoring and optimization,
- fewer edge-case tests and extended error handling, reduced opportunity to explore more advanced features introduced later in the lectures.

These limitations are primarily related to time and project management constraints rather than conceptual or technical understanding. Given more time, the project could be extended with cleaner abstractions, additional tests, and more advanced logic.

2. 1 Limitations in our current code

1) classify_steps() doesn’t return anything (bug)

    Right now:
    ```python
    def classify_steps():
        s = ask_number("Steps: ", 0, 50000)
    ```

    There is no return, so steps becomes None.
    That affects scoring and weekly/monthly averages.

    Fix idea:
    Return a category like you do for water:

    1 = low, 2 = medium, 3 = high

2) Duplicate functions in the same file

    We define to_number() and process_day() twice (copy-paste).
    That’s confusing and risky because later changes might only happen in one copy.

    Limitation statement: code duplication → harder maintenance.

    Improve: keep only one version, and move scoring/advice into a separate module (you already planned wellness_score.py).

3) No “28-day history” enforcement although comments say so

    save_data() “maintains 28+ day history”, but it actually saves everything forever:
    
    data.append(processed)
    save_data(data)

    No trimming to last 28 entries.

    Improve: after append do:

    data = data[-28:]

4) File handling isn’t safe / robust

    You use:

    ```python
    json.load(open(DATA_FILE))
    json.dump(data, open(DATA_FILE, "w"), ...)
    ```

    This works, but if something goes wrong, files may stay open. Also, if the JSON file is empty/corrupted the program will crash.

    Improve:
    - use with open(...) as f:
    - add try/except json.JSONDecodeError

5) Weekly log and weekly report are inconsistent

    You write weekly data into weekly_data.txt, but the weekly report is generated from JSON data. The txt log is basically not used for reporting, only for “pretty history”.

    Limitation: duplicated storage formats (JSON + TXT) without a clear purpose.

    Improve: choose one source of truth (JSON), and generate TXT reports from it.

6) Data validation is good, but not consistent for all fields
    - ask_choice() forces valid strings ✅
    - ask_number() is okay ✅

    But “water” and “steps” are classified while “work_hours” is raw float — yet your score calculation ignores work_hours completely.

    Limitation: some metrics are collected but not used in score, so tracking feels incomplete.

    Improve: either:
    - include work_hours in score logic, or
    - remove it from scoring expectations and use it only in reports.

7) FIELDS_NUMERIC includes fields that aren’t always numeric in meaning

    Your YES/NO mapping: no = 1, yes = 2 works for math, but it makes averages like:
    - friends average = 1.6 (what does that mean?)

    Limitation: averages are not always intuitive.

    Improve: convert average back to meaningful text:
    - 1–1.49 = mostly no
    - 1.5–2 = mostly yes

8) Monthly report uses all data, not “this month”

    save_monthly_report(data) calculates averages across the entire dataset, even if it spans months.

    Limitation: the “monthly report” isn’t truly monthly.

    Improve: filter data to entries where date month/year equals current month/year.

9) Minor: ask_number message has a small edge case

    This part:

    if min_val and max_val


    If min_val is 0, it evaluates False, so your range message won’t show.

    Improve: use min_val is not None checks.

2. 3 What I’d consider doing next (Future improvements)

If you need a strong “what we would do with more time” list:

    1) Fix steps classification (return values) and validate that all fields are numeric as expected.
    2) Remove duplicated functions and split into modules cleanly:
        - storage.py, validation.py, scoring.py, reports.py
    3) Implement true 28-day window and true “weekly/monthly” filters by date.
    4) More testing: especially edge cases (empty/corrupted JSON, non-number input, missing keys).
    5) Improve reporting clarity: translate averages back into labels (“mostly yes”, “sleep: good on average”).
    6) Make score system transparent (show how points are calculated in the daily output).



## 📝 License

This project is provided for **educational use only** as part of the Programming Foundations module.  
[MIT License](LICENSE)
