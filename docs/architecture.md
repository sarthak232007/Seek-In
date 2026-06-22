# Seek-IN — Technical Documentation

**Team Binaries** — Sarthak Dixit (Team Lead), Shreyansh Singh

---

## 1. Problem

Non-technical business stakeholders depend entirely on data engineers to query company databases, since doing so requires writing SQL. This creates delays of hours or days for even simple business questions. At the same time, existing AI-powered query tools typically send the real database schema — including sensitive column names like `salary` or `ssn` — directly to an external AI service, which is a real security risk for any business handling sensitive data.

## 2. Solution overview

Seek-IN lets a business stakeholder ask a question in plain English and get an answer pulled from their real database, while the schema structure itself is never exposed to the AI provider.

The system is built as five cooperating layers, each in its own file, each independently testable:

| Layer | File | Responsibility |
|---|---|---|
| Schema obfuscation | `obfuscation.py` | Converts real table/column names to meaningless aliases, and reverses this conversion |
| NL-to-SQL engine | `nl_to_sql.py` | Sends the question + aliased schema to an AI model, gets back a SQL query written using only fake names |
| Safety validator | `validator.py` | Confirms the generated SQL is a read-only `SELECT` statement before it ever touches the real database |
| Database layer | `db.py` | Executes the validated, real SQL against MySQL |
| Insight generator | `insight_generator.py` | Converts raw query results into a plain-English answer |

`app.py` (Flask) wires these together into a single request/response flow.

## 3. Request flow

1. User submits a question through the frontend chat interface.
2. `nl_to_sql.py` builds a schema description using only fake names (e.g. `table_A`, `col_A2`) and sends it, along with the question, to the AI model.
3. The AI returns a SQL query written entirely in terms of fake names — it has no knowledge of what `table_A` or `col_A2` actually represent.
4. `obfuscation.py`'s `fake_to_real()` function converts the fake names in that query back to the real schema names.
5. `validator.py` checks the now-real SQL query against a safety policy: it must start with `SELECT`, and must not contain dangerous keywords (`DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, etc.) or multiple chained statements.
6. If safe, `db.py` executes the query against the real MySQL database and returns the raw result rows.
7. `insight_generator.py` sends those raw rows back to the AI model, asking for a short, plain-English answer.
8. The answer is returned to the frontend and displayed to the user.

At every step where the AI model is involved (steps 2 and 7), it only ever sees disguised schema names or raw, decontextualized result rows — never the real table/column structure of the business's database.

## 4. Why schema obfuscation, specifically

Most natural-language-to-SQL tools send the real database schema directly to the AI provider as part of the prompt. This means a third-party AI service (and its servers, logs, and any human review processes) gains full knowledge of a business's internal data structure, including sensitive field names.

Seek-IN's obfuscation layer means the AI model only ever interacts with meaningless identifiers. Even if those identifiers were somehow leaked or logged by the AI provider, they reveal nothing about the real business's data structure, since the alias mapping exists only on Seek-IN's own server.

## 5. Technology choices and reasoning

- **Python + Flask** — chosen for simplicity and fast iteration; Flask's minimal routing was sufficient for this single-endpoint prototype.
- **MySQL** — a standard relational database, representative of what most real businesses already use.
- **Groq (Llama 3.3 70B)** — chosen over Gemini after encountering Gemini's currently very low free-tier daily request limit (20 requests/day at time of writing), which was unsuitable for live demo conditions. Groq's free tier offers a substantially higher daily allowance and uses an OpenAI-compatible API format.
- **Plain HTML/CSS/JS frontend** — chosen to keep the prototype simple and fast to build, given the team's primary backend focus for this round. No frontend framework was required for the scope of this prototype.

## 6. Safety validation details

The validator (`validator.py`) enforces three rules on every generated query before execution:

1. The query must start with `SELECT`.
2. The query must not contain any of: `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`, `CREATE`, `GRANT`, `REVOKE`, `EXEC`, or SQL comment markers (`--`, `/*`).
3. The query must not contain multiple chained statements separated by a semicolon.

This is a defense-in-depth measure: even though the AI is explicitly instructed to only generate `SELECT` statements, the validator does not trust AI output blindly before it reaches the real database.

## 7. Current limitations and production roadmap

This is a hackathon-stage prototype. The following are known simplifications, along with what a production version would change:

| Current approach | Limitation | Production improvement |
|---|---|---|
| `schema_config.json` is manually written | Does not scale to large or arbitrary databases | Auto-generate the alias map by reading the database's schema directly (e.g. via MySQL's `INFORMATION_SCHEMA`) |
| Obfuscation uses text replacement on the SQL string | Can behave incorrectly if the same column name exists in multiple tables (e.g. `name` in both `customers` and `products`) | Use a proper SQL parser (e.g. `sqlglot`) to perform structurally-aware replacement instead of plain text substitution |
| Single shared demo database | Does not reflect a real multi-tenant deployment | Each business would connect their own existing database; Seek-IN would not store, copy, or share data across businesses |
| Free-tier AI usage | Lower rate limits, and free-tier usage terms may allow provider review of prompts | A production deployment would move to a paid AI tier for higher throughput guarantees and stronger data-privacy terms |

## 8. Cost considerations

Based on Groq and Gemini's published per-token pricing, a single query (schema description + question, plus a second call to summarize results) costs a small fraction of a cent. At an estimated 2,000 queries/day for a large business, projected AI cost remains under roughly ₹1,300/month — substantially less than the cost of a dedicated data analyst or a commercial BI tool subscription.