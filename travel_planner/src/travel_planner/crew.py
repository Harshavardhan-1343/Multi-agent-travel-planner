from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from tools.custom_tool import RealTimeFlightTool

# Inside agent definition



@CrewBase
class TravelPlanner():
    """TravelPlanner crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def flight_optimizer(self) -> Agent:
        return Agent(
            config=self.agents_config['flight_optimizer'],  # type: ignore[index]
            verbose=True
            tools=[RealTimeFlightTool()]
        )

    @agent
    def stay_recommender(self) -> Agent:
        return Agent(
            config=self.agents_config['stay_recommender'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def itinerary_curator(self) -> Agent:
        return Agent(
            config=self.agents_config['itinerary_curator'],  # type: ignore[index]
            verbose=True
        )

    @task
    def flight_task(self) -> Task:
        return Task(
            config=self.tasks_config['flight_task'],  # type: ignore[index]
            output_file='flight_options.md'
        )

    @task
    def hotel_task(self) -> Task:
        return Task(
            config=self.tasks_config['hotel_task'],  # type: ignore[index]
            output_file='hotel_recommendations.md'
        )

    @task
    def itinerary_task(self) -> Task:
        return Task(
            config=self.tasks_config['itinerary_task'],  # type: ignore[index]
            output_file='travel_itinerary.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the TravelPlanner crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

