# ============================================
# validator.py
#
# This is our safety net. Even though we INSTRUCT Gemini to only write
# SELECT statements, AI models can sometimes make mistakes or be tricked
# by unusual questions. We never trust AI output blindly when it's about
# to touch a real database -- we verify it ourselves in code.
#
# Think of this like input validation/sanitization in Express before
# saving anything to MongoDB -- same defensive principle, different layer.
# ============================================

# Words that should NEVER appear in a query we're about to run.
# If any of these show up, we block the query completely.
DANGEROUS_KEYWORDS = [
    "DROP", "DELETE", "UPDATE", "INSERT", "ALTER",
    "TRUNCATE", "CREATE", "GRANT", "REVOKE", "EXEC",
    "--", ";--", "/*"
    # "--" and "/*" are SQL comment markers -- sometimes used in
    # injection attempts to "comment out" the rest of a query.
]


def is_query_safe(sql_query):
    """
    Checks whether a SQL query is safe to run.
    Returns (True, "") if safe.
    Returns (False, "reason") if NOT safe -- the reason explains why,
    which is useful to show in logs or error messages.
    """

    # Convert to uppercase for checking, so we catch "drop", "Drop", "DROP"
    # all the same way. We don't change the original query, just this
    # copy used for checking.
    query_upper = sql_query.upper().strip()

    # Rule 1: The query MUST start with SELECT.
    # This is the single most important rule -- a read-only query
    # should only ever be retrieving data, never changing it.
    if not query_upper.startswith("SELECT"):
        return False, "Query does not start with SELECT -- rejected."

    # Rule 2: Block any dangerous keyword appearing ANYWHERE in the query.
    # Even if it starts with SELECT, a clever/malformed query could try
    # to sneak in multiple statements separated by a semicolon.
    for keyword in DANGEROUS_KEYWORDS:
        if keyword in query_upper:
            return False, f"Dangerous keyword '{keyword}' found -- rejected."

    # Rule 3: Block multiple statements in one query.
    # A safe single SELECT should not contain a semicolon in the middle
    # (only optionally at the very end, which we can ignore).
    # Example of what we're blocking:
    # "SELECT * FROM table_A; DROP TABLE table_A;"
    query_without_trailing_semicolon = query_upper.rstrip(";").rstrip()
    if ";" in query_without_trailing_semicolon:
        return False, "Multiple statements detected -- rejected."

    # If we reach here, none of the danger checks triggered.
    return True, ""


# ----------------------------------------------
# Test block -- only runs when executing this file directly.
# We test with a few queries: one safe, a few dangerous ones,
# to make sure our checks actually catch problems correctly.
# ----------------------------------------------
if __name__ == "__main__":
    test_queries = [
        "SELECT name FROM customers WHERE city = 'Lucknow'",       # safe
        "DROP TABLE customers",                                     # dangerous
        "SELECT * FROM customers; DELETE FROM customers;",          # dangerous
        "DELETE FROM orders WHERE order_id = 1",                    # dangerous
        "SELECT name FROM customers;",                              # safe (trailing ; is fine)
    ]

    for query in test_queries:
        safe, reason = is_query_safe(query)
        status = "SAFE" if safe else "BLOCKED"
        print(f"[{status}] {query}")
        if not safe:
            print(f"    Reason: {reason}")