-- NOTE FOR FUTURE REFERENCE: all database changes should be scripted
-- and named accordingly: ACHOO-<ticket-number>.sql
-- For example: ACHOO-#7.sql
-- And then placed in the app/migrate/sql directory
--To execute:
-- navigate to the app/migrate/sql directory and run:
-- psql -h <hostname> -d <database-name> -U <username> -a -q -f ACHOO-<ticket-number>.sql

\connect postgres

ALTER DATABASE allergyalert RENAME TO achoo;
