const STORAGE_KEY = "todo-polished-v1";

const todoForm = document.getElementById("todoForm");
const todoInput = document.getElementById("todoInput");
const todoList = document.getElementById("todoList");
const emptyState = document.getElementById("emptyState");
const filterButtons = document.querySelectorAll(".filter-btn");
const clearCompletedBtn = document.getElementById("clearCompletedBtn");
const stats = document.getElementById("stats");

let tasks = [];
let activeFilter = "all";

function loadTasks() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) return [];

  try {
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    return parsed.filter(
      (item) =>
        item &&
        typeof item.id === "string" &&
        typeof item.text === "string" &&
        typeof item.completed === "boolean"
    );
  } catch {
    return [];
  }
}

function saveTasks() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
}

function getVisibleTasks() {
  if (activeFilter === "completed") return tasks.filter((task) => task.completed);
  if (activeFilter === "active") return tasks.filter((task) => !task.completed);
  return tasks;
}

function updateStats() {
  const total = tasks.length;
  const completed = tasks.filter((task) => task.completed).length;
  const active = total - completed;
  stats.textContent = `${total} total • ${active} active • ${completed} done`;
}

function render() {
  const visibleTasks = getVisibleTasks();
  todoList.innerHTML = "";
  emptyState.style.display = visibleTasks.length === 0 ? "block" : "none";

  visibleTasks.forEach((task) => {
    const li = document.createElement("li");
    li.className = "task";
    if (task.completed) li.classList.add("completed");

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = task.completed;
    checkbox.addEventListener("change", () => {
      task.completed = checkbox.checked;
      saveTasks();
      render();
    });

    const span = document.createElement("span");
    span.className = "task-text";
    span.textContent = task.text;

    const delBtn = document.createElement("button");
    delBtn.className = "delete-btn";
    delBtn.type = "button";
    delBtn.textContent = "Delete";
    delBtn.addEventListener("click", () => {
      tasks = tasks.filter((item) => item.id !== task.id);
      saveTasks();
      render();
    });

    li.append(checkbox, span, delBtn);
    todoList.appendChild(li);
  });

  filterButtons.forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.filter === activeFilter);
  });

  updateStats();
}

todoForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const text = todoInput.value.trim();
  if (!text) return;

  tasks.unshift({
    id: crypto.randomUUID(),
    text,
    completed: false
  });

  saveTasks();
  todoInput.value = "";
  todoInput.focus();
  render();
});

filterButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    activeFilter = btn.dataset.filter;
    render();
  });
});

clearCompletedBtn.addEventListener("click", () => {
  tasks = tasks.filter((task) => !task.completed);
  saveTasks();
  render();
});

tasks = loadTasks();
render();
