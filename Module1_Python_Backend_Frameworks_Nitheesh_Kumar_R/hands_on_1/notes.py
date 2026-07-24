"""
Task 1: Understand the Request-Response Cycle

1. Request-Response Cycle in Django:
   - A user sends an HTTP request (e.g., GET /api/courses/) from their browser.
   - The request hits the Django application and passes through the URL router (urls.py).
   - The URL router matches the requested URL to a specific View function or class.
   - The View processes the request. If it needs data, it interacts with the Model (models.py) to perform a DB query.
   - The Model returns the requested data to the View.
   - The View formats the data (often using a Template or a serializer for APIs) and constructs an HTTP response.
   - The response is sent back through middleware to the user's browser.

2. Middleware:
   - Middleware sits between the web server and the view, acting as a series of hooks in the request/response processing mechanism. It processes requests before they reach the view and processes responses before they are returned to the user.
   - Built-in Django middleware examples:
     a) AuthenticationMiddleware: Associates users with requests using sessions. It adds the `request.user` attribute, representing the currently logged-in user.
     b) CsrfViewMiddleware: Adds protection against Cross-Site Request Forgeries by adding hidden form fields to POST forms and checking requests for the correct value.

3. WSGI vs ASGI:
   - WSGI (Web Server Gateway Interface): The traditional, synchronous standard for Python web applications. It handles one request at a time per worker process/thread.
   - ASGI (Asynchronous Server Gateway Interface): The modern, asynchronous standard. It allows handling multiple concurrent requests (e.g., WebSockets, long-polling, async I/O) without blocking the thread.
   - Django uses WSGI by default.
   - You would switch to ASGI when building real-time applications that require persistent connections (like chat apps with WebSockets) or when you need high concurrency with asynchronous views/tasks.

4. MVC vs MVT Pattern:
   - MVC (Model-View-Controller) is a software design pattern for developing user interfaces that divides the related program logic into three interconnected elements.
   - Django uses a variation called MVT (Model-View-Template).
   - MVT mapping to MVC:
     - Model (Django MVT) maps to Model (MVC): Handles data access, validation, and relationships (database interactions).
     - View (Django MVT) maps to Controller (MVC): Handles the business logic, receives requests, fetches data from models, and delegates rendering.
     - Template (Django MVT) maps to View (MVC): Handles presentation logic, defining how the data is presented to the user (HTML/UI).
"""
