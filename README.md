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
> 🚧 Please remove this paragraphs having "🚧". These are comments for preparing the documentations.
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

To ensure the application collects accurate and meaningful information, each user input is assigned to a specific category and validated using an appropriate data type. This structure helps maintain data integrity throughout the program and ensures users provide responses that match the expected format. Below is an overview of the input categories used in the application alongside their corresponding data types and validation rules: 

The application validates all user input to ensure data integrity and a smooth user experience. This is implemented in `main-invoice.py` as follows:

- **Stress level validation:** When the user enters their daily stress level, the program ensures that the input is a number between 1 and 5:
Category: Daily stress measurement (1–5)
Data type: Integer
Validation: Must be a number between 1 and 5

	```python
	if not stress.isdigit() or not (1 <= int(stress) <= 5):
    	print("⚠️ Please enter a number between 1 and 5.")
			continue
	```

- **Sleep quality validation:** The user must choose from specific options (good, medium, bad):
Category: Sleep rating
Data type: String
Validation: Must be one of: good, medium, bad

	```python
	if sleep_quality.lower() not in ["good", "medium", "bad"]:
    	print("⚠️ Invalid input. Please choose: good, medium, or bad.")
    		continue

	```

- **Yes/No questions (friends, exercise, hobbies, medication):** For binary inputs, the program checks if the user enters only yes or no:
Category: Social and health habits (friends, exercise, hobbies, medication)
Data type: String
Validation: Must be yes or no

	```python
	if answer.lower() not in ["yes", "no"]:
    	print("⚠️ Please enter 'yes' or 'no'.")
    		continue

	```

- **Water intake validation:** Water intake is checked to confirm that the input is numeric and within realistic limits:
Category: Daily water consumption in liters
Data type: Float
Validation: Must be a valid number (e.g., 1.5) — non-numeric input is rejected

	```python
	try:
	water = float(water_input)
	except ValueError:
    print("⚠️ Please enter a valid number (e.g., 1.5).")
    		continue

	```

- **Step count validation:** The number of steps is verified to be a positive integer:
Category: Physical activity measurement
Data type: Integer
Validation: Must be a positive number

	```python
	if not steps.isdigit() or int(steps) < 0:
    	print("⚠️ Invalid input. Please enter a positive number.")
    		continue

	```


These checks prevent crashes and guide the user to provide correct input, matching the validation requirements described in the project guidelines.


### 3. File Processing 

The application reads and writes data using files:

- **Input file:** `input_validation.py` — Contains the user’s tracked daily data, one line per day in the format:
				   Day;SleepQuality;StressLevel;Friends;WaterIntake;Exercise;Mood;WorkHours;Hobbies;Steps;Medication:
	
	Example:

	```python
				Day 1;good;3;yes;1.5;yes;happy;8;yes;8000;no
				Day 2;medium;4;no;1.0;no;anxious;9;no;5000;yes
				Day 3;bad;5;no;0.7;no;irritable;10;no;3000;no

		```
- The application reads this file to generate a weekly or monthly summary and give personalized advice.
- Reading the file (example implementation):

		```python
		with open("input_validation.py", "r") as file:
   			 for line in file:
        parts = line.strip().split(";")
        if len(parts) == 11:
            data.append(parts)
        else:
            print(f"⚠️ Skipping invalid line: {line.strip()}")

		```

- **Output file:** `report.txt` — Generated after completing a week or month of entries.
					The file contains averages, insights, and advice based on the collected data.
		Example:

		```python
		
		E-lif(e) Weekly Report
		---------------------------
		Average stress level: 3.7
		Sleep quality: mostly medium
		Average water intake: 1.2L
		Steps: great job (average 8,200)
		Exercise: 4/7 days
		Mood summary: balanced, slightly anxious midweek

		💡 Advice:
		- Try to increase water intake to 1.5L daily.
		- Reduce stress through light exercise or mindfulness.
		- Keep up the good step count!

		```
 - Writing the file (example implementation):

		```python

		with open("report.txt", "w") as file:
    	file.write("E-lif(e) Weekly Report\n")
    	file.write("---------------------------\n")
    	file.write(f"Average stress level: {avg_stress}\n")
    	file.write(f"Average steps: {avg_steps}\n")
    	file.write("💡 Advice: Stay hydrated and manage stress.\n") 

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
- `from menu import`: main_menu

All used libraries are built into Python’s standard library.

These libraries are part of the Python standard library, so no external installation is required. They were chosen for their simplicity and effectiveness in handling file management tasks in a console application.


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
----------------------------------------------------------------------------------------------------------------------------------------------------------## 🤝 Contributing

- Use this repository as a starting point by importing it into your own GitHub account.  
- Work only within your own copy — do not push to the original template.  
- Commit regularly to track your progress.

## 📝 License

This project is provided for **educational use only** as part of the Programming Foundations module.  
[MIT License](LICENSE)
