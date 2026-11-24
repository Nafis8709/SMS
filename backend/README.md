# SMS Backend

A REST backend for the Student Management System: students, courses and course enrollment.
Built for CSE 3102L (Topic 04, Backend Frameworks and Architecture).

## Framework and why

**Flask (Python).** It is small and readable, and it is the framework of the course starter project,
so this backend uses the same layers and file layout. Data is stored in **SQLite** through Python's
built-in `sqlite3` module, so no database server or ORM is needed.

## How to run

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # Windows: copy .env.example .env
python run.py
```

The API runs at `http://localhost:5000`. The database file (`sms.db` by default) is created on first start.

| Setting | Default | Meaning |
|---|---|---|
| `APP_ENV` | `development` | Environment name |
| `LOG_LEVEL` | `INFO` | Logging level |
| `DATABASE_PATH` | `sms.db` | SQLite file path |

## How to test

```bash
cd backend
pytest
```

Each test creates its own empty database in a temporary folder, so tests are isolated and can run in any order.

| File | What it covers |
|---|---|
| `tests/test_students.py` | Student CRUD through HTTP, validation (422), malformed JSON (400), not found (404), duplicate ID (409), data stored in SQLite and still there after an app restart |
| `tests/test_courses.py` | Course CRUD, enrollment lifecycle, the seat rules (409), unknown student (422) and course (404), data stored in SQLite |
| `tests/test_services.py` | A use case run without a web server; an unexpected error is logged in full but hidden from the client |

## Architecture note

```
backend/
  app/
    __init__.py                      create_app: wiring, middleware, error handlers
    config.py                        settings from environment variables
    errors.py                        AppError, NotFound, Conflict, ValidationFailed, BadRequest
    routes/                          controllers: HTTP in, HTTP out
      students.py
      courses.py
      helpers.py                     JSON body, query checks, JSON shapes
    services/                        use cases
      student_service.py
      course_service.py
    repositories/                    the only code that touches SQLite
      database.py
      student_repository.py
      course_repository.py
      enrollment_repository.py
    domain/                          entities and rules; no Flask, no SQL
      student.py
      course.py
      validation.py
  tests/
  run.py  requirements.txt  .env.example
```

| Layer | Job | Does not |
|---|---|---|
| Routes | Read the request, call the service, build the response and status code | Hold SQL or business rules |
| Services | Run one use case, such as enroll a student, and log it | Know about HTTP, JSON or status codes |
| Repositories | Store and fetch domain objects | Decide business rules |
| Domain | `Student`, `Course`, field validation, the seat rules | Import Flask or `sqlite3` |

**Request flow, `POST /courses/CSE3102/enrollments`:** the middleware assigns a request ID; the route
calls `CourseService.enroll`; the service loads the course and student from the repositories;
`Course.check_can_enroll` raises `Conflict` if the student is already enrolled or no seats are left;
the error handler turns `Conflict` into a `409 application/problem+json` response.

**Wiring:** every repository and service is created once in `create_app` and passed in through its
constructor, so tests can build services directly and storage can be changed by editing only
`repositories/`.

**Errors:** every failure uses the RFC 9457 format, including framework errors such as an unknown URL
(404) or a wrong method (405, with an `Allow` header). Unexpected errors return a generic 500; the
stack trace goes only to the log.

**Logging:** one line per request (method, path, status, request ID) plus service events such as
`student enrolled`. Send `X-Request-ID` to use your own ID; it is echoed back in the response.

## Endpoints

| Method | URL | Body | Success | Failures |
|---|---|---|---|---|
| POST | `/students` | `{"studentId":1630,"name":"Rihan","major":"EEE"}` | 201 + `Location` | 400, 409 ID exists, 422 |
| GET | `/students?major=CSE` | | 200 `{"items":[...]}` | 400 unknown filter |
| GET | `/students/{studentId}` | | 200 | 404 |
| PUT | `/students/{studentId}` | `{"name":"Rihan","major":"CSE"}` | 200 | 400, 404, 422 |
| DELETE | `/students/{studentId}` | | 204 | 404, 409 still enrolled |
| POST | `/courses` | `{"code":"CSE3102","title":"Web Technology Lab","seats":40}` | 201 + `Location` | 400, 409 code exists, 422 |
| GET | `/courses` | | 200 `{"items":[...]}` | 400 unknown filter |
| GET | `/courses/{code}` | | 200 | 404 |
| PUT | `/courses/{code}` | `{"title":"Web Tech","seats":30}` | 200 | 400, 404, 409 seats below enrolled, 422 |
| DELETE | `/courses/{code}` | | 204 | 404, 409 has enrollments |
| POST | `/courses/{code}/enrollments` | `{"studentId":1630}` | 201 + `Location` | 400, 404 course, 409 already enrolled, 409 full, 422 unknown student |
| GET | `/courses/{code}/enrollments` | | 200 `{"items":[...]}` | 404 |
| GET | `/courses/{code}/enrollments/{studentId}` | | 200 | 404 |
| DELETE | `/courses/{code}/enrollments/{studentId}` | | 204 | 404 |

All request bodies are JSON (`Content-Type: application/json`). Error example:

```json
{
  "type": "/problems/conflict",
  "title": "Request conflicts with current state",
  "status": 409,
  "detail": "No seats left in this course",
  "requestId": "8cf71b17aef7"
}
```

## Known limitation

The seat check and the insert are two separate steps. If two requests ask for the last seat at the
same moment, both could pass the check. A duplicate enrollment is still impossible because
`(course_code, student_id)` is the primary key.

## AI-use disclosure

<!-- Fill this in with what you used and what you verified yourself. -->
