# REST service to view the salary and the date of the next raise
This repository contains an implementation of a REST service that allows you to view the current salary and date of the next raise for each
#
### Technologies.
The service is implemented using asynchronous database connections using SQLAlchemy and Asyncpg. Asynchronous pytest is also used to write tests. Registration and authorization is implemented using the [`fastapi_users`](https://fastapi-users.github.io/fastapi-users/12.0/) library.
#
### Installation and Startup
1. Clone the repository:
    ```sh
    git clone git@github.com:nnnLik/salary-viewer-service.git
    ```
2. Navigate to the project directory:
    ```sh
    cd shift-ml-testtask
    ```
3. Create .env.db and env.server. You will find the variables in the .env.example file.

4. Run the service and database in Docker with Docker Compose:
    ```sh
    docker-compose up --build
    ```
5. After a successful start, the service will be available at:
    ```
    http://localhost:8888
    ```
#
### API documentation
Documentation on the service's API is available at:
```
http://localhost:8888/docs
```
#
##### __User Registration__
You must register a user to access salary information and the date of the next raise. Send a `POST` request to the `/auth/jwt/register` endpoint with the following data in the body of the request:
```json
{
  "email": "example@example.com",
  "password": "secret",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```
##### __Create post__
To create a position, send a `POST` query to the `/position/positions` endpoint. Pass the following data in the body of the request:
```json
{
  "id": 1,
  "name": "front end developer",
  "base_salary": 600
}
```
##### __Filling in user information__
After successful registration, fill in the user information by sending a `POST` query to endpoint `/employee/info`. In the header of the request specify the authorization token:
```
Authorization: Bearer <token>
```
Pass the following data in the body of the request:
```json
{
  "first_name'': "Big",
  "last_name'': "Dude",
  "birth_year": 1900,
  "position_id": 1
}
```
##### __Get Salary Information__
To get salary information and the date of the next raise, send a `GET` query to the `/employee/salary` endpoint. Specify the authorization token in the header of the request:
```
Authorization: Bearer <token>
```

In response you will get the following:
```json
{
  "id": int,
  "first_name": str,
  "last_name": str,
  "birth_year": int,
  "employment_date": str,
  "position": str,
  "employee_id": str,
  "salary": int,
  "next_increase_date": str,
  "days_until_increase": int.
}
```
#
### Tests:
1. To run the test you will need to install all the dependencies:
    ```sh
    poetry install
    ```
2. To run the Tests:
    ```sh
    pytest -vv tests/
    ```

### TODO:
* Data fixtures
* Admin
