
from google.adk.agents import Agent
from google.adk.agents import SequentialAgent, ParallelAgent, LoopAgent
from google.adk.tools import exit_loop


MODEL = "gemini-3.5-flash-lite"


coordinator = Agent(
    name="coordinator",
    model=MODEL,
    description="Understands the student's study-planning request.",
    instruction=(
        "Read the student's request and identify all five required inputs: "
        "subject, days until exam, current level, topics, and available "
        "study hours per day. Preserve the exact values supplied. "
        "If any input is missing, explicitly list the missing information "
        "and do not invent values. If all inputs are present, summarize "
        "them clearly for the downstream agents."
    ),
    output_key="student_request",
)


planning_agent = Agent(
    name="planning_agent",
    model=MODEL,
    description="Prepares the study-planning requirements.",
    instruction=(
        "Use the student's request: {student_request}. "
        "Prepare a concise planning brief for the Topic, Practice, "
        "and Schedule agents. Include constraints, priorities, and "
        "the available study time. Flag any missing information."
    ),
    output_key="planning_context",
)



topic_agent = Agent(
    name="topic_agent",
    model=MODEL,
    description="Prioritizes topics for the student's exam.",
    instruction=(
        "Using {planning_context}, analyze every topic supplied by the student. "
        "For each topic, provide: "
        "1. Priority: High, Medium, or Low. "
        "2. Difficulty level with a brief explanation. "
        "3. Recommended study focus. "
        "Do not omit any supplied topics or invent syllabus topics. "
        "Keep recommendations appropriate to the student's current level "
        "and time remaining before the exam."
    ),
    output_key="topic_results",
)


practice_agent = Agent(
    name="practice_agent",
    model=MODEL,
    description="Creates practice activities for exam preparation.",
   instruction=(
        "Using {planning_context}, create a realistic practice plan for "
        "every topic supplied by the student. For each topic, recommend "
        "a reasonable number of problems and specify suitable practice "
        "types, including concept questions, coding problems, or mixed "
        "practice as appropriate. Include a mock test when feasible. "
        "Keep the workload realistic for the available study time. "
        "Do not omit any supplied topics."
    ),
    output_key="practice_results",
)


schedule_agent = Agent(
    name="schedule_agent",
    model=MODEL,
    description="Creates a realistic study timetable.",
    instruction=(
        "Using {planning_context}, create a day-by-day schedule. "
        "Respect the available study hours and days remaining. "
        "Include breaks, practice, revision, and final-day review. "
        "Do not allocate more study time than the student has."
    ),
    output_key="schedule_results",
)


parallel_agents = ParallelAgent(
    name="parallel_study_tasks",
    sub_agents=[
        topic_agent,
        practice_agent,
        schedule_agent,
    ],
)



study_plan_writer = Agent(
    name="study_plan_writer",
    model=MODEL,
    description="Combines the specialist outputs into one study plan.",
    instruction=(
        "Create one complete, personalized study plan using these results:\n"
        "Topic analysis: {topic_results}\n"
        "Practice plan: {practice_results}\n"
        "Schedule: {schedule_results}\n"
        "Include all of the following:\n"
        "1. A clear day-by-day schedule.\n"
        "2. Every supplied topic and its study focus.\n"
        "3. Specific practice tasks and problem counts.\n"
        "4. Revision activities throughout the plan.\n"
        "5. A mock test or suitable final preparation activities.\n"
        "Respect the student's level, exam deadline, and available "
        "study hours. Make sure the practice workload fits the schedule. "
        "Return the complete study plan, not an outline."
    ),
    output_key="draft_study_plan",
)



review_agent = Agent(
    name="review_agent",
    model=MODEL,
    description="Reviews the draft study plan against the requirements.",
    instruction=(
        "Review the study plan in {draft_study_plan} against the "
        "student requirements in {student_request}. Check all of these: "
        "1. Every supplied topic is covered. "
        "2. Daily and total study hours fit the student's availability. "
        "3. The schedule fits the days remaining until the exam. "
        "4. Practice questions or exercises are included. "
        "5. Revision is included. "
        "6. The final day has an appropriate workload and review. "
        "Identify specific problems and required corrections. "
        "If every criterion passes, call exit_loop. "
        "If any criterion fails, provide concise, actionable feedback "
        "for the revision agent and do not call exit_loop. "
        "Never approve a plan merely because it looks reasonable."
    ),
    tools=[exit_loop],
    output_key="study_plan_review",
)



revision_agent = Agent(
    name="revision_agent",
    model=MODEL,
    description="Improves a study plan using reviewer feedback.",
    instruction=(
        "Revise {draft_study_plan} using {study_plan_review}. "
        "Correct every issue identified by the reviewer. Preserve "
        "the subject, topics, available hours, and exam deadline. "
        "Return the complete revised study plan, including a "
        "day-by-day schedule, practice, and revision. "
        "Do not return only a list of changes."
        "Make the revised plan satisfy every review criterion, "
        "and preserve the student's original constraints exactly. "
    ),
    output_key="draft_study_plan",
)


review_loop = LoopAgent(
    name="review_loop",
    sub_agents=[review_agent, revision_agent],
    max_iterations=2,
)


root_agent = SequentialAgent(
    name="smart_study",
    sub_agents=[
        coordinator,
        planning_agent,
        parallel_agents,
        study_plan_writer,
        review_loop,
    ],
)
