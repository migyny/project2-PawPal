# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
  - My initial UML design will have 5 classes: owner, pet, task, scheduler and daily plan. Owner holds reference to pet, and pet has a set of tasks that needs to be done. Scheduler takes owner and pet as input and makes daily plan as output. This way the design will seperate data like owner,pet and task from logic like scheduler and output daily plan, so i can test everything seperately.
- What classes did you include, and what responsibilities did you assign to each?
  - I will have 5 classes: owner, pet, task, scheduler and daily plan.
 Owner: stores owner's name, daily available time and preferences. Owner should also hold a reference to their pets.
  - Attributes: name, available_minutes, preferences, pets
  - Methods: add_pet(pet), get_pets()
 Pet: stores name, species, age, and a list of tasks.
  - Attributes: name, species, age, tasks, task_count
  - Methods: add_task(task), remove_task(task_id), get_tasks()
 Task: task assigned to pet with name and category (walk,feed,sleep, etc.), duration of the task, and optional preferred time of the day.
  - Attributes: task_id, name, category, duration_minutes, priority, time_of_day, status
  - Methods: is_valid(), mark_in_progress(),mark_complete()
 Scheduler: takes owner and pet as input, and it should generate daily plan by sorting tasks by priority nad fitting them to the time the owner is available. 
  - Attributes: owner
  - Methods: generate_plan(pet, available), generate_all_plans(), get_tasks_for_pet(pet_name), sort_by_priority(tasks), detect_conflicts()
 Daily plan: it is the output of the scheduler. Has the list of sccheduled tasks, skipped tasks, and total time. Also has to give reasoning
  - Attributes: scheduled, skipped, available_minutes, owner, pet, total_minutes
  - Methods: summary(), reasoning(), completion_rate()

**b. Design changes**

- Did your design change during implementation?
  - Yes
- If yes, describe at least one change and why you made it.
  - In my intial UML plan, sheduler takes both owner and pet, but AI pointed that owner holds pet, and if i leave it like that i can accidentaly put pet that doesn't belong to that owner, so scheduler only needs owner and can call owner.get_pet() internally.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
  - Time constraints:
  If owner has 120 available minutes, it is shared across all pets he owns (used to have a problem where for example owner had 120 minutes and 2 pets, and after building a schedule each pet had 120 minutes available)
  - Priority: 
  Tasks are sorted by priority first and then by time of day. A task is scheduled only if it fits within the remaining available minutes. Higher priority task gets first access to the budget (according to time of day)
  - No duplicate task IDs per pet
  - Valid task fields: Task.is_valid() checks that task_id/name are non-empty, duration_minutes > 0, priority is 1/2/3, and time_of_day is recognized.
  - detect_conflicts flags when multiple pats have tasks in the same slot, since owner can't be in two places at once.
  - If a task's duration is 0, it's filled form the species+category table.
- How did you decide which constraints mattered most?
  - The most important for me was priority, time constraints, and edge cases. Sorting by priority first ensures the owner's most important responsibilities are protected before time runs out. For time constraint: once available_minutes is exhausted, nothing else runs. I also discovered a bug where each pet was getting the full budget instead of sharing it, which showed that getting this constraint right was really important.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
  1. generate_plan adds tasks one by one and skips any that don't fit, so it never looks ahead. This means a long low priority task early in the list can block multiple shorter high priority tasks from being scheduled, even if swapping them would be better.
  2. generate_all_plans gives time to pets in list order. The first pet gets first request on the full budget. Later, pets get whatever remains. If the first pet's tasks uses most of the time, the second pet's tasks may be skipped.
- Why is that tradeoff reasonable for this scenario?
  1. generate_plan : it is reasonable because it is simple and predictable. An owner can read the output and understand why something was skipped.
  2. generate_all_plans: it is simple to implement, but not fair to pets added later.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
  - I used AI on multiple stages, so it can correct my thinking and implementation of my ideas. It helped me brainstorm some ideas, corrected my UML design and helped find some bugs.
- What kinds of prompts or questions were most helpful?
  - When AI suggested some changes I didn't understand, I asked to explain these changes in examples (like " how would this change affect the program/ change the UI)

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
  - Ai was implementing default task duration for dog and cat, and it mistakenly made priority = 2, instead of making the Owner choose one. As a reslt, the priority of any task would have been 2.
- How did you evaluate or verify what the AI suggested?
  - I checked the code myself if it made sense. I also ran a pytest and manually checked the website if the changes I made worked correctly.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
  - test_sort_by_time_then_priority: verifies that sort_by_priority orders tasks by time of day first and then by priority (For example checks that morning feed (priority 1) comes before morning walk (priority 2), nd that all morning tasks come before afternoon  and evening ones).
  - test_add_task_increase_count: verifies that adding a task to a pet increments task_count from 0 to 1.
  - test_mark_complete_changes_status: verifies calling mark_complete() on a task changes its status from "pending" to "complete"
- Why were these tests important?
  - test_sort_by_time_then_priority: if tasks were sorted wrong, high priority tasks  could be pushed behind low priority ones and get skipped when the time budget runs out.
  - test_add_task_increase_count: task_count verifies a pet has tasks before scheduling. If adding a task failed, the scheduler would generate empty plans with no error.
  - test_mark_complete_changes_status: if mark_ complete() didn't work, the completion rate would always show 0% no matter what tasks were actually finished.

**b. Confidence**

- How confident are you that your scheduler works correctly?
  - I think the core logic was tested and it seems correct (the right task s get prioritized). Also the data operations like add task, update status are verified through testing.
- What edge cases would you test next if you had more time?
  - If owner has 0 or few minutes available - schedules should be empty, and all tasks are in skipped
  - If owner has less minutes than a task.
  - duplicate ID's
  - Two tasks, same time slot, different priority.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
  - I liked to make a UML diagram and figure out how everything should work before even touching code.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
  - Fair time for pets: for now the first pet gets priority in owner;s available time, but I want to make it so that every pet would have somewhat equal time.
  - For now I have greedy approach that skips a task if it doesn't fit, even if a shorter lower priority task could fill the gap. I want to use time more efficiently.
  - detect_conflict just prints the conflict message, but scheduler doesn't check them. Ideally, it should block scheduling ot adjust the plan, not just print a message.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
  - You should always check the code that AI suggests. During this project, I found mistakes that would have been pushed if I didn;t catch them.
