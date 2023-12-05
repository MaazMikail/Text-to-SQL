from langchain.tools import StructuredTool
from pydantic import BaseModel

def write_report(filename, html):
    with open(filename, 'w') as f:
        f.write(html)


class WriteReportArgsSchema(BaseModel):
    filename: str
    html: str

html_tool = StructuredTool.from_function(

        func=write_report,
        name="write_report",
        description="Write an HTML file to disk. Use this tool whenever someone asks for HTML output",
        args_schema=WriteReportArgsSchema
)