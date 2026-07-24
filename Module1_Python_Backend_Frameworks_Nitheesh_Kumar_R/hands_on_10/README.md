# Microservices Architecture: Hands-On 10

## Monolith Decomposition Strategy

We have successfully decomposed the monolithic Course Management API into distinct microservices, strictly adhering to bounded contexts.

| Service Name | Responsibility | Endpoints it owns | Database it owns |
| --- | --- | --- | --- |
| **Course Service** | Manages the catalog of departments and courses. | `/api/courses/*` | `courses.db` (Departments, Courses) |
| **Student Service** | Manages students and their course enrollments. | `/api/students/*` | `students.db` (Students, Enrollments) |

### Key Principle Applied
**Database per Service:** The `student_service` holds an `Enrollment` table containing `course_id`. However, it does not have a foreign key strictly bound to a `courses` table because the course catalog lives in an entirely separate database (`courses.db`) owned by the `course_service`. When an enrollment happens, `student_service` asks `course_service` via HTTP to verify the course.

---

## Inter-Service Communication Trade-offs

In this architecture, when a user posts to `/api/students/1/enroll`, the Student Service uses a **Synchronous HTTP Call** to the Course Service to verify the `course_id`.

### Synchronous (HTTP / REST / gRPC)
- **Pros:** 
  - Simple to implement and understand.
  - Immediate feedback (e.g., if a course doesn't exist, we can instantly return a 404).
- **Cons:** 
  - **Tight Coupling:** If Course Service is down, Student Service cannot process enrollments. It creates a single point of failure and cascading failures.
  - Slower response times (network overhead blocks the thread).

### Asynchronous (Message Queues: RabbitMQ, Kafka)
- **Pros:** 
  - **Decoupling:** If Course Service goes down, the enrollment request can sit safely in a queue. When the service comes back online, it processes the backlog.
  - Highly resilient and scalable for bursts of traffic.
- **Cons:** 
  - **Eventual Consistency:** The client doesn't get an immediate "Success" or "Failure" (e.g. course doesn't exist). They get a "Request Accepted" and have to check back later (or be notified via WebSockets/Webhooks).
  - High operational complexity.

### When to use Asynchronous messaging?
You would use a Message Queue like RabbitMQ for actions that do not require an immediate response back to the user, or for heavy background processing. In our domain, a **Notification Service** (sending welcome emails when a student registers) is the perfect candidate for asynchronous communication.
