FROM python:3.11.6-slim-bullseye as python

# Set the working directory
WORKDIR /app

# Environment variable to ensure output is sent directly to terminal (stdout)
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Copy the requirements file
COPY ./requirements.txt .

# Update package list and install necessary system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python-dev \
    libpq-dev \
    postgresql-client \
    postgresql \
    postgresql-contrib \
    postgis \
    wget \
    # wkhtmltopdf \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    --no-install-recommends && \
    # Install GDAL
    # binutils \
    # libproj-dev \
    # python-gdal python3-gdal \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Install Python packages
RUN pip install --upgrade pip \
    pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Copy wait-for-it script
# COPY wait-for-it.sh /app/wait-for-it.sh
# RUN chmod +x /app/wait-for-it.sh
# Command to run the application

# CMD ["./wait-for-it.sh", "db:5432", "--", "gunicorn", "CORE.wsgi:application", "--bind", "0.0.0.0:8000"]
