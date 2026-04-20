# ticket_management
Easy management of support tickets for businesses

## How to run:

### 1. Configure Environment Variables
Create a .env file in the root directory.

```env

# Database config

DB_HOST=db
DB_PORT=3306
DB_NAME=ticket_system
DB_USER=(user)
DB_PASS=(pass)

# Email config

MAIL_HOST=imap.gmail.com
MAIL_PORT=993
SMTP=smtp.gmail.com
EMAIL=(email)@gmail.com
PASS=(app pass)

# Application Settings

DEBUG=True
OLLAMA_HOST=host.docker.internal
```

### 2. Start with Docker
docker-compose up --build

The application will be at [http://localhost:8000](http://localhost:8000).

### 3. Create a Superuser
docker exec -it ticket_web python manage.py createsuperuser

### 4. Important information:
To make the ticket routing work, you will need to fill the database for the employee language and the language table via the admin panel. These are empty by default in the environment. Additionally, ticket routing is done through Ollama, a local LLM.