// PAGES
const HOME = "home";
const ATHLETE = "athlete";
const LIFT = "lift";
const BLOCK = "block";
const PROGRESS = "progress";

// NAV STATE
let navDirection = "forward";
const PROGRAMS_PAGE = "programs";
const PAGE_DEPTH = { home: 0, athlete: 1, lift: 2, block: 3, progress: 2, programs: 2 };
let currentDepth = 0;

// BREADCRUMB BUILDER
function updateBreadcrumbs(items) {
  const homeNav = document.getElementById("home-nav");
  homeNav.innerHTML = "";
  items.forEach(function (item, idx) {
    if (idx > 0) {
      const sep = document.createElement("span");
      sep.className = "nav-sep";
      sep.textContent = "/";
      homeNav.appendChild(sep);
    }
    const btn = document.createElement("button");
    btn.textContent = item.label;
    if (item.onclick) {
      btn.onclick = item.onclick;
    } else {
      btn.classList.add("nav-current");
      btn.disabled = true;
    }
    homeNav.appendChild(btn);
  });
}

// TABLES
const GENDERS = "genders"; // IMMUTABLE
const GROUPS = "groups"; // IMMUTABLE
const TYPES = "types"; // IMMUTABLE
const EXERCISES = "exercises"; // IMMUTABLE
const ATHLETES = "athletes"; // MUTABLE
const GOALS = "goals"; // MUTABLE
const LIFTS = "lifts"; // MUTABLE
const EXERCISE_BLOCKS = "exercise_blocks"; // MUTABLE
const EXERCISE_SETS = "exercise_sets"; // MUTABLE
const PROGRAMS = "programs"; // MUTABLE
const PRESETS = "presets"; // MUTABLE
const PRESET_BLOCKS = "preset_blocks"; // MUTABLE
const PRESET_SETS = "preset_sets"; // MUTABLE

// CHART ENDPOINTS
const LIFTS_BY_ATHLETE = "lifts/athlete";

const BASE_URL = "http://100.124.116.118:8000";

// GET ALL TABLE ROWS BY ENDPOINT
async function getAllData(endpoint) {
  const url = `${BASE_URL}/${endpoint}/`;
  const response = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  const data = await response.json();
  return data[endpoint];
}
// GET TABLE ROW BY ENDPOINT AND ID
async function getDataByID(endpoint, id) {
  const url = `${BASE_URL}/${endpoint.slice(0, -1)}/?id=${id}`;
  const response = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  const data = await response.json();
  return data[endpoint.slice(0, -1)];
}

// CHARTING ENDPOINTS
async function getStrengthData(athlete_id, exercise_id) {
  const url = `${BASE_URL}/strength/?athlete_id=${athlete_id}&exercise_id=${exercise_id}`;
  const response = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  const data = await response.json();
  return JSON.parse(data.data);
}

async function getLiftsByAthlete(athlete_id) {
  const url = `${BASE_URL}/${LIFTS_BY_ATHLETE}/?athlete_id=${athlete_id}`;
  const response = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  const data = await response.json();
  return data[LIFTS];
}

// CREATE AT ENDPOINT (MUTABLE TABLES ONLY)
async function createData(endpoint, params) {
  const url = `${BASE_URL}/${endpoint.slice(0, -1)}/`;
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(params),
  });
  const data = await response.json();
  return data[endpoint.slice(0, -1)];
}

// DELETE AT ENDPOINT AND ID (MUTABLE TABLES ONLY)
async function deleteDataByID(endpoint, id) {
  const url = `${BASE_URL}/${endpoint.slice(0, -1)}/?id=${id}`;
  const response = await fetch(url, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
  });
  const data = await response.json();
  return data[endpoint];
}

// UPDATE AT ENDPOINT AND ID (MUTABLE TABLES ONLY)
async function updateData(endpoint, id, params) {
  const url = `${BASE_URL}/${endpoint.slice(0, -1)}/?id=${id}`;
  const response = await fetch(url, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(params),
  });
  const data = await response.json();
  return data[endpoint.slice(0, -1)];
}

async function display_athletes() {
  const athletes_list = document.getElementById("athletes-list");
  athletes_list.innerHTML = "";
  const athletes_data = await getAllData(ATHLETES);

  if (athletes_data.length === 0) {
    const newDiv = document.createElement("div");
    newDiv.className = "none-athletes-panel";
    newDiv.innerText = "No athletes found.";
    athletes_list.appendChild(newDiv);
  } else {
    for (let i = 0; i < athletes_data.length; i++) {
      const athlete = athletes_data[i];
      const dob = new Date(athlete.dob);
      const today = new Date();
      const msInYear = 1000 * 60 * 60 * 24 * 365.25;
      const age = Math.floor((today - dob) / msInYear);

      // Outer panel div
      const panel = document.createElement("div");
      panel.id = `${ATHLETES}${athlete.id}`;
      panel.className = "athletes-panel";

      // Button to navigate to athlete content
      const navButton = document.createElement("button");
      navButton.type = "button";
      navButton.className = "athlete-nav-btn";
      navButton.onclick = loadAthletePage;

      const nameSpan = document.createElement("span");
      nameSpan.className = "athlete-name";
      const athletePrimary = document.createElement("span");
      athletePrimary.className = "panel-primary";
      athletePrimary.textContent = athlete.name;
      const athleteMeta = document.createElement("span");
      athleteMeta.className = "panel-meta";
      athleteMeta.textContent = `Age ${age}`;
      nameSpan.appendChild(athletePrimary);
      nameSpan.appendChild(athleteMeta);
      navButton.appendChild(nameSpan);

      const actions = document.createElement("div");
      actions.className = "panel-actions";

      const editButton = document.createElement("button");
      editButton.type = "button";
      editButton.innerText = "Edit";
      editButton.onclick = (e) => {
        e.stopPropagation();
        startEditAthlete(athlete, panel);
      };

      const deleteButton = document.createElement("button");
      deleteButton.type = "button";
      deleteButton.innerText = "Delete";
      deleteButton.onclick = deleteAthlete;

      actions.appendChild(editButton);
      actions.appendChild(deleteButton);

      panel.appendChild(navButton);
      panel.appendChild(actions);
      athletes_list.appendChild(panel);
    }
  }
}

function startEditAthlete(athlete, panel) {
  const originalHTML = panel.innerHTML;
  panel.innerHTML = "";
  panel.classList.add("editing");

  const form = document.createElement("div");
  form.className = "edit-form";

  const nameInput = document.createElement("input");
  nameInput.type = "text";
  nameInput.value = athlete.name;

  const dobInput = document.createElement("input");
  dobInput.type = "date";
  dobInput.value = athlete.dob.split("T")[0];

  const heightInput = document.createElement("input");
  heightInput.type = "number";
  heightInput.value = athlete.height;

  const xpInput = document.createElement("input");
  xpInput.type = "number";
  xpInput.value = athlete.xp;

  const saveBtn = document.createElement("button");
  saveBtn.innerText = "Save";
  saveBtn.onclick = async () => {
    const updated = {
      name: nameInput.value,
      dob: new Date(dobInput.value),
      height: parseInt(heightInput.value),
      xp: parseInt(xpInput.value),
    };
    await updateData(ATHLETES, athlete.id, updated);
    display_athletes();
  };

  const cancelBtn = document.createElement("button");
  cancelBtn.innerText = "Cancel";
  cancelBtn.onclick = () => display_athletes();

  form.appendChild(nameInput);
  form.appendChild(dobInput);
  form.appendChild(heightInput);
  form.appendChild(xpInput);
  form.appendChild(saveBtn);
  form.appendChild(cancelBtn);
  panel.appendChild(form);
}

async function display_lifts() {
  const lifts_list = document.getElementById("lifts-list");
  const homeNav = document.getElementById("home-nav");
  const athlete_id = parseInt(homeNav.dataset.athlete);
  lifts_list.innerHTML = "";
  const lifts_data = await getAllData(LIFTS);
  const athlete_lifts_data = lifts_data.filter(
    (l) => l.athlete_id == athlete_id,
  );

  if (athlete_lifts_data.length === 0) {
    const newDiv = document.createElement("div");
    newDiv.className = "none-lifts-panel";
    newDiv.innerText = "No lifts found.";
    lifts_list.appendChild(newDiv);
  } else {
    for (let i = 0; i < athlete_lifts_data.length; i++) {
      const lift = athlete_lifts_data[i];
      const panel = document.createElement("div");
      panel.id = `${LIFTS}${lift.id}`;
      panel.className = "lifts-panel";

      const navButton = document.createElement("button");
      navButton.type = "button";
      navButton.className = "lift-nav-btn";
      navButton.onclick = loadLiftPage;

      const nameSpan = document.createElement("span");
      nameSpan.className = "lift-name";
      const formatted = new Intl.DateTimeFormat("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
      }).format(new Date(lift.date));
      const liftPrimary = document.createElement("span");
      liftPrimary.className = "panel-primary";
      liftPrimary.textContent = formatted;
      const liftMeta = document.createElement("span");
      liftMeta.className = "panel-meta";
      liftMeta.textContent = `${lift.body_weight} lbs`;
      nameSpan.appendChild(liftPrimary);
      nameSpan.appendChild(liftMeta);
      navButton.appendChild(nameSpan);

      const actions = document.createElement("div");
      actions.className = "panel-actions";

      const editButton = document.createElement("button");
      editButton.type = "button";
      editButton.innerText = "Edit";
      editButton.onclick = (e) => {
        e.stopPropagation();
        startEditLift(lift, panel);
      };

      const deleteButton = document.createElement("button");
      deleteButton.type = "button";
      deleteButton.innerText = "Delete";
      deleteButton.onclick = deleteLift;

      actions.appendChild(editButton);
      actions.appendChild(deleteButton);

      panel.appendChild(navButton);
      panel.appendChild(actions);
      lifts_list.appendChild(panel);
    }
  }
}

function startEditLift(lift, panel) {
  panel.innerHTML = "";
  panel.classList.add("editing");

  const form = document.createElement("div");
  form.className = "edit-form";

  const dateInput = document.createElement("input");
  dateInput.type = "date";
  dateInput.value = lift.date.split("T")[0];

  const weightInput = document.createElement("input");
  weightInput.type = "number";
  weightInput.value = lift.body_weight;

  const saveBtn = document.createElement("button");
  saveBtn.innerText = "Save";
  saveBtn.onclick = async () => {
    const updated = {
      date: new Date(dateInput.value),
      body_weight: parseInt(weightInput.value),
    };
    await updateData(LIFTS, lift.id, updated);
    display_lifts();
  };

  const cancelBtn = document.createElement("button");
  cancelBtn.innerText = "Cancel";
  cancelBtn.onclick = () => display_lifts();

  form.appendChild(dateInput);
  form.appendChild(weightInput);
  form.appendChild(saveBtn);
  form.appendChild(cancelBtn);
  panel.appendChild(form);
}

async function display_goals() {
  const goals_list = document.getElementById("goals-list");
  const homeNav = document.getElementById("home-nav");
  const athlete_id = parseInt(homeNav.dataset.athlete);
  goals_list.innerHTML = "";
  const goals_data = await getAllData(GOALS);
  const athlete_goals_data = goals_data.filter(
    (g) => g.athlete_id == athlete_id,
  );

  if (athlete_goals_data.length === 0) {
    const newDiv = document.createElement("div");
    newDiv.className = "none-goals-panel";
    newDiv.innerText = "No goals found.";
    goals_list.appendChild(newDiv);
  } else {
    for (let i = 0; i < athlete_goals_data.length; i++) {
      const goal = athlete_goals_data[i];
      const panel = document.createElement("div");
      panel.id = `${GOALS}${goal.id}`;
      panel.className = "goals-panel";

      const nameSpan = document.createElement("span");
      nameSpan.className = "goal-name";
      const goal_exercise = await getDataByID(EXERCISES, goal.exercise_id);
      const formatted = new Intl.DateTimeFormat("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
      }).format(new Date(goal.start_date));

      const goalRow = document.createElement("span");
      goalRow.className = "panel-row";
      const goalPrimary = document.createElement("span");
      goalPrimary.className = "panel-primary";
      goalPrimary.textContent = goal_exercise.name;
      const goalTarget = document.createElement("span");
      goalTarget.className = "panel-target";
      goalTarget.textContent = `${goal.weight} \u00D7 ${goal.reps}`;
      goalRow.appendChild(goalPrimary);
      goalRow.appendChild(goalTarget);

      const goalMeta = document.createElement("span");
      goalMeta.className = "panel-meta";
      goalMeta.textContent = `Since ${formatted} \u00B7 ${goal.duration} weeks`;
      nameSpan.appendChild(goalRow);
      nameSpan.appendChild(goalMeta);

      const actions = document.createElement("div");
      actions.className = "panel-actions";

      const editButton = document.createElement("button");
      editButton.type = "button";
      editButton.innerText = "Edit";
      editButton.onclick = () => startEditGoal(goal, panel);

      const deleteButton = document.createElement("button");
      deleteButton.type = "button";
      deleteButton.innerText = "Delete";
      deleteButton.onclick = deleteGoal;

      actions.appendChild(editButton);
      actions.appendChild(deleteButton);

      panel.appendChild(nameSpan);
      panel.appendChild(actions);
      goals_list.appendChild(panel);
    }
  }
}

async function startEditGoal(goal, panel) {
  panel.innerHTML = "";
  panel.classList.add("editing");

  const form = document.createElement("div");
  form.className = "edit-form";

  const exercise_data = await getAllData(EXERCISES);
  const exerciseSelect = document.createElement("select");
  exercise_data.forEach((ex) => {
    const opt = document.createElement("option");
    opt.value = ex.id;
    opt.innerText = ex.name;
    if (ex.id === goal.exercise_id) opt.selected = true;
    exerciseSelect.appendChild(opt);
  });

  const weightInput = document.createElement("input");
  weightInput.type = "number";
  weightInput.value = goal.weight;

  const repsInput = document.createElement("input");
  repsInput.type = "number";
  repsInput.value = goal.reps;

  const durationInput = document.createElement("input");
  durationInput.type = "number";
  durationInput.value = goal.duration;

  const dateInput = document.createElement("input");
  dateInput.type = "date";
  dateInput.value = goal.start_date.split("T")[0];

  const saveBtn = document.createElement("button");
  saveBtn.innerText = "Save";
  saveBtn.onclick = async () => {
    const updated = {
      exercise_id: parseInt(exerciseSelect.value),
      weight: parseInt(weightInput.value),
      reps: parseInt(repsInput.value),
      duration: parseInt(durationInput.value),
      start_date: new Date(dateInput.value),
    };
    await updateData(GOALS, goal.id, updated);
    display_goals();
  };

  const cancelBtn = document.createElement("button");
  cancelBtn.innerText = "Cancel";
  cancelBtn.onclick = () => display_goals();

  form.appendChild(exerciseSelect);
  form.appendChild(weightInput);
  form.appendChild(repsInput);
  form.appendChild(durationInput);
  form.appendChild(dateInput);
  form.appendChild(saveBtn);
  form.appendChild(cancelBtn);
  panel.appendChild(form);
}

async function display_blocks() {
  const blocks_list = document.getElementById("blocks-list");
  const homeNav = document.getElementById("home-nav");
  const athlete_id = parseInt(homeNav.dataset.athlete);
  const lift_id = parseInt(homeNav.dataset.lift);
  blocks_list.innerHTML = "";
  const blocks_data = await getAllData(EXERCISE_BLOCKS);
  const lift_blocks_data = blocks_data.filter((b) => b.lift_id == lift_id);

  if (lift_blocks_data.length === 0) {
    const newDiv = document.createElement("div");
    newDiv.className = "none-blocks-panel";
    newDiv.innerText = "No blocks found.";
    blocks_list.appendChild(newDiv);
  } else {
    for (let i = 0; i < lift_blocks_data.length; i++) {
      const block = lift_blocks_data[i];
      const panel = document.createElement("div");
      panel.id = `${EXERCISE_BLOCKS}${block.id}`;
      panel.className = "blocks-panel";

      const navButton = document.createElement("button");
      navButton.type = "button";
      navButton.className = "block-nav-btn";
      navButton.onclick = loadBlockPage;

      const nameSpan = document.createElement("span");
      nameSpan.className = "block-name";
      const block_exercise = await getDataByID(EXERCISES, block.exercise_id);
      const block_goal = await getDataByID(GOALS, block.goal_id);
      const blockPrimary = document.createElement("span");
      blockPrimary.className = "panel-primary";
      blockPrimary.textContent = block_exercise.name;
      const blockMeta = document.createElement("span");
      blockMeta.className = "panel-meta";
      blockMeta.textContent = `Goal: ${block_goal.weight} \u00D7 ${block_goal.reps}`;
      nameSpan.appendChild(blockPrimary);
      nameSpan.appendChild(blockMeta);
      navButton.appendChild(nameSpan);

      const actions = document.createElement("div");
      actions.className = "panel-actions";

      const editButton = document.createElement("button");
      editButton.type = "button";
      editButton.innerText = "Edit";
      editButton.onclick = (e) => {
        e.stopPropagation();
        startEditBlock(block, panel);
      };

      const deleteButton = document.createElement("button");
      deleteButton.type = "button";
      deleteButton.innerText = "Delete";
      deleteButton.onclick = deleteBlock;

      actions.appendChild(editButton);
      actions.appendChild(deleteButton);

      panel.appendChild(navButton);
      panel.appendChild(actions);
      blocks_list.appendChild(panel);
    }
  }
}

async function startEditBlock(block, panel) {
  panel.innerHTML = "";
  panel.classList.add("editing");

  const form = document.createElement("div");
  form.className = "edit-form";

  const exercise_data = await getAllData(EXERCISES);
  const exerciseSelect = document.createElement("select");
  exercise_data.forEach((ex) => {
    const opt = document.createElement("option");
    opt.value = ex.id;
    opt.innerText = ex.name;
    if (ex.id === block.exercise_id) opt.selected = true;
    exerciseSelect.appendChild(opt);
  });

  const goals_data = await getAllData(GOALS);
  const homeNav = document.getElementById("home-nav");
  const athlete_id = parseInt(homeNav.dataset.athlete);
  const goalSelect = document.createElement("select");
  goals_data
    .filter((g) => g.athlete_id === athlete_id)
    .forEach((goal) => {
      const opt = document.createElement("option");
      opt.value = goal.id;
      opt.innerText = `Goal: ${goal.weight}x${goal.reps}`;
      if (goal.id === block.goal_id) opt.selected = true;
      goalSelect.appendChild(opt);
    });

  const orderInput = document.createElement("input");
  orderInput.type = "number";
  orderInput.value = block.block_order;

  const saveBtn = document.createElement("button");
  saveBtn.innerText = "Save";
  saveBtn.onclick = async () => {
    const updated = {
      exercise_id: parseInt(exerciseSelect.value),
      goal_id: parseInt(goalSelect.value),
      block_order: parseInt(orderInput.value),
    };
    await updateData(EXERCISE_BLOCKS, block.id, updated);
    display_blocks();
  };

  const cancelBtn = document.createElement("button");
  cancelBtn.innerText = "Cancel";
  cancelBtn.onclick = () => display_blocks();

  form.appendChild(exerciseSelect);
  form.appendChild(goalSelect);
  form.appendChild(orderInput);
  form.appendChild(saveBtn);
  form.appendChild(cancelBtn);
  panel.appendChild(form);
}

async function display_sets() {
  const container = document.getElementById("sets-table-container");
  if (!container) return;

  const homeNav = document.getElementById("home-nav");
  const block_id = parseInt(homeNav.dataset.block);
  const sets_data = await getAllData(EXERCISE_SETS);
  const block_sets = sets_data
    .filter((s) => s.block_id == block_id)
    .sort((a, b) => a.set_order - b.set_order);

  container.innerHTML = "";

  const titleRow = document.createElement("div");
  titleRow.className = "sets-table-header";
  const title = document.createElement("h2");
  title.innerText = "Sets";
  const editBtn = document.createElement("button");
  editBtn.innerText = "Edit Sets";
  editBtn.className = "edit-sets-btn";
  editBtn.onclick = () => enterEditSetsMode(block_sets);
  titleRow.appendChild(title);
  titleRow.appendChild(editBtn);
  container.appendChild(titleRow);

  if (block_sets.length === 0) {
    const none = document.createElement("div");
    none.className = "none-sets-panel";
    none.innerText = "No sets found.";
    container.appendChild(none);
    return;
  }

  const table = document.createElement("table");
  table.className = "sets-table";
  table.innerHTML = `
    <thead>
      <tr>
        <th>Order</th>
        <th>Weight (lbs)</th>
        <th>Reps</th>
        <th>RTL</th>
      </tr>
    </thead>
    <tbody>
      ${block_sets
        .map(
          (s) => `
        <tr>
          <td>${s.set_order}</td>
          <td>${s.weight}</td>
          <td>${s.reps}</td>
          <td>${s.rtl}</td>
        </tr>
      `,
        )
        .join("")}
    </tbody>
  `;
  container.appendChild(table);
}

let deletedSetIds = [];

function enterEditSetsMode(sets) {
  const container = document.getElementById("sets-table-container");
  container.innerHTML = "";
  deletedSetIds = [];

  const titleRow = document.createElement("div");
  titleRow.className = "sets-table-header";
  const title = document.createElement("h2");
  title.innerText = "Edit Sets";
  titleRow.appendChild(title);
  container.appendChild(titleRow);

  const table = document.createElement("table");
  table.className = "sets-table editing-table";
  table.id = "edit-sets-table";
  const thead = document.createElement("thead");
  thead.innerHTML = `
    <tr>
      <th>Order</th>
      <th>Weight</th>
      <th>Reps</th>
      <th>RTL</th>
      <th></th>
    </tr>
  `;
  table.appendChild(thead);

  const tbody = document.createElement("tbody");
  sets.forEach((s) => addEditRow(tbody, s));
  table.appendChild(tbody);
  container.appendChild(table);

  const actions = document.createElement("div");
  actions.className = "table-edit-actions";

  const addBtn = document.createElement("button");
  addBtn.innerText = "+ Add Set";
  addBtn.onclick = () => addEditRow(tbody);

  const saveBtn = document.createElement("button");
  saveBtn.innerText = "Save Changes";
  saveBtn.className = "save-table-btn";
  saveBtn.onclick = saveSetsTable;

  const cancelBtn = document.createElement("button");
  cancelBtn.innerText = "Cancel";
  cancelBtn.onclick = display_sets;

  actions.appendChild(addBtn);
  actions.appendChild(saveBtn);
  actions.appendChild(cancelBtn);
  container.appendChild(actions);
}

function addEditRow(tbody, set = null) {
  const tr = document.createElement("tr");
  if (set) tr.dataset.id = set.id;

  tr.innerHTML = `
    <td><input type="number" class="col-order" value="${set ? set.set_order : tbody.children.length + 1}"></td>
    <td><input type="number" class="col-weight" value="${set ? set.weight : 0}"></td>
    <td><input type="number" class="col-reps" value="${set ? set.reps : 0}"></td>
    <td><input type="number" class="col-rtl" value="${set ? set.rtl : 0}"></td>
    <td><button type="button" class="row-delete-btn">\u00D7</button></td>
  `;

  tr.querySelector(".row-delete-btn").onclick = () => {
    if (set) deletedSetIds.push(set.id);
    tr.remove();
  };

  tbody.appendChild(tr);
}

async function saveSetsTable() {
  const homeNav = document.getElementById("home-nav");
  const block_id = parseInt(homeNav.dataset.block);
  const rows = document.querySelectorAll("#edit-sets-table tbody tr");

  showToast("Saving sets...", "loading");

  try {
    // 1. Delete removed sets
    for (const id of deletedSetIds) {
      await deleteDataByID(EXERCISE_SETS, id);
    }

    // 2. Update/Create sets
    for (const row of rows) {
      const id = row.dataset.id;
      const data = {
        block_id: block_id,
        set_order: parseInt(row.querySelector(".col-order").value),
        weight: parseInt(row.querySelector(".col-weight").value),
        reps: parseInt(row.querySelector(".col-reps").value),
        rtl: parseInt(row.querySelector(".col-rtl").value),
      };

      if (id) {
        await updateData(EXERCISE_SETS, id, data);
      } else {
        await createData(EXERCISE_SETS, data);
      }
    }

    showToast("Sets saved!", "success");
    display_sets();
  } catch (err) {
    showToast("Error saving sets.", "error");
    console.error(err);
  }
}

async function createAthlete(event) {
  event.preventDefault();
  const new_athlete = {
    name: document.getElementById("name").value,
    dob: new Date(document.getElementById("dob").value),
    xp: parseInt(document.getElementById("xp").value),
    height: parseInt(document.getElementById("height").value),
    gender_id: document.getElementById("gender").value == "male" ? 1 : 2,
  };
  const data = await createData(ATHLETES, new_athlete);
  display_athletes();
}

async function createLift(event) {
  event.preventDefault();
  const homeNav = document.getElementById("home-nav");
  const new_lift = {
    athlete_id: parseInt(homeNav.dataset.athlete),
    date: new Date(document.getElementById("date").value),
    body_weight: parseInt(document.getElementById("body-weight").value),
  };
  const data = await createData(LIFTS, new_lift);
  display_lifts();
}

async function createGoal(event) {
  event.preventDefault();
  const homeNav = document.getElementById("home-nav");
  const new_goal = {
    athlete_id: parseInt(homeNav.dataset.athlete),
    start_date: new Date(document.getElementById("start-date").value),
    exercise_id: document.getElementById("exercise").value,
    duration: parseInt(document.getElementById("duration").value),
    reps: parseInt(document.getElementById("reps").value),
    weight: parseInt(document.getElementById("weight").value),
  };
  const data = await createData(GOALS, new_goal);
  display_goals();
}

async function createBlock(event) {
  event.preventDefault();
  const homeNav = document.getElementById("home-nav");
  const new_block = {
    lift_id: parseInt(homeNav.dataset.lift),
    goal_id: parseInt(document.getElementById("goal").value),
    exercise_id: parseInt(document.getElementById("exercise").value),
    block_order: parseInt(document.getElementById("order").value),
  };
  const data = await createData(EXERCISE_BLOCKS, new_block);
  display_blocks();
}

async function createSet(event) {
  event.preventDefault();
  const homeNav = document.getElementById("home-nav");
  const new_set = {
    block_id: parseInt(homeNav.dataset.block),
    weight: parseInt(document.getElementById("weight").value),
    reps: parseInt(document.getElementById("reps").value),
    rtl: parseInt(document.getElementById("rtl").value),
    set_order: parseInt(document.getElementById("set-order").value),
  };
  const data = await createData(EXERCISE_SETS, new_set);
  display_sets();
}

async function deleteAthlete(event) {
  event.preventDefault();
  const athleteDiv = event.target.closest(".athletes-panel");
  const athlete_id = parseInt(athleteDiv.id.slice(ATHLETES.length));

  // Delete all sets within all blocks within all lifts for this athlete
  const sets_data = await getAllData(EXERCISE_SETS);
  const blocks_data = await getAllData(EXERCISE_BLOCKS);
  const lifts_data = await getAllData(LIFTS);
  const goals_data = await getAllData(GOALS);

  const athlete_lift_ids = lifts_data
    .filter((l) => l.athlete_id === athlete_id)
    .map((l) => l.id);

  const athlete_block_ids = blocks_data
    .filter((b) => athlete_lift_ids.includes(b.lift_id))
    .map((b) => b.id);

  for (const set of sets_data) {
    if (athlete_block_ids.includes(set.block_id)) {
      await deleteDataByID(EXERCISE_SETS, set.id);
    }
  }

  for (const block of blocks_data) {
    if (athlete_lift_ids.includes(block.lift_id)) {
      await deleteDataByID(EXERCISE_BLOCKS, block.id);
    }
  }

  for (const lift of lifts_data) {
    if (lift.athlete_id === athlete_id) {
      await deleteDataByID(LIFTS, lift.id);
    }
  }

  for (const goal of goals_data) {
    if (goal.athlete_id === athlete_id) {
      await deleteDataByID(GOALS, goal.id);
    }
  }

  await deleteDataByID(ATHLETES, athlete_id);
  display_athletes();
}

async function deleteLift(event) {
  event.preventDefault();
  const liftDiv = event.target.closest(".lifts-panel");
  const lift_id = parseInt(liftDiv.id.slice(LIFTS.length));

  // Delete all sets within all blocks for this lift
  const sets_data = await getAllData(EXERCISE_SETS);
  const blocks_data = await getAllData(EXERCISE_BLOCKS);

  const lift_block_ids = blocks_data
    .filter((b) => b.lift_id === lift_id)
    .map((b) => b.id);

  for (const set of sets_data) {
    if (lift_block_ids.includes(set.block_id)) {
      await deleteDataByID(EXERCISE_SETS, set.id);
    }
  }

  for (const block of blocks_data) {
    if (block.lift_id === lift_id) {
      await deleteDataByID(EXERCISE_BLOCKS, block.id);
    }
  }

  await deleteDataByID(LIFTS, lift_id);
  display_lifts();
}

async function deleteGoal(event) {
  event.preventDefault();
  const goalDiv = event.target.closest(".goals-panel");
  const data = await deleteDataByID(
    GOALS,
    parseInt(goalDiv.id.slice(GOALS.length)),
  );
  display_goals();
}

async function deleteBlock(event) {
  event.preventDefault();
  const blockDiv = event.target.closest(".blocks-panel");
  const data = await deleteDataByID(
    EXERCISE_BLOCKS,
    parseInt(blockDiv.id.slice(EXERCISE_BLOCKS.length)),
  );
  const homeNav = document.getElementById("home-nav");
  const block_id = parseInt(homeNav.dataset.block);
  const sets_data = await getAllData(EXERCISE_SETS);
  for (let i = 0; i < sets_data.length; i++) {
    if (block_id == sets_data[i].block_id) {
      await deleteDataByID(EXERCISE_SETS, sets_data[i].id);
    }
  }
  display_blocks();
}

async function deleteSet(event) {
  event.preventDefault();
  const setDiv = event.target.closest(".sets-panel");
  const data = await deleteDataByID(
    EXERCISE_SETS,
    parseInt(setDiv.id.slice(EXERCISE_SETS.length)),
  );
  display_sets();
}

async function loadPage(pageName) {
  const page_content = await fetch(`pages/${pageName}.html`);
  const page_html = await page_content.text();
  const content = document.getElementById("page-content");
  content.innerHTML = page_html;
  content.classList.remove("page-enter-forward", "page-enter-back");
  void content.offsetWidth; // force reflow to restart animation
  content.classList.add(
    navDirection === "back" ? "page-enter-back" : "page-enter-forward",
  );
}

async function loadHomePage(event) {
  if (event) event.preventDefault();
  navDirection = currentDepth > PAGE_DEPTH.home ? "back" : "forward";
  currentDepth = PAGE_DEPTH.home;
  await loadPage(HOME);
  const page_title_div = document.getElementById("page-title");
  page_title_div.innerHTML = "";
  page_title_div.innerText = "Athletes";
  updateBreadcrumbs([{ label: "Home", onclick: null }]);
  await display_athletes();
}

async function getExercises() {
  const exercise_data = await getAllData(EXERCISES);
  const exercise_select = document.getElementById("exercise");
  for (let i = 0; i < exercise_data.length; i++) {
    const newOption = document.createElement("option");
    newOption.value = exercise_data[i].id;
    newOption.innerText = exercise_data[i].name;
    exercise_select.appendChild(newOption);
  }
}

async function getGoals() {
  const goals_data = await getAllData(GOALS);
  const goal_select = document.getElementById("goal");
  const homeNav = document.getElementById("home-nav");
  const athlete_id = parseInt(homeNav.dataset.athlete);
  const athlete_goals_data = [];
  for (let i = 0; i < goals_data.length; i++) {
    if (goals_data[i].athlete_id === athlete_id) {
      athlete_goals_data.push(goals_data[i]);
    }
  }
  for (let i = 0; i < athlete_goals_data.length; i++) {
    const newOption = document.createElement("option");
    newOption.value = athlete_goals_data[i].id;
    const goal_exercise = await getDataByID(
      EXERCISES,
      athlete_goals_data[i].exercise_id,
    );
    const formatted = new Intl.DateTimeFormat("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    }).format(new Date(athlete_goals_data[i].start_date));
    newOption.innerText = `${goal_exercise.name} -> ${athlete_goals_data[i].weight} x ${athlete_goals_data[i].reps} - Start Date: ${formatted}`;
    goal_select.appendChild(newOption);
  }
}

async function updateLateralNav(
  endpoint,
  currentId,
  loadFunc,
  filterFunc = null,
) {
  const container = document.getElementById("lateral-nav");
  if (!container) return;
  container.innerHTML = "";

  let allItems = await getAllData(endpoint);
  if (filterFunc) {
    allItems = allItems.filter(filterFunc);
  }

  const currentIndex = allItems.findIndex((item) => item.id === currentId);
  if (currentIndex === -1) return;

  const prevItem = allItems[currentIndex - 1];
  const nextItem = allItems[currentIndex + 1];

  const prevBtn = document.createElement("button");
  prevBtn.textContent = "Previous";
  prevBtn.disabled = !prevItem;
  if (prevItem) prevBtn.onclick = () => loadFunc(null, prevItem.id);

  const nextBtn = document.createElement("button");
  nextBtn.textContent = "Next";
  nextBtn.disabled = !nextItem;
  if (nextItem) nextBtn.onclick = () => loadFunc(null, nextItem.id);

  container.appendChild(prevBtn);
  container.appendChild(nextBtn);
}

async function loadAthletePage(event, athleteId) {
  if (event) event.preventDefault();
  const athlete_id =
    athleteId !== undefined
      ? athleteId
      : parseInt(
          event.target.closest(".athletes-panel").id.slice(ATHLETES.length),
        );
  const athlete_data = await getDataByID(ATHLETES, athlete_id);
  navDirection = currentDepth > PAGE_DEPTH.athlete ? "back" : "forward";
  currentDepth = PAGE_DEPTH.athlete;
  await loadPage(ATHLETE);
  const page_title_div = document.getElementById("page-title");
  page_title_div.innerHTML = "";
  page_title_div.innerText = athlete_data.name;
  const homeNav = document.getElementById("home-nav");
  homeNav.dataset.athlete = athlete_data.id;
  updateBreadcrumbs([
    { label: "Home", onclick: () => loadHomePage(null) },
    { label: athlete_data.name, onclick: null },
  ]);
  await updateLateralNav(ATHLETES, athlete_id, loadAthletePage);
  await getExercises();
  await display_lifts();
  await display_goals();
}

async function loadLiftPage(event, liftId) {
  if (event) event.preventDefault();
  const lift_id =
    liftId !== undefined
      ? liftId
      : parseInt(event.target.closest(".lifts-panel").id.slice(LIFTS.length));
  const lift_data = await getDataByID(LIFTS, lift_id);
  const homeNav = document.getElementById("home-nav");
  const athlete_id = parseInt(homeNav.dataset.athlete);
  const athlete_data = await getDataByID(ATHLETES, athlete_id);
  navDirection = currentDepth > PAGE_DEPTH.lift ? "back" : "forward";
  currentDepth = PAGE_DEPTH.lift;
  await loadPage(LIFT);
  const formattedDate = new Intl.DateTimeFormat("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  }).format(new Date(lift_data.date));
  const lift_title = `${formattedDate} - ${lift_data.body_weight} lbs`;
  const page_title_div = document.getElementById("page-title");
  page_title_div.innerHTML = "";
  const lift_table_div = document.createElement("div");
  lift_table_div.innerText = lift_title;
  page_title_div.appendChild(lift_table_div);
  homeNav.dataset.lift = lift_id;
  const breadcrumb_date = new Intl.DateTimeFormat("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  }).format(new Date(lift_data.date));
  updateBreadcrumbs([
    { label: "Home", onclick: () => loadHomePage(null) },
    {
      label: athlete_data.name,
      onclick: () => loadAthletePage(null, athlete_id),
    },
    { label: breadcrumb_date, onclick: null },
  ]);
  await updateLateralNav(
    LIFTS,
    lift_id,
    loadLiftPage,
    (l) => l.athlete_id === athlete_id,
  );
  await getExercises();
  await getGoals();
  await populateProgramDropdown();
  await display_blocks();
}

async function loadBlockPage(event, blockId) {
  if (event) event.preventDefault();
  const block_id =
    blockId !== undefined
      ? blockId
      : parseInt(
          event.target
            .closest(".blocks-panel")
            .id.slice(EXERCISE_BLOCKS.length),
        );
  const block_data = await getDataByID(EXERCISE_BLOCKS, block_id);
  const lift_data = await getDataByID(LIFTS, block_data.lift_id);
  const athlete_id = lift_data.athlete_id;
  const athlete_data = await getDataByID(ATHLETES, athlete_id);

  navDirection = currentDepth > PAGE_DEPTH.block ? "back" : "forward";
  currentDepth = PAGE_DEPTH.block;

  await loadPage(BLOCK);
  const exercise_data = await getDataByID(EXERCISES, block_data.exercise_id);
  const page_title_div = document.getElementById("page-title");
  page_title_div.innerHTML = "";
  page_title_div.innerText = exercise_data.name;

  const homeNav = document.getElementById("home-nav");
  homeNav.dataset.athlete = athlete_id;
  homeNav.dataset.lift = lift_data.id;
  homeNav.dataset.block = block_id;

  const breadcrumb_date = new Intl.DateTimeFormat("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  }).format(new Date(lift_data.date));

  updateBreadcrumbs([
    { label: "Home", onclick: () => loadHomePage(null) },
    {
      label: athlete_data.name,
      onclick: () => loadAthletePage(null, athlete_id),
    },
    { label: breadcrumb_date, onclick: () => loadLiftPage(null, lift_data.id) },
    { label: exercise_data.name, onclick: null },
  ]);
  await updateLateralNav(
    EXERCISE_BLOCKS,
    block_id,
    loadBlockPage,
    (b) => b.lift_id === lift_data.id,
  );
  await display_sets();
}

async function loadProgressPage(event) {
  if (event) event.preventDefault();

  const homeNav = document.getElementById("home-nav");
  const athlete_id = parseInt(homeNav.dataset.athlete);
  const athlete_data = await getDataByID(ATHLETES, athlete_id);

  navDirection = currentDepth > PAGE_DEPTH.progress ? "back" : "forward";
  currentDepth = PAGE_DEPTH.progress;

  await loadPage(PROGRESS);
  const page_title_div = document.getElementById("page-title");
  page_title_div.innerHTML = "";
  page_title_div.innerText = `${athlete_data.name} - PROGRESS`;

  const lateral_nav = document.getElementById("lateral-nav");
  if (lateral_nav) lateral_nav.innerHTML = "";

  const [athlete_lifts_data, allBlocksData, allExercisesData] =
    await Promise.all([
      getLiftsByAthlete(athlete_id),
      getAllData(EXERCISE_BLOCKS),
      getAllData(EXERCISES),
    ]);

  // === Body Weight Chart ===
  const ctx = document
    .getElementById("weight-progression-chart")
    .getContext("2d");

  const gradient = ctx.createLinearGradient(0, 0, 0, 320);
  gradient.addColorStop(0, "rgba(242, 140, 56, 0.35)");
  gradient.addColorStop(1, "rgba(242, 140, 56, 0)");

  new Chart(ctx, {
    type: "line",
    data: {
      labels: athlete_lifts_data.map((row) => row.date),
      datasets: [
        {
          label: "Body Weight",
          data: athlete_lifts_data.map((row) => row.body_weight),
          borderColor: "#F28C38",
          backgroundColor: gradient,
          fill: true,
          borderWidth: 2,
          pointBackgroundColor: "#F28C38",
          pointBorderColor: "#FFFFFF",
          pointBorderWidth: 2,
          pointRadius: 4,
          pointHoverRadius: 6,
          tension: 0.3,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (item) => `Body Weight: ${item.parsed.y} lbs`,
          },
        },
      },
      scales: {
        x: {
          type: "time",
          time: {
            unit: "day",
            minUnit: "day",
            tooltipFormat: "MMM d, yyyy",
            displayFormats: { day: "MMM d" },
          },
          title: {
            display: true,
            text: "Lift Date",
            color: "#707070",
            font: { family: "Montserrat, sans-serif", size: 12, weight: "500" },
          },
          ticks: {
            color: "#707070",
            font: { family: "Montserrat, sans-serif", size: 11 },
          },
          grid: { color: "#E2E2E2" },
        },
        y: {
          beginAtZero: false,
          title: {
            display: true,
            text: "Body Weight (lbs)",
            color: "#707070",
            font: { family: "Montserrat, sans-serif", size: 12, weight: "500" },
          },
          ticks: {
            color: "#707070",
            font: { family: "Montserrat, sans-serif", size: 11 },
            callback: (value) => `${value} lbs`,
          },
          grid: { color: "#E2E2E2" },
        },
      },
    },
  });

  // === Strength Chart Controls ===
  const exerciseSelect = document.getElementById("strength-exercise");
  const metricSelect = document.getElementById("strength-metric");
  const startDateInput = document.getElementById("start-date");
  const endDateInput = document.getElementById("end-date");
  const updateBtn = document.getElementById("update-strength-btn");
  const chartMessage = document.getElementById("strength-chart-message");

  // Populate exercise dropdown with all exercises done by this athlete
  const athleteBlockIds = allBlocksData
    .filter((b) =>
      athlete_lifts_data.some((l) => l.id === b.lift_id)
    )
    .map((b) => b.exercise_id);
  const uniqueExerciseIds = [...new Set(athleteBlockIds)];
  
  uniqueExerciseIds.forEach(exId => {
    const ex = allExercisesData.find(e => e.id === exId);
    if (ex) {
      const opt = document.createElement("option");
      opt.value = ex.id;
      opt.textContent = ex.name;
      exerciseSelect.appendChild(opt);
    }
  });

  // State
  let cachedStrengthData = null; // { exerciseId, data[] }
  let strengthChart = null;

  function getMetricLabel(metric) {
    const labels = {
      weight: "Weight (lbs)",
      load: "Load",
      intensity: "Intensity",
      rtl: "RTL",
      volume: "Volume",
      "1RM": "1RM (lbs)"
    };
    return labels[metric] || metric;
  }

  function renderStrengthChart(data, metric) {
    const ctx2 = document
      .getElementById("strength-progression-chart")
      .getContext("2d");

    if (strengthChart) {
      strengthChart.destroy();
    }

    chartMessage.style.display = "none";

    // Daily Maximums Logic
    // Group by date and find max of the selected metric
    const dailyData = {};
    data.forEach(row => {
      // row.date might be ISO string or numeric timestamp
      const dateObj = new Date(row.date);
      if (isNaN(dateObj.getTime())) return;

      const d = dateObj.toISOString().substring(0, 10);
      if (!dailyData[d] || row[metric] > dailyData[d][metric]) {
        dailyData[d] = row;
      }
    });

    const sortedDates = Object.keys(dailyData).sort();
    console.log("Unique days found:", sortedDates.length, sortedDates);
    
    // Do not generate chart if there is only one data point
    if (sortedDates.length < 2) {
      strengthChart = null;
      ctx2.clearRect(0, 0, ctx2.canvas.width, ctx2.canvas.height);
      if (sortedDates.length === 1) {
        chartMessage.innerText = `Only one day of data found (${sortedDates[0]}). Need at least two to plot progression.`;
        chartMessage.style.display = "block";
      } else {
        chartMessage.innerText = "No data found for the selected criteria.";
        chartMessage.style.display = "block";
      }
      return;
    }

    const chartData = sortedDates.map(d => dailyData[d][metric]);
    const chartLabels = sortedDates.map(d => new Intl.DateTimeFormat("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    }).format(new Date(d)));

    const grad2 = ctx2.createLinearGradient(0, 0, 0, 320);
    grad2.addColorStop(0, "rgba(242, 140, 56, 0.35)");
    grad2.addColorStop(1, "rgba(242, 140, 56, 0)");

    const metricLabel = getMetricLabel(metric);

    strengthChart = new Chart(ctx2, {
      type: "line",
      data: {
        labels: chartLabels,
        datasets: [
          {
            label: metricLabel,
            data: chartData,
            borderColor: "#F28C38",
            backgroundColor: grad2,
            fill: true,
            borderWidth: 2,
            pointBackgroundColor: "#F28C38",
            pointBorderColor: "#FFFFFF",
            pointBorderWidth: 2,
            pointRadius: 4,
            pointHoverRadius: 6,
            tension: 0.3,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (item) => `${metricLabel}: ${item.parsed.y.toFixed(2)}`,
            },
          },
        },
        scales: {
          x: {
            title: {
              display: true,
              text: "Date",
              color: "#707070",
              font: {
                family: "Montserrat, sans-serif",
                size: 12,
                weight: "500",
              },
            },
            ticks: {
              color: "#707070",
              font: { family: "Montserrat, sans-serif", size: 11 },
            },
            grid: { color: "#E2E2E2" },
          },
          y: {
            beginAtZero: false,
            title: {
              display: true,
              text: metricLabel,
              color: "#707070",
              font: {
                family: "Montserrat, sans-serif",
                size: 12,
                weight: "500",
              },
            },
            ticks: {
              color: "#707070",
              font: { family: "Montserrat, sans-serif", size: 11 },
            },
            grid: { color: "#E2E2E2" },
          },
        },
      },
    });
  }

  async function updateStrengthChart() {
    const selectedExerciseId = parseInt(exerciseSelect.value);
    const selectedMetric = metricSelect.value;
    const startDate = startDateInput.value;
    const endDate = endDateInput.value;

    console.log("Updating chart:", { selectedExerciseId, selectedMetric, startDate, endDate });

    if (!selectedExerciseId) {
      chartMessage.innerText = "Please select an exercise.";
      chartMessage.style.display = "block";
      return;
    }

    if (
      !cachedStrengthData ||
      cachedStrengthData.exerciseId !== selectedExerciseId
    ) {
      const rawData = await getStrengthData(athlete_id, selectedExerciseId);
      cachedStrengthData = {
        exerciseId: selectedExerciseId,
        data: typeof rawData === "string" ? JSON.parse(rawData) : rawData,
      };
    }

    let filteredData = cachedStrengthData.data;
    console.log("Total datapoints for exercise:", filteredData.length);

    if (startDate) {
      const startTime = new Date(startDate + "T00:00:00").getTime();
      filteredData = filteredData.filter(row => new Date(row.date).getTime() >= startTime);
    }
    if (endDate) {
      const endTime = new Date(endDate + "T23:59:59").getTime();
      filteredData = filteredData.filter(row => new Date(row.date).getTime() <= endTime);
    }

    console.log("Datapoints after filtering:", filteredData.length);
    renderStrengthChart(filteredData, selectedMetric);
  }

  updateBtn.onclick = updateStrengthChart;

  exerciseSelect.addEventListener("change", () => {
    cachedStrengthData = null;
  });

  updateBreadcrumbs([
    { label: "Home", onclick: () => loadHomePage(null) },
    {
      label: athlete_data.name,
      onclick: () => loadAthletePage(null, athlete_id),
    },
    { label: "Progress", onclick: null },
  ]);
}

// ===== Programs Page ===== //
async function loadProgramsPage(event) {
  if (event) event.preventDefault();
  const homeNav = document.getElementById("home-nav");
  const athlete_id = parseInt(homeNav.dataset.athlete);
  const athlete_data = await getDataByID(ATHLETES, athlete_id);

  navDirection = currentDepth > PAGE_DEPTH.programs ? "back" : "forward";
  currentDepth = PAGE_DEPTH.programs;

  await loadPage(PROGRAMS_PAGE);
  const page_title_div = document.getElementById("page-title");
  page_title_div.innerHTML = "";
  page_title_div.innerText = "Programs";

  updateBreadcrumbs([
    { label: "Home", onclick: () => loadHomePage(null) },
    {
      label: athlete_data.name,
      onclick: () => loadAthletePage(null, athlete_id),
    },
    { label: "Programs", onclick: null },
  ]);

  await display_programs();
}

async function display_programs() {
  const programs_list = document.getElementById("programs-list");
  const homeNav = document.getElementById("home-nav");
  const athlete_id = parseInt(homeNav.dataset.athlete);
  programs_list.innerHTML = "";
  const programs_data = await getAllData(PROGRAMS);
  const athlete_programs = programs_data.filter(
    (p) => p.athlete_id === athlete_id,
  );

  if (athlete_programs.length === 0) {
    const newDiv = document.createElement("div");
    newDiv.className = "none-programs-panel";
    newDiv.innerText = "No programs found.";
    programs_list.appendChild(newDiv);
  } else {
    for (let i = 0; i < athlete_programs.length; i++) {
      const program = athlete_programs[i];
      const panel = document.createElement("div");
      panel.id = `${PROGRAMS}${program.id}`;
      panel.className = "programs-panel";

      const navButton = document.createElement("button");
      navButton.type = "button";
      navButton.className = "program-nav-btn";
      navButton.onclick = () => selectProgram(program.id);

      const nameSpan = document.createElement("span");
      nameSpan.className = "program-name";
      const programPrimary = document.createElement("span");
      programPrimary.className = "panel-primary";
      programPrimary.textContent = program.name;
      nameSpan.appendChild(programPrimary);
      navButton.appendChild(nameSpan);

      const actions = document.createElement("div");
      actions.className = "panel-actions";

      const editButton = document.createElement("button");
      editButton.type = "button";
      editButton.innerText = "Edit";
      editButton.onclick = (e) => {
        e.stopPropagation();
        startEditProgram(program, panel);
      };

      const deleteButton = document.createElement("button");
      deleteButton.type = "button";
      deleteButton.innerText = "Delete";
      deleteButton.onclick = () => deleteProgram(program.id);

      actions.appendChild(editButton);
      actions.appendChild(deleteButton);

      panel.appendChild(navButton);
      panel.appendChild(actions);
      programs_list.appendChild(panel);
    }
  }
}

function startEditProgram(program, panel) {
  panel.innerHTML = "";
  panel.classList.add("editing");

  const form = document.createElement("div");
  form.className = "edit-form";

  const nameInput = document.createElement("input");
  nameInput.type = "text";
  nameInput.value = program.name;

  const saveBtn = document.createElement("button");
  saveBtn.innerText = "Save";
  saveBtn.onclick = async () => {
    await updateData(PROGRAMS, program.id, { name: nameInput.value });
    display_programs();
  };

  const cancelBtn = document.createElement("button");
  cancelBtn.innerText = "Cancel";
  cancelBtn.onclick = () => display_programs();

  form.appendChild(nameInput);
  form.appendChild(saveBtn);
  form.appendChild(cancelBtn);
  panel.appendChild(form);
}

async function selectProgram(program_id) {
  const homeNav = document.getElementById("home-nav");
  homeNav.dataset.program = program_id;

  // Hide deeper sections
  document.getElementById("preset-block-section").style.display = "none";
  document.getElementById("preset-set-section").style.display = "none";

  // Show and populate presets
  document.getElementById("preset-section").style.display = "";
  await display_presets(program_id);
}

async function display_presets(program_id) {
  const presets_list = document.getElementById("presets-list");
  presets_list.innerHTML = "";
  const presets_data = await getAllData(PRESETS);
  const program_presets = presets_data.filter(
    (p) => p.program_id === program_id,
  );

  if (program_presets.length === 0) {
    const newDiv = document.createElement("div");
    newDiv.className = "none-presets-panel";
    newDiv.innerText = "No presets found.";
    presets_list.appendChild(newDiv);
  } else {
    for (let i = 0; i < program_presets.length; i++) {
      const preset = program_presets[i];
      const panel = document.createElement("div");
      panel.id = `${PRESETS}${preset.id}`;
      panel.className = "presets-panel";

      const navButton = document.createElement("button");
      navButton.type = "button";
      navButton.className = "preset-nav-btn";
      navButton.onclick = () => selectPreset(preset.id);

      const nameSpan = document.createElement("span");
      nameSpan.className = "preset-name";
      const presetPrimary = document.createElement("span");
      presetPrimary.className = "panel-primary";
      presetPrimary.textContent = preset.name;
      nameSpan.appendChild(presetPrimary);
      navButton.appendChild(nameSpan);

      const actions = document.createElement("div");
      actions.className = "panel-actions";

      const editButton = document.createElement("button");
      editButton.type = "button";
      editButton.innerText = "Edit";
      editButton.onclick = (e) => {
        e.stopPropagation();
        startEditPreset(preset, panel);
      };

      const deleteButton = document.createElement("button");
      deleteButton.type = "button";
      deleteButton.innerText = "Delete";
      deleteButton.onclick = () => deletePreset(preset.id);

      actions.appendChild(editButton);
      actions.appendChild(deleteButton);

      panel.appendChild(navButton);
      panel.appendChild(actions);
      presets_list.appendChild(panel);
    }
  }
}

function startEditPreset(preset, panel) {
  panel.innerHTML = "";
  panel.classList.add("editing");

  const form = document.createElement("div");
  form.className = "edit-form";

  const nameInput = document.createElement("input");
  nameInput.type = "text";
  nameInput.value = preset.name;

  const saveBtn = document.createElement("button");
  saveBtn.innerText = "Save";
  saveBtn.onclick = async () => {
    await updateData(PRESETS, preset.id, { name: nameInput.value });
    const homeNav = document.getElementById("home-nav");
    display_presets(parseInt(homeNav.dataset.program));
  };

  const cancelBtn = document.createElement("button");
  cancelBtn.innerText = "Cancel";
  cancelBtn.onclick = () => {
    const homeNav = document.getElementById("home-nav");
    display_presets(parseInt(homeNav.dataset.program));
  };

  form.appendChild(nameInput);
  form.appendChild(saveBtn);
  form.appendChild(cancelBtn);
  panel.appendChild(form);
}

async function selectPreset(preset_id) {
  const homeNav = document.getElementById("home-nav");
  homeNav.dataset.preset = preset_id;

  // Hide deeper section
  document.getElementById("preset-set-section").style.display = "none";

  // Show and populate preset blocks
  document.getElementById("preset-block-section").style.display = "";
  await populatePresetExercises();
  await populatePresetGoals();
  await display_preset_blocks(preset_id);
}

async function populatePresetExercises() {
  const exercise_data = await getAllData(EXERCISES);
  const exercise_select = document.getElementById("preset-exercise");
  exercise_select.innerHTML = "";
  for (let i = 0; i < exercise_data.length; i++) {
    const newOption = document.createElement("option");
    newOption.value = exercise_data[i].id;
    newOption.innerText = exercise_data[i].name;
    exercise_select.appendChild(newOption);
  }
}

async function populatePresetGoals() {
  const goals_data = await getAllData(GOALS);
  const goal_select = document.getElementById("preset-goal");
  const homeNav = document.getElementById("home-nav");
  const athlete_id = parseInt(homeNav.dataset.athlete);
  goal_select.innerHTML = "";
  const athlete_goals = goals_data.filter((g) => g.athlete_id === athlete_id);
  for (let i = 0; i < athlete_goals.length; i++) {
    const newOption = document.createElement("option");
    newOption.value = athlete_goals[i].id;
    const goal_exercise = await getDataByID(
      EXERCISES,
      athlete_goals[i].exercise_id,
    );
    const formatted = new Intl.DateTimeFormat("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    }).format(new Date(athlete_goals[i].start_date));
    newOption.innerText = `${goal_exercise.name} -> ${athlete_goals[i].weight} x ${athlete_goals[i].reps} - Start Date: ${formatted}`;
    goal_select.appendChild(newOption);
  }
}

async function display_preset_blocks(preset_id) {
  const blocks_list = document.getElementById("preset-blocks-list");
  blocks_list.innerHTML = "";
  const blocks_data = await getAllData(PRESET_BLOCKS);
  const preset_blocks = blocks_data.filter((b) => b.preset_id === preset_id);

  if (preset_blocks.length === 0) {
    const newDiv = document.createElement("div");
    newDiv.className = "none-preset-blocks-panel";
    newDiv.innerText = "No preset blocks found.";
    blocks_list.appendChild(newDiv);
  } else {
    for (let i = 0; i < preset_blocks.length; i++) {
      const block = preset_blocks[i];
      const panel = document.createElement("div");
      panel.id = `${PRESET_BLOCKS}${block.id}`;
      panel.className = "preset-blocks-panel";

      const navButton = document.createElement("button");
      navButton.type = "button";
      navButton.className = "preset-block-nav-btn";
      navButton.onclick = () => selectPresetBlock(block.id);

      const nameSpan = document.createElement("span");
      nameSpan.className = "preset-block-name";
      const block_exercise = await getDataByID(EXERCISES, block.exercise_id);
      const blockPrimary = document.createElement("span");
      blockPrimary.className = "panel-primary";
      blockPrimary.textContent = block_exercise.name;
      const blockMeta = document.createElement("span");
      blockMeta.className = "panel-meta";
      blockMeta.textContent = `Order: ${block.block_order}`;
      nameSpan.appendChild(blockPrimary);
      nameSpan.appendChild(blockMeta);
      navButton.appendChild(nameSpan);

      const actions = document.createElement("div");
      actions.className = "panel-actions";

      const editButton = document.createElement("button");
      editButton.type = "button";
      editButton.innerText = "Edit";
      editButton.onclick = (e) => {
        e.stopPropagation();
        startEditPresetBlock(block, panel);
      };

      const deleteButton = document.createElement("button");
      deleteButton.type = "button";
      deleteButton.innerText = "Delete";
      deleteButton.onclick = () => deletePresetBlock(block.id);

      actions.appendChild(editButton);
      actions.appendChild(deleteButton);

      panel.appendChild(navButton);
      panel.appendChild(actions);
      blocks_list.appendChild(panel);
    }
  }
}

async function startEditPresetBlock(block, panel) {
  panel.innerHTML = "";
  panel.classList.add("editing");

  const form = document.createElement("div");
  form.className = "edit-form";

  const exercise_data = await getAllData(EXERCISES);
  const exerciseSelect = document.createElement("select");
  exercise_data.forEach((ex) => {
    const opt = document.createElement("option");
    opt.value = ex.id;
    opt.innerText = ex.name;
    if (ex.id === block.exercise_id) opt.selected = true;
    exerciseSelect.appendChild(opt);
  });

  const goals_data = await getAllData(GOALS);
  const homeNav = document.getElementById("home-nav");
  const athlete_id = parseInt(homeNav.dataset.athlete);
  const goalSelect = document.createElement("select");
  goals_data
    .filter((g) => g.athlete_id === athlete_id)
    .forEach((goal) => {
      const opt = document.createElement("option");
      opt.value = goal.id;
      opt.innerText = `Goal: ${goal.weight}x${goal.reps}`;
      if (goal.id === block.goal_id) opt.selected = true;
      goalSelect.appendChild(opt);
    });

  const orderInput = document.createElement("input");
  orderInput.type = "number";
  orderInput.value = block.block_order;

  const saveBtn = document.createElement("button");
  saveBtn.innerText = "Save";
  saveBtn.onclick = async () => {
    const updated = {
      exercise_id: parseInt(exerciseSelect.value),
      goal_id: parseInt(goalSelect.value),
      block_order: parseInt(orderInput.value),
    };
    await updateData(PRESET_BLOCKS, block.id, updated);
    const homeNav = document.getElementById("home-nav");
    display_preset_blocks(parseInt(homeNav.dataset.preset));
  };

  const cancelBtn = document.createElement("button");
  cancelBtn.innerText = "Cancel";
  cancelBtn.onclick = () => {
    const homeNav = document.getElementById("home-nav");
    display_preset_blocks(parseInt(homeNav.dataset.preset));
  };

  form.appendChild(exerciseSelect);
  form.appendChild(goalSelect);
  form.appendChild(orderInput);
  form.appendChild(saveBtn);
  form.appendChild(cancelBtn);
  panel.appendChild(form);
}

async function selectPresetBlock(preset_block_id) {
  const homeNav = document.getElementById("home-nav");
  homeNav.dataset.presetBlock = preset_block_id;

  document.getElementById("preset-set-section").style.display = "";
  await display_preset_sets(preset_block_id);
}

async function display_preset_sets(preset_block_id) {
  const sets_list = document.getElementById("preset-sets-list");
  sets_list.innerHTML = "";
  const sets_data = await getAllData(PRESET_SETS);
  const block_sets = sets_data.filter(
    (s) => s.preset_block_id === preset_block_id,
  );

  if (block_sets.length === 0) {
    const newDiv = document.createElement("div");
    newDiv.className = "none-preset-sets-panel";
    newDiv.innerText = "No preset sets found.";
    sets_list.appendChild(newDiv);
  } else {
    for (let i = 0; i < block_sets.length; i++) {
      const set = block_sets[i];
      const panel = document.createElement("div");
      panel.id = `${PRESET_SETS}${set.id}`;
      panel.className = "preset-sets-panel";

      const navButton = document.createElement("button");
      navButton.type = "button";
      navButton.className = "preset-set-nav-btn";

      const nameSpan = document.createElement("span");
      nameSpan.className = "preset-set-name";
      const setPrimary = document.createElement("span");
      setPrimary.className = "panel-primary";
      setPrimary.textContent = `${set.reps} reps`;
      const setMeta = document.createElement("span");
      setMeta.className = "panel-meta";
      setMeta.textContent = `Set ${set.set_order}`;
      nameSpan.appendChild(setPrimary);
      nameSpan.appendChild(setMeta);
      navButton.appendChild(nameSpan);

      const actions = document.createElement("div");
      actions.className = "panel-actions";

      const editButton = document.createElement("button");
      editButton.type = "button";
      editButton.innerText = "Edit";
      editButton.onclick = () => startEditPresetSet(set, panel);

      const deleteButton = document.createElement("button");
      deleteButton.type = "button";
      deleteButton.innerText = "Delete";
      deleteButton.onclick = () => deletePresetSet(set.id);

      actions.appendChild(editButton);
      actions.appendChild(deleteButton);

      panel.appendChild(navButton);
      panel.appendChild(actions);
      sets_list.appendChild(panel);
    }
  }
}

function startEditPresetSet(set, panel) {
  panel.innerHTML = "";
  panel.classList.add("editing");

  const form = document.createElement("div");
  form.className = "edit-form";

  const repsInput = document.createElement("input");
  repsInput.type = "number";
  repsInput.value = set.reps;

  const orderInput = document.createElement("input");
  orderInput.type = "number";
  orderInput.value = set.set_order;

  const saveBtn = document.createElement("button");
  saveBtn.innerText = "Save";
  saveBtn.onclick = async () => {
    const updated = {
      reps: parseInt(repsInput.value),
      set_order: parseInt(orderInput.value),
    };
    await updateData(PRESET_SETS, set.id, updated);
    const homeNav = document.getElementById("home-nav");
    display_preset_sets(parseInt(homeNav.dataset.presetBlock));
  };

  const cancelBtn = document.createElement("button");
  cancelBtn.innerText = "Cancel";
  cancelBtn.onclick = () => {
    const homeNav = document.getElementById("home-nav");
    display_preset_sets(parseInt(homeNav.dataset.presetBlock));
  };

  form.appendChild(repsInput);
  form.appendChild(orderInput);
  form.appendChild(saveBtn);
  form.appendChild(cancelBtn);
  panel.appendChild(form);
}

// ===== Programs CRUD ===== //
async function createProgram(event) {
  event.preventDefault();
  const homeNav = document.getElementById("home-nav");
  const new_program = {
    athlete_id: parseInt(homeNav.dataset.athlete),
    name: document.getElementById("program-name").value,
  };
  await createData(PROGRAMS, new_program);
  display_programs();
}

async function createPreset(event) {
  event.preventDefault();
  const homeNav = document.getElementById("home-nav");
  const new_preset = {
    program_id: parseInt(homeNav.dataset.program),
    name: document.getElementById("preset-name").value,
  };
  await createData(PRESETS, new_preset);
  display_presets(parseInt(homeNav.dataset.program));
}

async function createPresetBlock(event) {
  event.preventDefault();
  const homeNav = document.getElementById("home-nav");
  const new_block = {
    preset_id: parseInt(homeNav.dataset.preset),
    exercise_id: parseInt(document.getElementById("preset-exercise").value),
    block_order: parseInt(document.getElementById("preset-block-order").value),
    goal_id: parseInt(document.getElementById("preset-goal").value),
  };
  await createData(PRESET_BLOCKS, new_block);
  display_preset_blocks(parseInt(homeNav.dataset.preset));
}

async function createPresetSet(event) {
  event.preventDefault();
  const homeNav = document.getElementById("home-nav");
  const new_set = {
    preset_block_id: parseInt(homeNav.dataset.presetBlock),
    reps: parseInt(document.getElementById("preset-reps").value),
    set_order: parseInt(document.getElementById("preset-set-order").value),
  };
  await createData(PRESET_SETS, new_set);
  display_preset_sets(parseInt(homeNav.dataset.presetBlock));
}

async function deleteProgram(program_id) {
  // Cascade: delete all preset_sets, preset_blocks, presets under this program
  const presets_data = await getAllData(PRESETS);
  const preset_blocks_data = await getAllData(PRESET_BLOCKS);
  const preset_sets_data = await getAllData(PRESET_SETS);

  const program_preset_ids = presets_data
    .filter((p) => p.program_id === program_id)
    .map((p) => p.id);
  const program_block_ids = preset_blocks_data
    .filter((b) => program_preset_ids.includes(b.preset_id))
    .map((b) => b.id);

  for (const set of preset_sets_data) {
    if (program_block_ids.includes(set.preset_block_id)) {
      await deleteDataByID(PRESET_SETS, set.id);
    }
  }
  for (const block of preset_blocks_data) {
    if (program_preset_ids.includes(block.preset_id)) {
      await deleteDataByID(PRESET_BLOCKS, block.id);
    }
  }
  for (const preset of presets_data) {
    if (preset.program_id === program_id) {
      await deleteDataByID(PRESETS, preset.id);
    }
  }
  await deleteDataByID(PROGRAMS, program_id);

  // Hide child sections
  document.getElementById("preset-section").style.display = "none";
  document.getElementById("preset-block-section").style.display = "none";
  document.getElementById("preset-set-section").style.display = "none";
  display_programs();
}

async function deletePreset(preset_id) {
  const preset_blocks_data = await getAllData(PRESET_BLOCKS);
  const preset_sets_data = await getAllData(PRESET_SETS);

  const preset_block_ids = preset_blocks_data
    .filter((b) => b.preset_id === preset_id)
    .map((b) => b.id);

  for (const set of preset_sets_data) {
    if (preset_block_ids.includes(set.preset_block_id)) {
      await deleteDataByID(PRESET_SETS, set.id);
    }
  }
  for (const block of preset_blocks_data) {
    if (block.preset_id === preset_id) {
      await deleteDataByID(PRESET_BLOCKS, block.id);
    }
  }
  await deleteDataByID(PRESETS, preset_id);

  const homeNav = document.getElementById("home-nav");
  document.getElementById("preset-block-section").style.display = "none";
  document.getElementById("preset-set-section").style.display = "none";
  display_presets(parseInt(homeNav.dataset.program));
}

async function deletePresetBlock(preset_block_id) {
  const preset_sets_data = await getAllData(PRESET_SETS);
  for (const set of preset_sets_data) {
    if (set.preset_block_id === preset_block_id) {
      await deleteDataByID(PRESET_SETS, set.id);
    }
  }
  await deleteDataByID(PRESET_BLOCKS, preset_block_id);

  const homeNav = document.getElementById("home-nav");
  document.getElementById("preset-set-section").style.display = "none";
  display_preset_blocks(parseInt(homeNav.dataset.preset));
}

async function deletePresetSet(preset_set_id) {
  await deleteDataByID(PRESET_SETS, preset_set_id);
  const homeNav = document.getElementById("home-nav");
  display_preset_sets(parseInt(homeNav.dataset.presetBlock));
}

// ===== Apply Preset to Lift ===== //
async function populateProgramDropdown() {
  const homeNav = document.getElementById("home-nav");
  const athlete_id = parseInt(homeNav.dataset.athlete);
  const programs = await getAllData(PROGRAMS);
  const select = document.getElementById("program-select");
  if (!select) return;
  programs
    .filter((p) => p.athlete_id === athlete_id)
    .forEach((p) => {
      const opt = document.createElement("option");
      opt.value = p.id;
      opt.textContent = p.name;
      select.appendChild(opt);
    });
}

async function loadPresetsForProgram(programId) {
  const presetSelect = document.getElementById("preset-select");
  presetSelect.innerHTML = '<option value="">-- Select Preset --</option>';
  if (!programId) {
    presetSelect.disabled = true;
    return;
  }
  const presets = await getAllData(PRESETS);
  presets
    .filter((p) => p.program_id === parseInt(programId))
    .forEach((p) => {
      const opt = document.createElement("option");
      opt.value = p.id;
      opt.textContent = p.name;
      presetSelect.appendChild(opt);
    });
  presetSelect.disabled = false;
}

async function applyPreset(event) {
  event.preventDefault();
  const homeNav = document.getElementById("home-nav");
  const lift_id = parseInt(homeNav.dataset.lift);
  const preset_id = parseInt(document.getElementById("preset-select").value);
  if (!preset_id) return;
  const url = `${BASE_URL}/apply_preset/`;
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ lift_id, preset_id }),
  });
  const data = await response.json();
  display_blocks();
}

// ===== Data Export ===== //
async function exportData() {
  showToast("Exporting data...", "loading");
  try {
    const response = await fetch(`${BASE_URL}/export/`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });
    if (!response.ok) throw new Error("Export request failed");
    const data = await response.json();
    // Strip the message field; keep metadata and all data arrays
    const { message, ...exportPayload } = data;
    const json = JSON.stringify(exportPayload, null, 2);
    const blob = new Blob([json], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    const timestamp = new Date().toISOString().slice(0, 10);
    a.href = url;
    a.download = `lifting-data-export-${timestamp}.json`;
    a.click();
    URL.revokeObjectURL(url);
    showToast("Export successful!", "success");
  } catch {
    showToast("Export failed. Is the server running?", "error");
  }
}

// ===== Data Import ===== //
async function importData(event) {
  const file = event.target.files[0];
  if (!file) return;

  // File size guard (10 MB)
  if (file.size > 10 * 1024 * 1024) {
    showToast("File too large (max 10 MB).", "error");
    event.target.value = "";
    return;
  }

  showToast("Importing data...", "loading");

  let payload;
  try {
    const text = await file.text();
    payload = JSON.parse(text);
  } catch {
    showToast("Invalid JSON file.", "error");
    event.target.value = "";
    return;
  }

  // Client-side schema check before sending
  const tables = ["athletes", "lifts", "exercises", "programs"]; // Check for core tables
  let hasData = false;
  for (const key of tables) {
    if (Array.isArray(payload[key])) {
      hasData = true;
      break;
    }
  }
  if (!hasData) {
    showToast("Invalid format: no data tables found.", "error");
    event.target.value = "";
    return;
  }

  try {
    const response = await fetch(`${BASE_URL}/import/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      const err = await response.json();
      let msg = "Unknown error";
      if (typeof err.detail === "string") {
        msg = err.detail;
      } else if (Array.isArray(err.detail)) {
        msg = err.detail.map((e) => `${e.loc.join(".")}: ${e.msg}`).join(" | ");
      }
      showToast(`Import failed: ${msg}`, "error");
      event.target.value = "";
      return;
    }
    showToast("Import successful!", "success");
    event.target.value = "";
    await display_athletes();
  } catch {
    showToast("Import failed. Is the server running?", "error");
    event.target.value = "";
  }
}

// ===== Toast Notifications ===== //
function showToast(message, type) {
  const existing = document.getElementById("toast");
  if (existing) existing.remove();

  const toast = document.createElement("div");
  toast.id = "toast";
  toast.className = `toast toast--${type}`;
  toast.textContent = message;
  document.body.appendChild(toast);

  if (type !== "loading") {
    setTimeout(() => toast.remove(), 3000);
  }
}

// INITIAL PAGE LOAD
(async () => {
  await loadPage(HOME);
  await display_athletes();
})();
