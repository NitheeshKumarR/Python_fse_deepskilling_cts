# SDLC vs TDLC — V-Model & Agile QA Integration

## Task 1: V-Model Mapping

### 1. V-Model Diagram

```text
(SDLC Phases)                                            (TDLC Phases)
Requirements Analysis -------------------------------> Acceptance Testing
    \                                                     /
     \                                                   /
    System Design --------------------------------> System Testing
        \                                             /
         \                                           /
    Architecture Design ---------------------> Integration Testing
            \                                     /
             \                                   /
         Module Design --------------------> Unit Testing
                \                             /
                 \                           /
                  -------- Coding ---------
```

### 2. Test Artifacts per Phase

For each SDLC phase on the left side, QA prepares corresponding test artifacts for the testing phase on the right side:

*   **Requirements Analysis &harr; Acceptance Testing:** The **Acceptance Test Plan** and User Acceptance Test cases are created.
*   **System Design &harr; System Testing:** The **System Test Plan** and end-to-end system test cases are created.
*   **Architecture Design &harr; Integration Testing:** The **Integration Test Plan** and API contract/database integration test cases are created.
*   **Module Design &harr; Unit Testing:** The **Unit Test Plan** and isolated unit test cases (usually written by developers) are created.

### 3. Entry and Exit Criteria for Testing Levels

| Test Level | Entry Criteria (What must be true to start) | Exit Criteria (What must be true to finish) |
| :--- | :--- | :--- |
| **Unit Testing** | The module/component code is complete and compiles successfully without syntax errors. | All unit tests executed, 100% pass rate, code coverage meets the defined threshold (e.g., 80%). |
| **Integration Testing** | Unit testing is complete. The database and API endpoints are deployed to a test environment. | All integration tests executed, 100% pass rate. No open Critical/High defects regarding data flow. |
| **System Testing** | Integration testing is complete. The full Course Management API and frontend (or Postman suite) are deployed to Staging. | 100% of functional/non-functional system tests executed. No open High/Critical defects. Defect count is within acceptable limits. |
| **Acceptance Testing** | System testing is signed off. The staging environment mimics production. Business stakeholders are available. | Business stakeholders (e.g., College Admin) execute the UAT test plan and formally sign off on the release. |

### 4. QA Engagement in the V-Model for Course Management API

1.  **Requirements Analysis Phase:** QA reviews the initial API specs (e.g., determining what fields a Course should have). By asking "What happens if a Course name is 200 characters?" QA catches ambiguities before the database schema is even designed.
2.  **System Design Phase:** QA reviews the proposed architecture (e.g., the decision to use microservices). QA can point out that separating the Student and Course databases will require complex integration tests to ensure data consistency when enrolling students.

---

## Task 2: Agile QA and Shift-Left Testing

### 1. Problems Caused by Waterfall in Course Management API
1.  **Late Defect Discovery:** If testing only happens after development, a fundamental flaw—like using `GET` instead of `POST` for enrollment—won't be caught until weeks into the project, requiring massive rework of the API gateway and services.
2.  **Misunderstood Requirements:** Without QA involvement early on, developers might assume "Course Code" doesn't need to be unique. Finding this out during System Testing means rewriting database schemas, migrations, and model validations at the very end.
3.  **Bottlenecks:** The testing phase becomes a massive bottleneck. If development takes 4 weeks and QA takes 2, any delays in development eat directly into the QA time, leading to rushed, poor-quality releases.

### 2. QA Engineer Roles in Agile Ceremonies
*   **Sprint Planning:** QA reviews the User Stories with the Product Owner and Developers to define clear, testable Acceptance Criteria. They ensure the team understands *how* a feature will be validated.
*   **Daily Standup:** QA reports on testing progress, highlights any critical defects found in the previous day's build, and raises blockers (e.g., "The Staging environment database is down").
*   **Sprint Review:** QA often leads or assists in the demo of the working software to stakeholders, showcasing the new features (like the new JWT login flow) working flawlessly.
*   **Retrospective:** QA suggests process improvements (e.g., "We found a lot of bugs in the enrollment endpoint this sprint; next sprint, let's write API integration tests *before* merging the code").

### 3. Shift-Left Practices Applied to the API
1.  **Reviewing requirements for testability:** Before writing the `Register User` endpoint, QA asks: "How will we test email uniqueness? Do we have a script to clear the test database?"
2.  **TDD/BDD (Test/Behavior Driven Development):** QA and Developers write automated tests (like `test_api()` from Hands-On 9) *before* the API routes are actually coded. The code is then written to make the failing tests pass.
3.  **Static Code Analysis:** Integrating tools like `flake8` or `SonarQube` into the CI/CD pipeline to catch syntax errors, unused imports, or security vulnerabilities before the code is even run.
4.  **API Contract Testing:** Using tools like Swagger/OpenAPI or Postman mock servers to agree on the JSON structure of `CourseResponse` before the backend or frontend teams start building, ensuring they integrate perfectly on day one.

### 4. Acceptance Criteria (Given-When-Then / Gherkin format)

**User Story:** As a college admin, I want to create a new course, so that students can enroll in it.

*   **Scenario 1: Happy Path (Successful Creation)**
    *   **Given** I am logged in as an administrator
    *   **And** I provide a valid course name, unique code, credits, and department ID
    *   **When** I submit the request to create the course
    *   **Then** the course should be saved in the database
    *   **And** I should receive a 201 Created response containing the new course details.

*   **Scenario 2: Duplicate Course Code**
    *   **Given** I am logged in as an administrator
    *   **And** a course with the code "CS101" already exists in the system
    *   **When** I submit the request to create a new course with the code "CS101"
    *   **Then** the course should not be saved
    *   **And** I should receive a 409 Conflict response indicating the code must be unique.

*   **Scenario 3: Missing Required Fields**
    *   **Given** I am logged in as an administrator
    *   **When** I submit the request to create a course but leave the "credits" field empty
    *   **Then** the course should not be saved
    *   **And** I should receive a 422 Unprocessable Entity response highlighting the missing field.
