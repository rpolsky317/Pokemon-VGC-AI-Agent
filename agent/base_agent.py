from openai import OpenAI
import os
from dotenv import load_dotenv
import json

class BaseAgent:

    def __init__(
        self,
        instructions: str,
        tools: list,
        tool_dispatcher
    ):
        
        load_dotenv()

        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        self.instructions = instructions

        self.tools = tools

        self.tool_dispatcher = tool_dispatcher

        self.tool_call_history = []
        


    def run(
        self,
        user_input
    ):

        response = self.client.responses.create(
            model="gpt-5.6",
            input=user_input,
            instructions=self.instructions,
            tools=self.tools
        )

        return self._handle_response(
            response
        )


    def _handle_response(
        self,
        response
    ):

        tool_outputs = []

        for function_call in response.output:

            if function_call.type != "function_call":
                continue

            tool_name = function_call.name

            arguments = json.loads(
                function_call.arguments
            )

            print(
                f"\nCalling tool: {tool_name}"
            )

            print(
                f"Arguments: {arguments}"
            )

            self.tool_call_history.append(
                {
                    "name": tool_name,
                    "arguments": arguments
                }
            )

            result = self.tool_dispatcher.dispatch(
                tool_name,
                arguments
            )

            print(
                f"Tool result: {result!r}"
            )

            serialized_result = (
                self._serialize_tool_result(
                    result
                )
            )

            tool_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": function_call.call_id,
                    "output": str(serialized_result)
                }
            )

        if not tool_outputs:
            return response.output_text

        response = self.client.responses.create(
            model="gpt-5.6",
            input=tool_outputs,
            previous_response_id=response.id,
            instructions=self.instructions,
            tools=self.tools
        )

        return self._handle_response(
            response
        )


    def _serialize_tool_result(
        self,
        result
    ):

        if result is None:
            return ""

        if isinstance(result, str):
            return result

        return json.dumps(
            result,
            default=str
        )


    def _get_final_response(
        self,
        response
    ):

        for item in response.output:

            if item.type != "message":
                continue

            for content in item.content:

                if content.type == "output_text":

                    return content.text

        return ""