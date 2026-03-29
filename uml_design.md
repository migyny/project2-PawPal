# PawPal+ UML Class Diagram


classDiagram
    class Owner {
        +String name
        +int available_minutes
        +list preferences
        +list pets
        +add_pet(pet)
        +get_pets()
    }

    class Pet {
        +String name
        +String species
        +int age
        +list tasks
        +int task_count
        +add_task(task)
        +remove_task(task_id)
        +get_tasks()
    }

    class Task {
        +String task_id
        +String name
        +String category
        +int duration_minutes
        +int priority
        +String time_of_day
        +String status
        +mark_in_progress()
        +mark_complete()
        +is_valid()
    }

    class Scheduler {
        +Owner owner
        +generate_plan(pet, available)
        +generate_all_plans()
        +get_tasks_for_pet(pet_name)
        +sort_by_priority(tasks)
        +detect_conflicts()
    }

    class DailyPlan {
        +Owner owner
        +Pet pet
        +int available_minutes
        +list scheduled
        +list skipped
        +int total_minutes
        +completion_rate()
        +summary()
        +reasoning()
    }

    Owner "1" --> "0..*" Pet : owns
    Pet "1" o-- "0..*" Task : has
    Scheduler --> Owner : takes
    Scheduler ..> DailyPlan : produces
    DailyPlan --> Owner : references
    DailyPlan --> Pet : references
