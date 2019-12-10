# Undo Logging
    Write UNDO logs into a file for a given set of transactions. Do not worry about concurrency on transactions, there will be inconsistencies.
#   Undo Recovery
    Given an input file containing UNDO logs till a crash point, and the current set of database element values, perform a recovery - output the set of database elements and their recovered values
