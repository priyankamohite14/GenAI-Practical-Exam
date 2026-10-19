
from datetime import datetime, timedelta
import json

# AI Agent system prompt
system_prompt = """
You are an Academic Assignment Planning Agent.
Create tasks, priorities and deadlines.
Check for missing information and deadline conflicts.
Never assume an unknown deadline.
Update the plan when requirements change.
"""

def create_plan(assignment):
    title = assignment.get("title")
    deadline_text = assignment.get("deadline")
    requirements = assignment.get("requirements", [])

    # Check incomplete information
    if not title or not deadline_text:
        return {
            "status": "INCOMPLETE",
            "message": "Assignment title or deadline is missing."
        }

    try:
        deadline = datetime.strptime(
            deadline_text, "%Y-%m-%d"
        ).date()
    except ValueError:
        return {
            "status": "INCOMPLETE",
            "message": "Use deadline format YYYY-MM-DD."
        }

    if not requirements:
        return {
            "status": "INCOMPLETE",
            "message": "Assignment requirements are missing."
        }

    # Prepare tasks
    task_names = [
        "Understand the assignment",
        "Collect study material",
        "Complete the main work",
        "Review and correct errors",
        "Submit the assignment"
    ]

    if "presentation" in [
        r.lower() for r in requirements
    ]:
        task_names.insert(3, "Prepare presentation")

    today = datetime.today().date()
    tasks = []

    # Distribute task dates before the final deadline
    total = len(task_names)

    for i, task in enumerate(task_names):
        due_date = deadline - timedelta(days=total - 1 - i)
        tasks.append({
            "task": task,
            "priority": "High" if i >= total - 2 else "Medium",
            "deadline": due_date.isoformat()
        })

    # Validate task dates
    conflicts = []
    for task in tasks:
        task_date = datetime.strptime(
            task["deadline"], "%Y-%m-%d"
        ).date()

        if task_date > deadline:
            conflicts.append(task["task"])

    overdue = deadline < today

    return {
        "status": "PASS" if not conflicts and not overdue else "CHECK",
        "assignment": title,
        "final_deadline": deadline_text,
        "tasks": tasks,
        "deadline_conflicts": conflicts,
        "deadline_already_passed": overdue
    }


# Scenario 1
scenario1 = {
    "title": "Python Project",
    "deadline": "2026-10-30",
    "requirements": ["report", "program", "screenshots"]
}

print("SYSTEM PROMPT:")
print(system_prompt)

print("\nSCENARIO 1")
print(json.dumps(create_plan(scenario1), indent=4))

# Scenario 2
scenario2 = {
    "title": "AI Seminar Assignment",
    "deadline": "2026-11-05",
    "requirements": ["report", "presentation"]
}

print("\nSCENARIO 2")
print(json.dumps(create_plan(scenario2), indent=4))

# Change a requirement and revise the plan
scenario1["requirements"].append("presentation")

print("\nREVISED SCENARIO 1")
print(json.dumps(create_plan(scenario1), indent=4))

# Test missing deadline
scenario3 = {
    "title": "Database Assignment",
    "requirements": ["report"]
}

print("\nMISSING INFORMATION TEST")
print(json.dumps(create_plan(scenario3), indent=4))
