from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew, before_kickoff, after_kickoff
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Dict, Any
import json

@CrewBase
class TravelPlanningCrew:
    """
    AI Travel Planning Crew that collaboratively creates comprehensive travel plans
    by analyzing budgets, researching destinations, curating experiences, planning
    itineraries, organizing transportation, and managing potential risks.
    """

    agents: List[BaseAgent]
    tasks: List[Task]

    # Paths to your YAML configuration files
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @before_kickoff
    def prepare_inputs(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and prepare inputs before the crew starts execution.
        Ensures all required travel planning parameters are present.
        """
        required_fields = [
            'num_travelers', 'destination_list', 'total_budget', 'trip_duration',
            'travel_dates', 'experience_preferences', 'traveler_flexibility',
            'traveler_interests', 'travel_style', 'cultural_interest_level',
            'traveler_ethics_preference', 'passport_country', 'preferred_platforms'
        ]
        
        # Validate required inputs
        missing_fields = [field for field in required_fields if field not in inputs]
        if missing_fields:
            raise ValueError(f"Missing required inputs: {', '.join(missing_fields)}")
        
        # Add processing timestamp and additional metadata
        inputs['processing_started_at'] = str(datetime.now())
        inputs['crew_version'] = "1.0.0"
        
        # Format destination list if it's a string
        if isinstance(inputs['destination_list'], str):
            inputs['destination_list'] = [dest.strip() for dest in inputs['destination_list'].split(',')]
        
        print(f"🚀 Starting travel planning for {inputs['num_travelers']} travelers")
        print(f"📍 Destinations: {', '.join(inputs['destination_list'])}")
        print(f"💰 Budget: ${inputs['total_budget']}")
        print(f"📅 Duration: {inputs['trip_duration']} days")
        
        return inputs

    @after_kickoff
    def process_output(self, output) -> Any:
        """
        Process and enhance the final output after crew execution.
        Adds summary information and formatting for better presentation.
        """
        # Create a comprehensive travel plan summary
        summary = {
            "plan_generated_at": str(datetime.now()),
            "total_phases_completed": 5,
            "crew_agents_involved": 7,
            "plan_status": "Complete"
        }
        
        # Add summary to the output
        if hasattr(output, 'raw'):
            output.raw += f"\n\n## 📋 Planning Summary\n"
            output.raw += f"- Plan Generated: {summary['plan_generated_at']}\n"
            output.raw += f"- Phases Completed: {summary['total_phases_completed']}\n"
            output.raw += f"- Agents Involved: {summary['crew_agents_involved']}\n"
            output.raw += f"- Status: {summary['plan_status']}\n"
            output.raw += f"\n✅ Your comprehensive travel plan is ready!"
        
        print("🎉 Travel planning completed successfully!")
        return output

    # AGENT DEFINITIONS
    @agent
    def travel_finance_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['Travel Finance Advisor'],
            verbose=True
        )

    @agent
    def travel_intelligence_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['Travel Intelligence Analyst'],
            verbose=True
        )

    @agent
    def destination_research_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['Destination Research Specialist'],
            verbose=True
        )

    @agent
    def cultural_experience_curator(self) -> Agent:
        return Agent(
            config=self.agents_config['Cultural Experience Curator'],
            verbose=True
        )

    @agent
    def itinerary_planning_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['Itinerary Planning Specialist'],
            verbose=True
        )

    @agent
    def transportation_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['Multi-Modal Transportation Strategist'],
            verbose=True
        )

    @agent
    def crisis_management_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['Travel Crisis Management Specialist'],
            verbose=True
        )

    # TASK DEFINITIONS
    @task
    def budget_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config['travel_finance_advisor_task']
        )

    @task
    def pricing_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['travel_intelligence_analyst_task']
        )

    @task
    def destination_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['destination_research_specialist_task']
        )

    @task
    def cultural_curation_task(self) -> Task:
        return Task(
            config=self.tasks_config['cultural_experience_curator_task']
        )

    @task
    def itinerary_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['itinerary_planning_specialist_task']
        )

    @task
    def transportation_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config['transportation_strategist_task']
        )

    @task
    def risk_assessment_task(self) -> Task:
        return Task(
            config=self.tasks_config['travel_crisis_management_task']
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # Automatically collected by @agent decorators
            tasks=self.tasks,    # Automatically collected by @task decorators
            process=Process.sequential,  # Tasks execute in defined order for proper dependencies
            verbose=True,
            memory=True,  # Enable memory for context sharing between agents
            cache=True,   # Cache tool results for efficiency
            max_rpm=100,  # Rate limiting to avoid API issues
            embedder={
                "provider": "openai"  # For memory functionality
            },
            planning=True,  # Enable planning for better task coordination
        )


# HOW TO USE THE CREW
def run_travel_planning(travel_inputs: Dict[str, Any]):
    """
    Execute the travel planning crew with the provided inputs.
    
    Args:
        travel_inputs: Dictionary containing all required travel parameters
    
    Returns:
        Comprehensive travel plan generated by the crew
    """
    try:
        crew_instance = TravelPlanningCrew()
        result = crew_instance.crew().kickoff(inputs=travel_inputs)
        return result
    except Exception as e:
        print(f"Error during travel planning: {str(e)}")
        raise


# EXAMPLE USAGE
if __name__ == "__main__":
    # Example input parameters
    example_inputs = {
        "num_travelers": 2,
        "destination_list": ["Tokyo, Japan", "Kyoto, Japan", "Bangkok, Thailand"],
        "total_budget": 8000,
        "trip_duration": 14,
        "travel_dates": "March 15-29, 2025",
        "experience_preferences": "authentic local culture, food experiences, nature",
        "traveler_flexibility": "moderate - can adjust dates by 2-3 days",
        "traveler_interests": "photography, cooking, hiking, history",
        "travel_style": "mid-range comfort with some luxury experiences",
        "cultural_interest_level": "high - want deep cultural immersion",
        "traveler_ethics_preference": "sustainable and responsible tourism",
        "passport_country": "United States",
        "preferred_platforms": "Expedia, Booking.com, local tour operators"
    }
    
    # Run the travel planning crew
    travel_plan = run_travel_planning(example_inputs)
    print("Travel plan generated successfully!")
    print(travel_plan)