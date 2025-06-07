# 🧩 OVERVIEW

## A. Background

**Great Commissioners International _(GCI)_** Church operates with departments to ensure effective administration and spiritual growth. One of these departments is the **Schools Department**, responsible for training and spiritual formation through structured learning programs such as:

- **School of Foundation**
- **School of Ministry**
- **School of Leadership**

Currently, most school activities are handled **manually or physically** — including registration, attendance, progress tracking, and module delivery. This has led to operational inefficiencies, difficulty in data management, and limited scalability.


## B. Problem Statement

<table>
  <thead>
    <tr>
      <th>Aspect</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>The Problem of:</strong></td>
      <td>Manual handling of school activities leading to errors, delays, poor tracking of student progress, and lack of centralized data.</td>
    </tr>
    <tr>
      <td><strong>Which Affects:</strong></td>
      <td>Students, instructors, and administrators who struggle with fragmented information, poor communication, and lack of visibility into academic progress and administration.</td>
    </tr>
    <tr>
      <td><strong>For Which a Capable Solution Would Be:</strong></td>
      <td>A centralized web-based platform to manage the activities of all schools under the department.</td>
    </tr>
    <tr>
      <td><strong>Which Would:</strong></td>
      <td>
        <ul>
          <li>Digitize the enrollment and module management process.</li>
          <li>Allow students to track their progress.</li>
          <li>Empower instructors to structure and manage their modules and students.</li>
          <li>Provide administrators with tools to oversee the entire system efficiently.</li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

## C. Project Stakeholders

<table>
  <thead>
    <tr>
      <th>Stakeholder</th>
      <th>Role and Responsibilities</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>GCI Church Leadership:</strong></td>
      <td>Approves and oversees the overall project vision; ensures alignment with the church’s mission.</td>
    </tr>
    <tr>
      <td><strong>Schools Department Head:</strong></td>
      <td>Provides detailed requirements; ensures the system meets the administrative needs of the schools.</td>
    </tr>
    <tr>
      <td><strong>Schools Department Instructors:</strong></td>
      <td>Deliver content, manage modules, and track student participation and progress.</td>
    </tr>
    <tr>
      <td><strong>Students / Church Members:</strong></td>
      <td>End-users of the platform who will enroll in and participate in school modules.</td>
    </tr>
    <tr>
      <td><strong>Media Department Developers:</strong></td>
      <td>Design, develop, and maintain the web application; implement features and ensure usability.</td>
    </tr>
  </tbody>
</table>

## D. Project Scope 

This project involves the development of an **online system** — a web application for managing all church schools. The system will be scalable, modular, and ready for future features like certificate generation, attendance tracking, assessments, and more.

## E. Objectives

<table>
  <thead>
    <tr>
      <th>Objective Type</th>
      <th>Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Functional Objectives:</strong><br><em>The system must...</em></td>
      <td>
        <ul>
          <li>Allow creation and management of multiple schools (e.g., Foundation, Ministry, Leadership)</li>
          <li>Allow each school to have multiple modules</li>
          <li>Support student registration and module enrollment</li>
          <li>Track student progress and completion status</li>
          <li>Enable instructors to manage module content and attendance</li>
          <li>Provide admin interfaces for user, school, and module management</li>
          <li>Ensure role-based access control (admin, instructor, student)</li>
          <li>Maintain audit trails of enrollment and module updates</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td><strong>Non-Functional Objectives:</strong><br><em>The system should...</em></td>
      <td>
        <ul>
          <li>Be <strong>secure</strong> — use authentication and authorization (role-based)</li>
          <li>Be <strong>scalable</strong> — support more schools, modules, and users over time</li>
          <li>Be <strong>reliable</strong> — ensure minimal downtime</li>
          <li>Be <strong>responsive</strong> — accessible on mobile and desktop</li>
          <li>Be <strong>user-friendly</strong> — clean UI, intuitive navigation</li>
          <li>Be <strong>auditable</strong> — maintain logs of critical operations</li>
          <li>Be <strong>portable</strong> — deployable on most cloud or on-prem environments</li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

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
