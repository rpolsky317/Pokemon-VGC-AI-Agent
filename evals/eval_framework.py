import json

from evals.eval_models import (
    EvalResult,
    ToolAssertionResult,
    ArgumentAssertionResult
)


# ============================================================
# EVAL CONTEXT
# ============================================================

class EvalContext:

    def __init__(
        self,
        agents,
        response
    ):
        self.agents = agents
        self.response = response


    def get_agent(
        self,
        agent_name
    ):
        agent = self.agents.get(
            agent_name
        )

        if agent is None:
            raise ValueError(
                f"Unknown agent: {agent_name}. "
                f"Available agents: "
                f"{list(self.agents.keys())}"
            )

        return agent


    def get_tool_calls(
        self,
        agent_name
    ):
        agent = self.get_agent(
            agent_name
        )

        return getattr(
            agent,
            "tool_call_history",
            []
        )


    def first_call_to(
        self,
        tool_name,
        agent_name
    ):
        tool_calls = self.get_tool_calls(
            agent_name
        )

        for call in tool_calls:

            if call["name"] != tool_name:
                continue

            arguments = call.get(
                "arguments",
                {}
            )

            if isinstance(
                arguments,
                str
            ):
                arguments = json.loads(
                    arguments
                )

            return arguments

        return None
    
    def print(self):

        status = "PASS" if self.passed else "FAIL"

        print(
            f"Overall test result for: "
            f"{self.name}: {status}"
        )

        for tool in self.tool_assertions:

            status = "PASS" if tool.overall_passed else "FAIL"

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
    
class ToolAssertion:

    def __init__(
        self,
        context,
        tool_name,
        agent_name
    ):
        self.context = context
        self.tool_name = tool_name
        self.agent_name = agent_name

        self.argument_assertions = []


    def with_argument(
        self,
        path,
        expected
    ):
        self.argument_assertions.append(
            (
                path,
                expected
            )
        )

        return self


    def evaluate(self):

        arguments = self.context.first_call_to(
            tool_name=self.tool_name,
            agent_name=self.agent_name
        )

        # --------------------------------------------------
        # Tool was not called
        # --------------------------------------------------

        if arguments is None:

            return ToolAssertionResult(
                tool_name=self.tool_name,
                agent_name=self.agent_name,
                passed=False,
                reason=(
                    f"{self.tool_name} tool was not called "
                    f"by {self.agent_name} agent"
                )
            )


        # --------------------------------------------------
        # Tool was called
        # --------------------------------------------------

        argument_results = []

        for path, expected in self.argument_assertions:

            actual = self._get_path(
                arguments,
                path
            )

            path_string = ".".join(
                path
            )

            # --------------------------------------------------
            # Compare values
            # --------------------------------------------------

            if isinstance(actual, str) and isinstance(expected, str):
                passed = (
                    actual.casefold()
                    ==
                    expected.casefold()
                )

            elif isinstance(actual, list) and isinstance(expected, list):

                passed = (
                    {
                        item.casefold()
                        if isinstance(item, str)
                        else item
                        for item in actual
                    }
                    ==
                    {
                        item.casefold()
                        if isinstance(item, str)
                        else item
                        for item in expected
                    }
                )

            else:

                passed = actual == expected


            # --------------------------------------------------
            # Build result
            # --------------------------------------------------

            reason = (
                f"'{self.tool_name}' argument "
                f"{path_string} was expected "
                f"{expected!r}, and was {actual!r}."
            )


            argument_results.append(
                ArgumentAssertionResult(
                    path=path,
                    passed=passed,
                    reason=reason
                )
            )


        return ToolAssertionResult(
            tool_name=self.tool_name,
            agent_name=self.agent_name,
            passed=True,
            reason=(
                f"{self.tool_name} tool was called "
                f"by {self.agent_name} agent"
            ),
            arguments=argument_results
        )


    @staticmethod
    def _get_path(
        data,
        path
    ):

        current = data

        for key in path:

            if not isinstance(
                current,
                dict
            ):
                return None

            if key not in current:
                return None

            current = current[key]

        return current

class EvalAssertions:

    def __init__(
        self,
        context
    ):
        self.context = context

        self.tool_assertions = []


    def tool_was_called(
        self,
        tool_name,
        agent_name="orchestrator"
    ):

        assertion = ToolAssertion(
            context=self.context,
            tool_name=tool_name,
            agent_name=agent_name
        )

        self.tool_assertions.append(
            assertion
        )

        return assertion


    def evaluate(
        self,
        name
    ):

        results = [
            assertion.evaluate()
            for assertion
            in self.tool_assertions
        ]

        passed = all(
            result.overall_passed
            for result
            in results
        )

        return EvalResult(
            name=name,
            passed=passed,
            tool_assertions=results
        )