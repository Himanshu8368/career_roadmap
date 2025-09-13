# Career Roadmap Tracker

Career Roadmap Tracker is a Python-based command-line application designed to help users set, track, and manage their career development milestones efficiently.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Configuration](#configuration)
- [Example Workflow](#example-workflow)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Add Career Goals:** Create new goals with descriptions and target dates.
- **Update Goals:** Modify existing goals, update progress, or change deadlines.
- **Delete Goals:** Remove goals that are no longer relevant.
- **Track Progress:** View and update the completion status of each goal.
- **Command-Line Interface:** Simple and interactive prompts for managing your roadmap.
- **Data Persistence:** Goals are saved locally for future sessions.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Git (for cloning the repository)

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/Career_roadmap_tracker.git
    cd Career_roadmap_tracker
    ```

2. **(Optional) Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**
    This project uses only standard Python libraries, so no additional installation is required.

## Usage

Run the main script from the project directory:

```bash
python code.py
```

You will be prompted to:

- Add a new career goal
- View all goals and their progress
- Update or delete existing goals
- Mark goals as completed

All data is stored locally in a file (`goals.json`).

## Configuration

- By default, the application stores data in `goals.json` in the project directory.
- You can modify the storage location by editing the relevant path in `code.py`.

## Example Workflow

1. **Add a goal:**  
   _"Learn Python for Data Analysis by 2024-09-01"_

2. **View progress:**  
   See a list of all goals and their completion status.

3. **Update a goal:**  
   Change the target date or update progress notes.

4. **Delete a goal:**  
   Remove goals that are no longer relevant.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes.
4. Push to your fork and submit a pull request.

For major changes, please open an issue first to discuss your ideas.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
