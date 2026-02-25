# Job / Internship Portal (Flask + MySQL)

This is a full-stack Job/Internship Listing Portal developed using Python (Flask) and MySQL. The application allows users to search and filter jobs, bookmark listings, and apply by submitting their details and resume. It also includes an Admin Portal where administrators can securely log in to add or delete job postings.

## Key Features
- Job listing cards with company, location, salary, and type
- Search by title or skills
- Filter by location and category
- Bookmark (Save) jobs
- Apply form with resume upload
- Admin login with job management (Add/Delete)

## Technologies Used
- Python (Flask)
- MySQL
- HTML
- CSS
- JavaScript


##folder Structure
job_portal/
│
├── app.py
│
├── templates/
│     ├── index.html
│     ├── apply.html
│     ├── saved.html
│     ├── admin_login.html   ← MUST BE HERE
│     ├── admin_dashboard.html
│     └── add_job.html
│
├── static/
│     ├── style.css
│     └── script.js
