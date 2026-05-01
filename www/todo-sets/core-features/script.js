const todoForm = document.getElementById("todoForm");
const todoInput = document.getElementById("todoInput");
const todoList = document.getElementById("todoList");
const taskCount = document.getElementById("taskCount");
const emptyState = document.getElementById("emptyState");
const filterButtons = document.querySelectorAll(".filter-btn");

const tasks = [];
let currentFilter = "all";

function getFilteredTasks() {
  if (currentFilter === "completed") {
    return tasks.filter((task) => task.completed);
  }
  if (currentFilter === "active") {
    return tasks.filter((task) => !task.completed);
  }
  return tasks;
}

function updateCount() {
  const done = tasks.filter((task) => task.completed).length;
  taskCount.textContent = `${tasks.length} tasks • ${done} completed`;
}

function render() {
  todoList.innerHTML = "";
  const visibleTasks = getFilteredTasks();
  emptyState.style.display = visibleTasks.length === 0 ? "block" : "none";
  updateCount();

  visibleTasks.forEach((task) => {
    const li = document.createElement("li");
    li.className = "task";
    if (task.completed) li.classList.add("completed");

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = task.completed;
    checkbox.addEventListener("change", () => {
      task.completed = checkbox.checked;
      render();
    });

    const text = document.createElement("span");
    text.className = "task-text";
    text.textContent = task.text;

    const delBtn = document.createElement("button");
    delBtn.className = "delete-btn";
    delBtn.type = "button";
    delBtn.textContent = "Delete";
    delBtn.addEventListener("click", () => {
      const idx = tasks.findIndex((item) => item.id === task.id);
      if (idx >= 0) tasks.splice(idx, 1);
      render();
    });

    li.append(checkbox, text, delBtn);
    todoList.appendChild(li);
  });
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

  todoInput.value = "";
  todoInput.focus();
  render();
});

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    currentFilter = button.dataset.filter;
    filterButtons.forEach((btn) => btn.classList.remove("active"));
    button.classList.add("active");
    render();
  });
});

render();
