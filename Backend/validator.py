
DANGEROUS_KEYWORDS = [
    "DROP", "DELETE", "UPDATE", "INSERT", "ALTER",
    "TRUNCATE", "CREATE", "GRANT", "REVOKE", "EXEC",
    "--", ";--", "/*"
    
]


def is_query_safe(sql_query):
    """
    Checks whether a SQL query is safe to run.
    Returns (True, "") if safe.
    Returns (False, "reason") if NOT safe -- the reason explains why,
    which is useful to show in logs or error messages.
    """

   
    query_upper = sql_query.upper().strip()

 
    if not query_upper.startswith("SELECT"):
        return False, "Query does not start with SELECT -- rejected."

   
    for keyword in DANGEROUS_KEYWORDS:
        if keyword in query_upper:
            return False, f"Dangerous keyword '{keyword}' found -- rejected."

   
    query_without_trailing_semicolon = query_upper.rstrip(";").rstrip()
    if ";" in query_without_trailing_semicolon:
        return False, "Multiple statements detected -- rejected."

    
    return True, ""



if __name__ == "__main__":
    test_queries = [
        "SELECT name FROM customers WHERE city = 'Lucknow'",       
        "DROP TABLE customers",                                     
        "SELECT * FROM customers; DELETE FROM customers;",         
        "DELETE FROM orders WHERE order_id = 1",          
        "SELECT name FROM customers;",                          
    ]

    for query in test_queries:
        safe, reason = is_query_safe(query)
        status = "SAFE" if safe else "BLOCKED"
        print(f"[{status}] {query}")
        if not safe:
            print(f"    Reason: {reason}")