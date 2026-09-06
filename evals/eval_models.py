from dataclasses import dataclass, field


@dataclass
class ArgumentAssertionResult:
    path: list[str]
    passed: bool
    reason: str


@dataclass
class ToolAssertionResult:
    tool_name: str
    passed: bool
    reason: str
    arguments: list[ArgumentAssertionResult] = field(
        default_factory=list
    )

    @property
    def overall_passed(self):
        if not self.passed:
            return False

        return all(
            argument.passed
            for argument in self.arguments
        )


@dataclass
class EvalResult:
    name: str
    passed: bool
    tool_assertions: list["ToolAssertionResult"]

    def print(self):

        status = "PASS" if self.passed else "FAIL"

        print(
            f"Overall test result for: "
            f"{self.name}: {status}"
        )

        for tool in self.tool_assertions:

            status = (
                "PASS"
                if tool.overall_passed
                else "FAIL"
            )

            print(
                f"- {status}: {tool.reason}"
            )

            for argument in tool.arguments:

                status = (
                    "PASS"
                    if argument.passed
                    else "FAIL"
                )

                print(
                    f"    - {status}: "
                    f"{argument.reason}"
                )