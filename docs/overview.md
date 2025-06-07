# 🧩 OVERVIEW

## A. Background

**Great Commissioners International _(GCI)_** Church operates with departments to ensure effective administration and spiritual growth. One of these departments is the **Schools Department**, responsible for training and spiritual formation through structured learning programs such as:

- **School of Foundation**
- **School of Ministry**
- **School of Leadership**

Currently, most school activities are handled **manually or physically** — including registration, attendance, progress tracking, and module delivery. This has led to operational inefficiencies, difficulty in data management, and limited scalability.


## B. Problem Statement

- **The Problem of:**  
  Manual handling of school activities leading to errors, delays, poor tracking of student progress, and lack of centralized data.

- **Which Affects:**  
  Students, instructors, and administrators who struggle with fragmented information, poor communication, and lack of visibility into academic progress and administration.

- **For Which a Capable Solution Would Be:**  
  A centralized web-based platform to manage the activities of all schools under the department.

- **Which Would:**  
  - Digitize the enrollment and module management process.
  - Allow students to track their progress.
  - Empower instructors to structure and manage their modules and students.
  - Provide administrators with tools to oversee the entire system efficiently.


## C. Project Stakeholders

- **GCI Church Leadership:**  
  Approves and oversees the overall project vision; ensures alignment with the church’s mission.

- **Schools Department Head:**  
  Provides detailed requirements; ensures the system meets the administrative needs of the schools.

- **Schools Department Instructors / Facilitators:**  
  Deliver content, manage modules, and track student participation and progress.

- **Students / Church Members:**  
  End-users of the platform who will enroll in and participate in school modules.

- **Media Department Developers:**  
  Design, develop, and maintain the web application; implement features and ensure usability.

## D. Project Scope 

This project involves the development of an **online system** — a web application for managing all church schools. The system will be scalable, modular, and ready for future features like certificate generation, attendance tracking, assessments, and more.

## E. Objectives

- **Functional Objectives _(The System Must...)_**
  - Allow creation and management of multiple schools (e.g., Foundation, Ministry, Leadership)
  - Allow each school to have multiple modules
  - Support student registration and module enrollment
  - Track student progress and completion status
  - Enable instructors to manage module content and attendance
  - Provide admin interfaces for user, school, and module management
  - Ensure role-based access control (admin, instructor, student)
  - Maintain audit trails of enrollment and module updates

- **Non-Functional Objectives _(The System Should...)_**
  - Be secure — use authentication and authorization (role-based)
  - Be scalable — support more schools, modules, and users over time 
  - Be reliable — ensure minimal downtime 
  - Be responsive — accessible on mobile and desktop 
  - Be user-friendly — clean UI, intuitive navigation 
  - Be auditable — maintain logs of critical operations 
  - Be portable — deployable on most cloud or on-prem environments

## F. Tech Stack

- <a href="https://www.djangoproject.com/" target="_blank">Django (Backend)</a>
- <a href="https://sqlite.org/" target="_blank">Sqlite (Development Database)</a>
- <a href="https://www.postgresql.org/" target="_blank">PostgreSQL (Production Database)</a>
- <a href="https://getbootstrap.com/" target="_blank">Bootstrap and other frontend vendors (Frontend enhancements)</a>
- <a href="https://python-poetry.org/" target="_blank">Python Poetry (Dependency management)</a>

## 📚 Guides:

- 🧭 [Index](index.md)
- 🧩 [Overview](overview.md)
- 🗺️ [System Context](system_context.md)
- 🎯 [System Use Cases](system_use_cases.md)
- 🗄️ [System Database Design](system_database_design.md)
- 🛠️ [Setup Development](setup_development.md)
- 🚀 [Setup Production](setup_production.md)
