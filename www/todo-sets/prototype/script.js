const todoForm = document.getElementById("todoForm");
const todoInput = document.getElementById("todoInput");
const todoList = document.getElementById("todoList");
const emptyState = document.getElementById("emptyState");

const tasks = [];

function render() {
  todoList.innerHTML = "";
  emptyState.style.display = tasks.length === 0 ? "block" : "none";

  tasks.forEach((task) => {
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

    const span = document.createElement("span");
    span.className = "task-text";
    span.textContent = task.text;

    const delBtn = document.createElement("button");
    delBtn.className = "delete-btn";
    delBtn.type = "button";
    delBtn.textContent = "Delete";
    delBtn.addEventListener("click", () => {
      const idx = tasks.findIndex((item) => item.id === task.id);
      if (idx >= 0) tasks.splice(idx, 1);
      render();
    });

    li.append(checkbox, span, delBtn);
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

render();
