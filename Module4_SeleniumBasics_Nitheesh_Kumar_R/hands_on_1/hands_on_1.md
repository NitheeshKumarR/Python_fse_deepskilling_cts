# QA Concepts, Functional Testing & Defect Lifecycle

## Task 1: Map Testing Types to a Real System

### 1 & 2. Testing Types & Classifications
*   **Unit Testing (Functional):** Test the `get_password_hash()` utility function in isolation. Provide a dummy string and assert that the output string matches the expected bcrypt format and length.
*   **Integration Testing (Functional):** Test the API Endpoint + Database interaction by making a `POST /api/courses/` request with valid data using a test database, then directly querying the database to ensure a record was created with the correct data.
*   **System Testing (Functional):** Test the full enrollment flow by authenticating, POSTing to `/api/students/1/enroll`, and verifying both the HTTP 201 response and the execution of the background confirmation email task.
*   **User Acceptance Testing (Functional):** A college administrator tests the web interface to verify they can successfully add a new Department, create a Course within that Department, and view it on the public catalog, mimicking their daily workflow.
*   **Non-Functional Testing Example (Performance/Load):** Send 500 concurrent requests to the `GET /api/courses/` endpoint using a tool like JMeter to ensure the average response time remains under 200ms and no 5xx errors are thrown under heavy load.

### 3. Black-Box vs White-Box Testing
*   **Black-Box Testing:** Testing the software without any knowledge of its internal structure, source code, or implementation details. The tester treats the application as a "black box," focusing strictly on inputs and outputs. **Typically performed by QA Testers.**
*   **White-Box Testing:** Testing the software with full knowledge of the internal source code, architecture, and logic. The tester writes tests to exercise specific code paths, loops, and conditions. **Typically performed by Developers (e.g., writing Unit tests).**

### 4. Formal Test Cases for `POST /api/courses/`

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_API_001** | Verify successful course creation with valid data | User is authenticated with a valid JWT token. DB is running. | 1. Send POST request to `/api/courses/` with JSON body containing valid `name`, `code`, `credits`, and `department_id`. | HTTP 201 Created response. Response body contains course details with a new `id`. Location header is present. | | |
| **TC_API_002** | Verify course creation fails if `code` is duplicated | User is authenticated. A course with code 'CS101' already exists in the DB. | 1. Send POST request to `/api/courses/` with JSON body containing `code: "CS101"`. | HTTP 409 Conflict (or 422). Error message indicates code must be unique. | | |
| **TC_API_003** | Verify API rejects unauthorized requests | User does NOT have a valid JWT token. | 1. Send POST request to `/api/courses/` without an Authorization header. | HTTP 401 Unauthorized response. Course is not created in DB. | | |

---

## Task 2: Defect Lifecycle & Severity Classification

### 5. Defect Lifecycle
**New** &rarr; **Assigned** (Developer picks it up) &rarr; **Open** (Developer is actively working on it) &rarr; **Fixed** (Developer pushes a code fix) &rarr; **Retest** (QA verifies the exact steps that failed) &rarr; **Verified** (QA confirms the fix works) &rarr; **Closed** (Bug is resolved).
*   **Rejected path:** If the developer determines it's not a bug (e.g., it's a misunderstanding of requirements or an environment issue), it moves from Open &rarr; Rejected.
*   **Deferred path:** If the bug is recognized but not critical for the current release, it moves from Open &rarr; Deferred (to be fixed in a later sprint).

### 6. Severity & Priority Classification
*   **a) POST /api/courses/ returns 500 Internal Server Error for all requests.**
    *   **Severity:** Critical (Core functionality is completely broken, preventing any user from adding courses).
    *   **Priority:** P1 (Must be fixed immediately to restore primary system operation).
*   **b) Course names longer than 150 characters are silently truncated without an error.**
    *   **Severity:** Medium (Data loss occurs without warning, but it only affects unusually long course names; the system still functions overall).
    *   **Priority:** P3 (Should be fixed to prevent data issues, but not an immediate emergency).
*   **c) The /docs Swagger page has a typo in the API description.**
    *   **Severity:** Low (Purely cosmetic; does not affect the functionality or usage of the API).
    *   **Priority:** P4 (Can be fixed whenever a developer has spare time; does not block anything).
*   **d) Login with correct credentials occasionally returns 401 on the first attempt (intermittent).**
    *   **Severity:** Medium (Users can eventually log in if they try again, so functionality is not entirely blocked).
    *   **Priority:** P1 or P2 (Highly disruptive to the user experience and breaks trust, indicating underlying instability that needs urgent investigation).

### 7. Defect Report
**Defect ID:** DEF-1001
**Title:** POST /api/courses/ consistently throws 500 Internal Server Error
**Environment:** Staging Server (Ubuntu 22.04), SQLite Database
**Build Version:** v1.0.4-rc
**Severity:** Critical
**Priority:** P1
**Steps to Reproduce:**
1. Authenticate via `/api/auth/login/` to acquire a valid JWT token.
2. Send a POST request to `/api/courses/` with a valid JSON payload (`name`, `code`, `credits`, `department_id`).
**Expected Result:** System should return a 201 Created status code and store the new course in the database.
**Actual Result:** System returns a 500 Internal Server Error immediately. No data is saved to the database.
**Attachments:** screenshot of 500 error

### 8. Severity vs Priority
*   **Severity** describes the technical impact of a defect on the software system (e.g., does it crash? does it corrupt data?).
*   **Priority** describes the business urgency to fix the defect (e.g., how quickly do we need to fix this?).
*   **Real-World Example (High Severity / Low Priority):** A bug causes the application to completely crash (High Severity) but only if a user performs an incredibly obscure combination of steps on an outdated, unsupported browser like Internet Explorer 8 that 0.01% of customers use. Because it rarely affects users, the business gives it a Low Priority to fix. 
    *(Conversely, a misspelled company name on the main homepage is Low Severity because the site still functions perfectly, but High Priority because it damages the brand reputation and is highly visible).*
