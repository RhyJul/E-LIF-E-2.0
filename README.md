# ✔️ E-life(e) – Habit Tracker

> 🚧 This is a template repository for student project in the course Programming Foundations at FHNW, BSc BIT.  
> 🚧 Do not keep this section in your final submission.

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
> 🚧 Describe the real-world problem your application solves. (Not HOW, but WHAT)

💡 Example: In a busy lifestyle, individuals often lack a simple, consolidated way to track and assess their daily wellness habits (e.g., sleep, stress, water, exercise). This lack of immediate feedback makes it difficult to maintain awareness, identify patterns, and make necessary adjustments to achieve their health and habit goals.

**Scenario**
> 🚧 Describe when and how a user will use your application

💡 Example: The E-lif(e) Tracker is designed for quick, end-of-day use. The user runs the application from the console, is prompted with quick questions about their day's habits, and, upon completion, automatically generates a clear status report with a personalized wellness score and actionable advice. This provides an immediate, clear overview without complex setup or extensive data entry.

**User stories:**
1. As a user, I want to track my daily habits by answering simple, quick questions.
2. As a user, I want to select from predefined options (e.g., good/medium/bad) or input simple numeric values for answers.
3. As a user, I want a daily status report that gives advice based on my input
4. As a user, I want the history of my daily reports to be saved so I can view my progress over time.

---

## ✅ Project Requirements

Each app must meet the following three criteria in order to be accepted (see also the official project guidelines PDF on Moodle):

1. Interactive app (console input)
2. Data validation (input checking)
3. File processing (read/write)

---

### 1. Interactive App (Console Input)

> 🚧 In this section, document how your project fulfills each criterion.  
---
The application interacts with the user via the console. Users can:
- View all the habits 
- Select habit and answer the question 
- See the results of each habit - Receive a daily/weekly overview of the habits

---


### 2. Data Validation 

The application validates all user input to ensure data integrity and a smooth user experience. This is implemented in `main-invoice.py` as follows:

- **Stress level validation:** When the user enters their daily stress level, the program ensures that the input is a number between 1 and 5:
	```python
	if not stress.isdigit() or not (1 <= int(stress) <= 5):
    	print("⚠️ Please enter a number between 1 and 5.")
			continue
	```

- **Sleep quality validation:** The user must choose from specific options (good, medium, bad):
	```python
	if sleep_quality.lower() not in ["good", "medium", "bad"]:
    	print("⚠️ Invalid input. Please choose: good, medium, or bad.")
    		continue

	```

- **Yes/No questions (friends, exercise, hobbies, medication):** For binary inputs, the program checks if the user enters only yes or no:
	```python
	if answer.lower() not in ["yes", "no"]:
    	print("⚠️ Please enter 'yes' or 'no'.")
    		continue

	```

- **YWater intake validation:** Water intake is checked to confirm that the input is numeric and within realistic limits:
	```python
	try:
	water = float(water_input)
	except ValueError:
    print("⚠️ Please enter a valid number (e.g., 1.5).")
    		continue

	```

- **Step count validation:** The number of steps is verified to be a positive integer:
	```python
	if not steps.isdigit() or int(steps) < 0:
    	print("⚠️ Invalid input. Please enter a positive number.")
    		continue

	```


These checks prevent crashes and guide the user to provide correct input, matching the validation requirements described in the project guidelines.

---

---


### 3. File Processing 

The application reads and writes data using files:

- **Input file:** `weekly_data.txt` — Contains the user’s tracked daily data, one line per day in the format:
				Day;SleepQuality;StressLevel;Friends;WaterIntake;Exercise;Mood;WorkHours;Hobbies;Steps;Medication:
	
	Example:

	```python
				Day 1;good;3;yes;1.5;yes;happy;8;yes;8000;no
				Day 2;medium;4;no;1.0;no;anxious;9;no;5000;yes
				Day 3;bad;5;no;0.7;no;irritable;10;no;3000;no

		```
- The application reads this file to generate a weekly summary and give personalized advice.
- Reading the file (example implementation):

		```python
		with open("weekly_data.txt", "r") as file:
   			 for line in file:
        parts = line.strip().split(";")
        if len(parts) == 11:
            data.append(parts)
        else:
            print(f"⚠️ Skipping invalid line: {line.strip()}")

		```

- **Output file:** `report.txt` — Generated after completing a week of entries.
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
├─ main.py              # main entry point (this file)
├─ summary_logic.py     # Lara + helpers from Inês, calls storage from Sarah
├─ storage_csv.py       # Sarah's CSV module
├─ analysis_csv.py      # optional: simple CSV stats
└─ wellness_data.csv    # created automatically after first run
```

### How to Run
> 🚧 Adjust if needed.
1. Open the repository in **GitHub Codespaces**
2. Open the **Terminal**
3. Run:
	```bash
	python3 main.py
	```

### Libraries Used

- `os`: Check if files exist and handle paths.
- `csv` → Write and read daily input data in structured form.
- `datetime` → Add timestamps or weekly summaries.

All used libraries are built into Python’s standard library..

These libraries are part of the Python standard library, so no external installation is required. They were chosen for their simplicity and effectiveness in handling file management tasks in a console application.


## 👥 Team & Contributions

> 🚧 Fill in the names of all team members and describe their individual contributions below. Each student should be responsible for at least one part of the project.

| Name       	   | Contribution                                 |
|------------------|----------------------------------------------|
| da Costa Inês    | Menu reading (file input) and displaying menu|
| Haefliger Sarah  | Order logic and data validation              |
| Jegge Lara 	   | Invoice generation (file output) and slides  |
--------------------------------------------------------------------------------------------------------------------------------------------------------------
1️⃣ Who did what (for your documentation)
You can copy-paste and adjust names if you like:
Team Roles & Responsibilities
Inês – Input & Validation
Designed and implemented the user input flow for the daily tracker.
Wrote reusable helper functions:
ask_yes_no()
ask_int_in_range()
ask_non_negative_int()
ask_non_negative_float()
ask_choice()
Integrated these helpers into the main e_life_tracker() function to avoid repeated code and make input validation beginner-friendly.
Sarah – CSV Storage
Created the file storage_csv.py to handle all CSV file operations.
Defined the CSV structure via FIELDNAMES (including date, score, sleep, stress, etc.).
Implemented:
ensure_csv_exists() → creates wellness_data.csv with a header row.
append_entry(entry_dict) → appends one validated daily entry as a row.
Helped design build_entry_dict() in summary_logic.py so daily tracker results are saved correctly.
Lara – Summary & Logic
Designed the wellness scoring logic and advice system in summary_logic.py.
Implemented:
fun_girly_message(score) → fun daily message based on score.
generate_daily_summaries_girly(inputs) → text summaries per category (sleep, mood, water, etc.).
generate_monthly_report_girly(month_data) → end-of-month “GirlyPop” style report using averages and mood stats.
e_life_tracker() → collects one full day (using Inês’ helpers) and returns score, advice, summaries, and inputs.
run_month() → loops over multiple days, calls e_life_tracker(), saves to CSV (Sarah’s part), and prints the monthly report.
Bonus: Simple Analysis Script
An extra file analysis_csv.py reads wellness_data.csv and prints basic statistics (average score, average stress, average steps, sleep counts).

------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
## 🤝 Contributing

> 🚧 This is a template repository for student projects.  
> 🚧 Do not change this section in your final submission.

- Use this repository as a starting point by importing it into your own GitHub account.  
- Work only within your own copy — do not push to the original template.  
- Commit regularly to track your progress.

## 📝 License

This project is provided for **educational use only** as part of the Programming Foundations module.  
[MIT License](LICENSE)
