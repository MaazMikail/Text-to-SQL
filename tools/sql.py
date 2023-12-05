import sqlite3
from langchain.tools import Tool
from pydantic import BaseModel
from typing import List

conn = sqlite3.connect("db.sqlite")

def list_tables():
    c = conn.cursor()
    rows = c.execute("SELECT name from sqlite_master where type='table';").fetchall()
    return "\n".join(row[0] for row in rows if row[0] is not None)

def run_sqlite_query(query):
    c= conn.cursor()

    try:
        c.execute(query)
        return c.fetchall()
    except sqlite3.OperationalError as err:
        return f"The following error occured: {str(err)}"
    
class RunQueryArgsSchema(BaseModel):
    query: str

run_query_tool = Tool.from_function(
        func=run_sqlite_query,
        name="run_sqlite_query",
        description="Run a sqlite query.",
        args_schema=RunQueryArgsSchema

)


def describe_tables(table_names):
    c = conn.cursor()
    tables = ', '.join("'" + item + "'" for item in table_names)
    rows = c.execute(f"select sql from sqlite_master where type='table' and name in ({tables});")
    return '\n'.join(row[0] for row in rows if row[0] is not None)

class DescribeTablesArgsSchema(BaseModel):
    query: List[str]

describe_table_tool = Tool.from_function(

            func=describe_tables,
            name='describe_tables',
            description="Given a list of table names, return the schema",
            args_schema=DescribeTablesArgsSchema
)