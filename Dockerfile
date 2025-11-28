FROM postgres:16-alpine

# Set environment variables for PostgreSQL
ENV POSTGRES_USER=api_user
ENV POSTGRES_PASSWORD=api_password
ENV POSTGRES_DB=api_summarization

# Copy initialization scripts if needed
# COPY ./init-scripts/ /docker-entrypoint-initdb.d/

# Expose PostgreSQL port
EXPOSE 5432

# The official postgres image handles the rest

