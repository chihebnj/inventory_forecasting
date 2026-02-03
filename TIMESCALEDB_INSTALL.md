# TimescaleDB Installation Guide for Windows

## Option 1: Docker (Recommended - Easiest)

1. **Start Docker Desktop** (if not already running)

2. **Run TimescaleDB container:**
   ```powershell
   docker run -d --name timescaledb `
     -e POSTGRES_USER=HAZEM `
     -e POSTGRES_PASSWORD=guest `
     -e POSTGRES_DB=inventory_db `
     -p 5432:5432 `
     timescale/timescaledb:latest-pg18
   ```

3. **Update your Django settings.py** to point to the Docker container:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'inventory_db',
           'USER': 'HAZEM',
           'PASSWORD': 'guest',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

## Option 2: Install TimescaleDB Extension on Existing PostgreSQL

For PostgreSQL 18.1 on Windows:

1. **Download TimescaleDB for Windows:**
   - Visit: https://docs.timescale.com/install/latest/self-hosted/installation-windows/
   - Download the Windows installer for PostgreSQL 18

2. **Run the installer** and follow the installation wizard

3. **Restart PostgreSQL service:**
   ```powershell
   # Stop PostgreSQL
   net stop postgresql-x64-18
   
   # Start PostgreSQL
   net start postgresql-x64-18
   ```

## Option 3: Using WSL (Windows Subsystem for Linux)

If you have WSL installed:

1. **Open WSL terminal** (Ubuntu)

2. **Install PostgreSQL and TimescaleDB:**
   ```bash
   sudo apt update
   sudo apt install postgresql-18 postgresql-18-timescaledb
   ```

3. **Configure PostgreSQL** in WSL to match your settings

## After Installation

Once TimescaleDB is installed, run the Django management command:

```powershell
python manage.py setup_timescaledb
```

This will:
- Create the TimescaleDB extension in your database
- Convert `inventory_saleshistory` table to a hypertable (after you create the model and run migrations)

## Manual SQL (Alternative)

If you prefer to run SQL manually:

```sql
-- Connect to your database
psql -U HAZEM -d inventory_db

-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Convert table to hypertable (after migrations)
SELECT create_hypertable('inventory_saleshistory', 'timestamp');
```

## Verify Installation

Check if TimescaleDB is installed:

```sql
SELECT * FROM pg_extension WHERE extname = 'timescaledb';
```
