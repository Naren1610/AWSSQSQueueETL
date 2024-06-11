# TakeHomeTest
Data Engineering Take Home: ETL off a SQS Queue
 Data Engineering Take Home: ETL off a SQS Queue

 ## Objective
- Read data from an AWS SQS Queue.
- Mask PII fields in a way people can identify the duplicate values (`device_id` and `ip`).
- Write each record to a Postgres database.

## Setup Instructions

### Prerequisites
1. Ensure Docker and Docker Compose are installed.
    - [Docker Installation Guide](https://docs.docker.com/get-docker/)
    - [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)
2. Clone this repository to your local machine.

### Running the Project
1. Navigate to the project directory:
    ```sh
    cd project-directory
    ```
2. Start the localstack and Postgres services using Docker Compose:
    ```sh
    docker-compose up
    ```
3. Open a new terminal window and run the Python script:
    ```sh
    python3 testScript.py
    ```

### Thought Process
- Reading from SQS: Used boto3 to connect to the SQS queue and read messages.
- Masking PII: Applied SHA-256 hashing to mask `device_id` and `ip` fields.
- Database Insertion: Used psycopg2 to connect to Postgres and insert records.
- Error Handling: Implemented basic error handling and logging.
- Data Type Adjustment: Altered the `user_logins` table to change `app_version` from `integer` to `varchar` to handle string data.


