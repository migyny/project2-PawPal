# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
  - My initial UML design will have 5 classes: owner, pet, task, scheduler and daily plan. Owner holds reference to pet, and pet has a set of tasks that needs to be done. Scheduler takes owner and pet as input and makes daily plan as output. This way the design will seperate data like owner,pet and task from logic like scheduler and output daily plan, so i can test everything seperately.
- What classes did you include, and what responsibilities did you assign to each?
  - I will have 5 classes: owner, pet, task, scheduler and daily plan.
 Owner: stores owner's name, daily available time and preferences. Owner should also hold a reference to their pets.
  - Attributes: name, available_minutes, preferences, pets(list)
  - Methods: add_pet(), get_pets()
 Pet: stores name, species, age, and a list of tasks.
  - Attributes: name, species, age, tasks
  - Methods: add_task(), remove_taks(), get_tasks()
 Task: task assigned to pet with name and category (walk,feed,sleep, etc.), duration of the task, and optional preferred time of the day.
  - Attributes: task_id, name, category, duration_minutes, priority, time_of_day
  - Methods: is_valid()
 Scheduler: takes owner and pet as input, and it should generate daily plan by sorting tasks by priority nad fitting them to the time the owner is available. 
  - Attributes: owne, pet
  - Methods: generate_plan(), sort_by_priority(), _fits_in_time()
 Daily plan: it is the output of the scheduler. Has the list of sccheduled tasks, skipped tasks, and total time. Also has to give reasoning
  - Attributes: scheduled, skipped, total_minutes
  - Methods: summary(), reasoning()

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
