-- swich to an appropriate role to create user and role
USE ROLE USERADMIN; 

-- create dlt user
CREATE USER extract_loader
    PASSWORD = 'a1234b5678'
    DEFAULT_WAREHOUSE = DEV_WH;

-- create dlt role
-- (optional)drop role if there is any
DROP ROLE movies_dlt_role;
CREATE ROLE movies_dlt_role;

-- switch to an appropriate role to grant privileges to role & grant role to user
USE ROLE SECURITYADMIN;

-- grant role to user
GRANT ROLE movies_dlt_role TO USER extract_loader;

-- grant privileges to role
-- this role needs to use warehouse, db, schema
GRANT USAGE ON WAREHOUSE dev_wh TO ROLE movies_dlt_role;
GRANT USAGE ON DATABASE movies TO ROLE movies_dlt_role;
GRANT USAGE ON SCHEMA movies.staging to ROLE movies_dlt_role;


-- this role needs some special usages for the db and scheme
GRANT CREATE TABLE ON SCHEMA movies.staging TO ROLE movies_dlt_role;
GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA movies.staging TO ROLE movies_dlt_role;
GRANT INSERT, UPDATE, DELETE ON FUTURE TABLES IN SCHEMA movies.staging TO ROLE movies_dlt_role;

-- check grants
SHOW GRANTS TO ROLE movies_dlt_role;