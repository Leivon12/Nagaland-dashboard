# Nagaland Data Dashboard

Statistical data explorer for Nagaland datasets (2023–2024).

## Project Structure

```
nagaland-dashboard/
├── index.html                  ← Home page (shared)
├── annual_report/
│   ├── index.html              ← Person 1
│   └── Tables_Annual_Report_2023_Nagaland.xlsx
├── disaster/
│   ├── index.html              ← Person 2
│   └── 3Disaster_Stat_Accident.xlsx
└── population/
    ├── index.html              ← Person 3
    └── 1_Population_Births__Deaths_Related_2024.xlsx
```

## Setup (Everyone does this once after cloning)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

## Running the project

```bash
# Make sure you're in the root nagaland-dashboard/ folder
python -m http.server 8000
```

Open your browser at: http://localhost:8000

## Daily workflow

```bash
# Start of session
git pull

# End of session
git add .
git commit -m "describe what you did"
git push
```

## Adding a new package

```bash
pip install <package-name>
pip freeze > requirements.txt
# Then commit requirements.txt
```
