# PawPal+ UML Class Diagram


classDiagram
    class Owner {
        +String name
        +int available_minutes
        +list preferences
        +Pet pet
        +set_pet(pet)
        +get_pet()
    }

    class Pet {
        +String name
        +String species
        +int age
        +list tasks
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
        +is_valid()
    }

    class Scheduler {
        +Owner owner
        +generate_plan()
        +sort_by_priority(tasks)
        +fits_in_time(task, time_used)
    }

    class DailyPlan {
        +Owner owner
        +list scheduled
        +list skipped
        +int total_minutes
        +summary()
        +reasoning()
    }

    Owner "1" --> "1" Pet : owns
    Pet "1" o-- "0..*" Task : has
    Scheduler --> Owner : takes
    Scheduler ..> DailyPlan : produces
    DailyPlan --> Owner : references

