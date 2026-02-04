-- 1. Create a Namespace (roughly equivalent to a 'Cluster' or 'Project')
DEFINE NAMESPACE sage_ns;

-- 2. Switch to that Namespace
USE NAMESPACE sage_ns;

-- 3. Create a Database within the Namespace
DEFINE DATABASE sage_db;

-- 4. Switch to that Database
USE DATABASE sage_db;

-- 5. Create a Root User for this Database (Equivalent to granting full privileges on the DB)
-- This user can ONLY access this specific database (sage_db) in this namespace (sage_ns)
DEFINE USER sage ON DATABASE PASSWORD 'pass' ROLES OWNER;

-- OPTIONAL: If you want a user that can access the whole namespace:
-- DEFINE USER sage_admin ON NAMESPACE PASSWORD 'pass' ROLES OWNER;

-- 6. (Optional) Define a Scope for Application Users (e.g. End Users like Students/Teachers)
-- This allows users to sign up/in tightly coupled to the DB.
-- DEFINE SCOPE user_scope SESSION 24h
--    SIGNUP ( CREATE user SET email = $email, pass = crypto::argon2::generate($pass) )
--    SIGNIN ( SELECT * FROM user WHERE email = $email AND crypto::argon2::compare(pass, $pass) );
