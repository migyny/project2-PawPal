import pandas as pd
import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler, DEFAULT_DURATIONS

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ---------------------------------------------------------------------------
# Owner
# ---------------------------------------------------------------------------
st.subheader("Owner")
col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
with col2:
    available_minutes = st.number_input(
        "Available minutes today", min_value=10, max_value=480, value=60
    )

# ---------------------------------------------------------------------------
# Pets
# ---------------------------------------------------------------------------
st.subheader("Pets")

if "pets" not in st.session_state:
    st.session_state.pets = []

col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    age = st.number_input("Age (years)", min_value=0, max_value=30, value=3)

if st.button("Add pet"):
    existing_names = [p.name for p in st.session_state.pets]
    if pet_name in existing_names:
        st.error(f"A pet named '{pet_name}' is already added.")
    else:
        st.session_state.pets.append(Pet(name=pet_name, species=species, age=int(age)))
        st.success(f"Added {pet_name}!")

if st.session_state.pets:
    st.write("Current pets:")
    pets_df = pd.DataFrame([
        {"name": p.name, "species": p.species, "age": p.age}
        for p in st.session_state.pets
    ], index=range(1, len(st.session_state.pets) + 1))
    st.table(pets_df)
else:
    st.info("No pets yet. Add one above.")

# ---------------------------------------------------------------------------
# Tasks
# ---------------------------------------------------------------------------
st.subheader("Tasks")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

PRIORITY_MAP = {"high": 1, "medium": 2, "low": 3}

if not st.session_state.pets:
    st.info("Add a pet first before adding tasks.")
else:
    pet_names = [p.name for p in st.session_state.pets]
    assigned_to = st.selectbox("Assign task to", pet_names)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_name = st.text_input("Task name", value="Morning walk")
        category = st.selectbox("Category", ["walk", "feed", "meds", "grooming", "other"])
    with col2:
        selected_pet = next((p for p in st.session_state.pets if p.name == assigned_to), None)
        species_defaults = DEFAULT_DURATIONS.get(selected_pet.species.lower(), {}) if selected_pet else {}
        default_duration = species_defaults.get(category, 15)
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=default_duration)
        time_of_day = st.selectbox("Time of day", ["morning", "afternoon", "evening", "anytime"])
    with col3:
        priority_label = st.selectbox("Priority", ["high", "medium", "low"])

    if st.button("Add task"):
        task_id = f"task_{len(st.session_state.tasks) + 1}"
        tod = None if time_of_day == "anytime" else time_of_day
        new_task = Task(
            task_id=task_id,
            name=task_name,
            category=category,
            duration_minutes=int(duration),
            priority=PRIORITY_MAP[priority_label],
            time_of_day=tod,
        )
        if new_task.is_valid():
            st.session_state.tasks.append({"task": new_task, "pet": assigned_to})
        else:
            st.error("Task has invalid fields — check duration and priority.")

if st.session_state.tasks:
    st.write("Current tasks:")
    tasks_df = pd.DataFrame([
        {
            "pet": t["pet"],
            "name": t["task"].name,
            "category": t["task"].category,
            "duration (min)": t["task"].duration_minutes,
            "priority": t["task"].priority,
            "time of day": t["task"].time_of_day or "anytime",
        }
        for t in st.session_state.tasks
    ], index=range(1, len(st.session_state.tasks) + 1))
    st.table(tasks_df)

st.divider()

# ---------------------------------------------------------------------------
# Generate Schedule
# ---------------------------------------------------------------------------
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if not st.session_state.pets:
        st.warning("Add at least one pet before generating a schedule.")
    elif not st.session_state.tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        owner = Owner(name=owner_name, available_minutes=int(available_minutes))

        add_error = False
        for pet in st.session_state.pets:
            fresh_pet = Pet(name=pet.name, species=pet.species, age=pet.age)
            for entry in st.session_state.tasks:
                if entry["pet"] == pet.name:
                    try:
                        fresh_pet.add_task(entry["task"])
                    except ValueError as e:
                        st.error(f"Task error: {e}")
                        add_error = True
            owner.add_pet(fresh_pet)

        if add_error:
            st.stop()

        scheduler = Scheduler(owner)

        conflicts = scheduler.detect_conflicts()
        if conflicts:
            st.warning("Conflicts detected — review before proceeding:")
            for msg in conflicts:
                st.warning(f"⚠ {msg}")

        plans = scheduler.generate_all_plans()
        st.session_state.plans = plans
        st.success("Schedule generated!")

if "plans" in st.session_state and st.session_state.plans:
    for plan in st.session_state.plans:
        st.text(plan.summary())
        total = len(plan.scheduled) + len(plan.skipped)
        rate = len(plan.scheduled) / total if total else 0.0
        st.metric(
            label=f"{plan.pet.name} — tasks scheduled",
            value=f"{len(plan.scheduled)}/{total}",
            delta=f"{rate:.0%} scheduled",
        )
        with st.expander(f"Reasoning — {plan.pet.name}"):
            st.text(plan.reasoning())
