# Docker PostgreSQL Setup

This project includes Docker configuration for running PostgreSQL.

## Quick Start

### Using Docker Compose (Recommended)

1. Start PostgreSQL:
```bash
docker-compose up -d postgres
```

2. Check if PostgreSQL is running:
```bash
docker-compose ps
```

3. View logs:
```bash
docker-compose logs -f postgres
```

4. Stop PostgreSQL:
```bash
docker-compose down
```

5. Stop and remove volumes (deletes all data):
```bash
docker-compose down -v
```

### Using Docker Directly

1. Build the image:
```bash
docker build -f Dockerfile -t api_summarization_postgres .
```

2. Run the container:
```bash
docker run -d \
  --name api_summarization_postgres \
  -e POSTGRES_USER=api_user \
  -e POSTGRES_PASSWORD=api_password \
  -e POSTGRES_DB=api_summarization \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  api_summarization_postgres
```

3. Stop the container:
```bash
docker stop api_summarization_postgres
```

4. Remove the container:
```bash
docker rm api_summarization_postgres
```

## Connecting to PostgreSQL

### From Host Machine

```bash
psql -h localhost -p 5432 -U api_user -d api_summarization
```

Password: `api_password`

### From Python/SQLAlchemy

```python
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://api_user:api_password@localhost:5432/api_summarization"
engine = create_engine(DATABASE_URL)
```

### From Docker Container

```bash
docker exec -it api_summarization_postgres psql -U api_user -d api_summarization
```

## Environment Variables

Copy `.env.example` to `.env` and adjust values as needed:

```bash
cp .env.example .env
```

## Database Initialization Scripts

To run SQL scripts on database initialization, create an `init-scripts` directory and place your `.sql` or `.sh` files there. Then uncomment the relevant lines in `Dockerfile.postgres` and `docker-compose.yml`.

Example:
```bash
mkdir init-scripts
echo "CREATE TABLE example (id SERIAL PRIMARY KEY, name VARCHAR(100));" > init-scripts/01-init.sql
```

## Data Persistence

Database data is persisted in a Docker volume named `postgres_data`. This means your data will survive container restarts.

To backup your data:
```bash
docker exec -t api_summarization_postgres pg_dump -U api_user api_summarization > backup.sql
```

To restore from backup:
```bash
docker exec -i api_summarization_postgres psql -U api_user -d api_summarization < backup.sql
```

## Configuration

Default configuration:
- **User**: api_user
- **Password**: api_password
- **Database**: api_summarization
- **Port**: 5432
- **Version**: PostgreSQL 16 (Alpine)

To change these values, edit the environment variables in `docker-compose.yml` or `Dockerfile.postgres`.

## Troubleshooting

### Port already in use

If port 5432 is already in use, change the port mapping in `docker-compose.yml`:
```yaml
ports:
  - "5433:5432"  # Host:Container
```

Then connect using port 5433 on your host machine.

### Permission denied

If you encounter permission issues with volumes, ensure Docker has proper permissions or try:
```bash
docker-compose down -v
docker-compose up -d postgres
```

### Health check failing

Wait a few seconds for PostgreSQL to fully start. You can check the health status:
```bash
docker inspect api_summarization_postgres | grep -A 10 Health
```

