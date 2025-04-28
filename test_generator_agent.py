import os
import json
from typing import List, Dict, Any
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
from test_tools import TestTools

class TestGeneratorAgent:
    def __init__(self):
        load_dotenv()
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0
        )
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.test_tools = TestTools()
        
        # Create the agent with a detailed system prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an AI testing expert that helps generate and execute test cases.
            Your goal is to ensure comprehensive testing of code with high coverage and quality.
            
            You should:
            1. Think carefully about what needs to be tested
            2. Analyze code structure and dependencies
            3. Generate appropriate test cases
            4. Execute tests and analyze results
            5. Provide detailed reports and suggestions
            
            Always consider:
            - Code complexity and edge cases
            - Dependencies and interactions
            - Error handling and edge cases
            - Performance implications
            - Best practices in software testing
            
            Make decisions based on:
            - Test results and coverage
            - Code analysis
            - Previous test outcomes
            - Best practices in software testing"""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        self.agent = create_openai_functions_agent(self.llm, self.test_tools.get_tools(), prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.test_tools.get_tools(),
            memory=self.memory,
            verbose=True
        )

    def run(self, directory: str):
        """Main method to run the test generation and execution process."""
        # Let the agent think and decide what to do
        initial_prompt = f"""I need you to help test the code in the directory: {directory}
        
        Please:
        1. Analyze the codebase
        2. Generate appropriate tests
        3. Execute the tests
        4. Provide a comprehensive report
        
        Think carefully about your approach and make decisions based on what you find."""
        
        try:
            # Let the agent execute its plan
            result = self.agent_executor.invoke({"input": initial_prompt})
            
            # Save the final report
            with open("test_execution_report.txt", "w") as f:
                f.write(result["output"])
            
            return result["output"]
        except Exception as e:
            print(f"\nError during agent execution: {str(e)}")
            print(f"Error type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            raise

if __name__ == "__main__":
    agent = TestGeneratorAgent()
    agent.run("./src") 