from typing import AnyStr
from .basetool import *


# Jerry: This tool can be dangerous

class CodeInterpreter:
    def __init__(self, timeout=300):
        self.globals = {}
        self.locals = {}
        self.timeout = timeout

    def execute_code(self, code):
        try:
            # Wrap the code in an eval() call to return the result
            wrapped_code = f"__result__ = eval({repr(code)}, globals(), locals())"
            exec(wrapped_code, self.globals, self.locals)
            return self.locals.get('__result__', None)
        except Exception as e:
            try:
                # If eval fails, attempt to exec the code without returning a result
                exec(code, self.globals, self.locals)
                return "Code executed successfully."
            except Exception as e:
                return f"Error: {str(e)}"

    def reset_session(self):
        self.globals = {}
        self.locals = {}


class PythonCodeInterpreter(BaseTool):
    """Python Code Interpreter Tool"""
    name = "run_python_code"
    description = "A tool to execute Python code and retrieve the command line output. Input should be executable Python code."
    args_schema: Optional[Type[BaseModel]] = create_model("CodeInterpreter", code=(str, ...))
    interpreter = CodeInterpreter()

    def _run(self, code: AnyStr) -> Any:
        return self.interpreter.execute_code(code)

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    tool = PythonCodeInterpreter()
    ans = tool._run("import os\nprint(\"helloworld\")")
    print(ans)
