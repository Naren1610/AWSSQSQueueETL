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

# Answering the Questions 

## How would you deploy this application in production?
### Deployment in Production:
1. Containerization:
   - Docker: Containerize the application using Docker. Docker provides a standardized unit of software that packages up the code and all its dependencies, ensuring that the application runs consistently across different environments. This makes it easier to manage and deploy applications in a consistent manner.
2. Orchestration:
   - Kubernetes: Use Kubernetes to manage the deployment, scaling, and operations of the containerized applications. Kubernetes automates the deployment and management of containerized applications, providing features such as load balancing, scaling, and self-healing. It ensures that the application is highly available and can handle increased traffic.
3. CI/CD Pipeline:
   - Continuous Integration and Continuous Deployment (CI/CD): Implement CI/CD pipelines using tools like Jenkins, GitHub Actions, or GitLab CI/CD. CI/CD automates the process of building, testing, and deploying the application, ensuring that changes are continuously integrated and deployed to production. This reduces the risk of errors and ensures that the application is always in a deployable state.

## What other components would you want to add to make this production ready?
### Additional Components for Production Readiness:
1. Monitoring and Logging:
   - Prometheus and Grafana: Integrate monitoring using Prometheus and Grafana to collect and visualize metrics from the application. Prometheus is used for monitoring and alerting, while Grafana provides a dashboard for visualizing the metrics.
   - ELK Stack: Implement logging using the ELK stack (Elasticsearch, Logstash, Kibana). Elasticsearch is used for storing and searching log data, Logstash for processing and transforming log data, and Kibana for visualizing the logs. This helps in identifying and troubleshooting issues in the application.
2. Secrets Management:
   - AWS Secrets Manager or HashiCorp Vault: Use AWS Secrets Manager or HashiCorp Vault for managing sensitive data such as database credentials and API keys. These tools provide a secure way to store and access secrets, ensuring that sensitive data is not hardcoded in the application code.
3. Error Handling and Retries:
   - Robust Error Handling: Implement robust error handling to gracefully handle errors and exceptions in the application. This includes catching exceptions, logging errors, and providing meaningful error messages.
   - Retry Mechanisms: Implement retry mechanisms for operations that can fail temporarily, such as reading messages from the queue and writing to the database. This ensures that transient errors do not cause the application to fail.
4. Data Validation:
   - Validation Logic: Implement data validation to handle inconsistencies such as type mismatches (e.g., `app_version` as a string). This ensures that the data being processed and stored is valid and consistent, preventing errors and data corruption.

## How can this application scale with a growing dataset?
 ### Scaling with Growing Dataset:
1. Auto-scaling:
   - Kubernetes Auto-scaling: Implement auto-scaling policies in Kubernetes based on CPU/memory usage. Kubernetes can automatically scale the application up or down based on resource usage, ensuring that the application can handle increased traffic and load.
2. Sharding and Partitioning:
   - Database Sharding and Partitioning: Use sharding and partitioning techniques in the database to manage large datasets. Sharding involves splitting the data across multiple databases, while partitioning involves dividing the data within a single database. This helps in managing and querying large datasets efficiently.
3. Message Batching:
   - Batch Processing: Process messages in batches to optimize database writes and reduce the number of transactions. Batching messages reduces the overhead of individual transactions and improves the performance of database operations.

## How can PII be recovered later on?
### PII Recovery:
Reversible Masking:
   - Encryption: Use a reversible masking technique such as encryption, where a decryption key can be used to recover the original data if needed. This allows PII to be masked for analysis while still being recoverable if necessary for compliance or other purposes.

## What are the assumptions you made?
### Assumptions Made:
1. Pre-configured Infrastructure:
   - SQS and Postgres: Assumed that the SQS queue and Postgres database are pre-configured and accessible. This means that the necessary infrastructure is already set up and the application can connect to these services without additional configuration.
2. Consistent JSON Structure:
   - Message Format: Assumed that the JSON structure of the messages from the queue is consistent. This means that the messages have a predictable structure, making it easier to process and transform the data.
3. Local Setup:
   - Docker and Docker Compose: Assumed that Docker and Docker Compose are installed and properly configured on the local machine. This is necessary for running the application and its dependencies in a containerized environment.
4. Data Type Adjustment:
   - App Version Column: Assumed that the `app_version` column in the `user_logins` table is initially of type `integer` and needs to be altered to `varchar` to handle the data correctly. This ensures that the application can process and store the `app_version` data as a string.
5. Data Loaded into the Table:
   - Only messages containing device_id and ip fields should be processed and loaded into the table. This ensures that only complete and valid data is inserted into the database, maintaining data integrity and consistency.
    


