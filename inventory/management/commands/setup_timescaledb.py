"""
Django management command to set up TimescaleDB extension and create hypertables.

Usage:
    python manage.py setup_timescaledb
"""
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Set up TimescaleDB extension and create hypertables for time-series tables'

    def add_arguments(self, parser):
        parser.add_argument(
            '--table',
            type=str,
            help='Specific table to convert to hypertable (default: all time-series tables)',
        )
        parser.add_argument(
            '--time-column',
            type=str,
            default='timestamp',
            help='Name of the time column (default: timestamp)',
        )

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Enable TimescaleDB extension
            self.stdout.write('Creating TimescaleDB extension...')
            try:
                cursor.execute("CREATE EXTENSION IF NOT EXISTS timescaledb;")
                self.stdout.write(
                    self.style.SUCCESS('[OK] TimescaleDB extension created successfully')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'[ERROR] Failed to create TimescaleDB extension: {e}')
                )
                self.stdout.write(
                    self.style.WARNING(
                        'Make sure TimescaleDB is installed in your PostgreSQL instance.'
                    )
                )
                return

            # Get the table name
            table_name = options.get('table')
            time_column = options.get('time_column')

            if table_name:
                # Convert specific table
                self._create_hypertable(cursor, table_name, time_column)
            else:
                # Convert all time-series tables (SalesHistory)
                tables_to_convert = [
                    ('inventory_saleshistory', 'timestamp'),
                ]

                for table, time_col in tables_to_convert:
                    self._create_hypertable(cursor, table, time_col)

    def _create_hypertable(self, cursor, table_name, time_column):
        """Convert a table to a TimescaleDB hypertable."""
        # Check if table exists
        cursor.execute(
            """
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = %s
            );
            """,
            [table_name],
        )
        table_exists = cursor.fetchone()[0]

        if not table_exists:
            self.stdout.write(
                self.style.WARNING(
                    f'[WARNING] Table {table_name} does not exist. Run migrations first.'
                )
            )
            return

        # Check if already a hypertable
        cursor.execute(
            """
            SELECT EXISTS (
                SELECT FROM timescaledb_information.hypertables 
                WHERE hypertable_name = %s
            );
            """,
            [table_name],
        )
        is_hypertable = cursor.fetchone()[0]

        if is_hypertable:
            self.stdout.write(
                self.style.WARNING(f'[WARNING] Table {table_name} is already a hypertable.')
            )
            return

        # Create hypertable
        self.stdout.write(f'Converting {table_name} to hypertable...')
        try:
            # TimescaleDB requires the time column to be part of a unique constraint
            # If there's a primary key that doesn't include the time column,
            # we need to handle it differently
            cursor.execute(
                f"""
                SELECT create_hypertable(
                    '{table_name}', 
                    '{time_column}',
                    chunk_time_interval => INTERVAL '1 day',
                    if_not_exists => TRUE
                );
                """
            )
            result = cursor.fetchone()[0]
            self.stdout.write(
                self.style.SUCCESS(
                    f'[OK] Successfully converted {table_name} to hypertable'
                )
            )
        except Exception as e:
            error_msg = str(e)
            # If error is about unique index, provide helpful message
            if 'unique index' in error_msg.lower() or 'partitioning' in error_msg.lower():
                self.stdout.write(
                    self.style.ERROR(
                        f'[ERROR] Failed to convert {table_name} to hypertable: {e}'
                    )
                )
                self.stdout.write(
                    self.style.WARNING(
                        '\nSolution: The time column must be part of a unique constraint.\n'
                        'Run this SQL manually to drop the primary key and add a composite unique constraint:\n'
                        f'ALTER TABLE {table_name} DROP CONSTRAINT {table_name}_pkey;\n'
                        f'ALTER TABLE {table_name} ADD CONSTRAINT {table_name}_unique_product_timestamp UNIQUE (product_id, {time_column});\n'
                        'Then run this command again.'
                    )
                )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f'[ERROR] Failed to convert {table_name} to hypertable: {e}'
                    )
                )
