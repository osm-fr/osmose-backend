-- Allow data loss (but not corruption) in the case of a power outage. This is okay because we need to re-run the script anyways.
SET synchronous_commit TO OFF;

-- Users
\copy users FROM 'users.txt'
