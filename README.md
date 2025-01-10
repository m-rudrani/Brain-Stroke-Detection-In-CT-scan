# Brain-Stroke-Detection-In-CT-scan

## Brain Stroke Lab README

### Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technical Requirements](#technical-requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

### Introduction

Brain Stroke Lab is a web-based application designed to assist in the early detection and prevention of brain strokes. The application uses advanced medical imaging analysis and artificial intelligence algorithms to provide users with a user-friendly interface to input relevant medical data and receive real-time assessments of stroke risk.

---

### Features

- User registration and login system
- Image upload feature for CT scans
- Machine learning-based prediction system for brain stroke detection
- Admin panel for managing user accounts and viewing prediction data
- Contact and About pages for users to learn more about the Brain Stroke Lab

---

### Technical Requirements

- Python 3.8 or higher
- Flask 2.0 or higher
- SQLite 3.22 or higher
- Bootstrap 5.1 or higher
- Font Awesome 5.15 or higher
- Machine learning model (stored in a file named `model.h5`)

---

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/brain-stroke-lab.git
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a new SQLite database file named `database.db` in the root directory.

4. Run the application:
   ```bash
   python app.py
   ```

---

### Usage

1. Open a web browser and navigate to `http://localhost:5000`.
2. Register a new user account or log in to an existing account.
3. Upload a CT scan image to the application.
4. View the prediction results and manage user accounts from the admin panel.

---

### Screenshots

#### Home Page
![Home Page](static/screenshots/homepage.png)

#### Upload Image Page
![Upload Page](static/screenshots/upload.png)

#### Prediction Result
![Prediction Result](static/screenshots/result.png)

#### Admin Panel
![Admin Panel](static/screenshots/admin.png)

*Ensure that screenshots are stored in `static/screenshots/` directory.*

---

### Contributing

Contributions are welcome! Please submit a pull request with your changes and a brief description of the changes made.

---

### License

This project is licensed under the MIT License. See the LICENSE file for more information.

---

### Acknowledgments

- This project was developed using the Flask web framework and SQLite database management system.
- The machine learning model was trained using a dataset of CT scan images.
- The application uses Bootstrap and Font Awesome for styling and icons.

