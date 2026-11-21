const API_URL = "/tasks/";

const taskForm = document.getElementById("task-form");
const taskList = document.getElementById("task-list");
const statusFilter = document.getElementById("status-filter");

// Carregar tarefas
async function loadTasks() {
    const status = statusFilter.value;
    let url = API_URL;

    if (status) {
        url += `?status=${encodeURIComponent(status)}`;
    }

    try {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error("Erro ao carregar tarefas.");
        }

        const tasks = await response.json();
        renderTasks(tasks);

    } catch (error) {
        taskList.textContent = "Não foi possível carregar as tarefas.";
        console.error(error);
    }
}

// Exibir tarefas na página
function renderTasks(tasks) {
    taskList.innerHTML = "";

    if (tasks.length === 0) {
        taskList.textContent = "Nenhuma tarefa encontrada.";
        return;
    }

    tasks.forEach(task => {
        const card = document.createElement("article");
        card.className = "task-card";

        const title = document.createElement("h3");
        title.textContent = task.title;

        const description = document.createElement("p");
        description.textContent = task.description || "Sem descrição.";

        const details = document.createElement("p");
        details.textContent =
            `Prioridade: ${task.priority} | Status: ${task.status}`;

        const actions = document.createElement("div");
        actions.className = "task-actions";

        const editButton = document.createElement("button");
        editButton.textContent = "Editar";
        editButton.addEventListener("click", () => editTask(task));

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Excluir";
        deleteButton.className = "delete-button";
        deleteButton.addEventListener("click", () => deleteTask(task.id));

        actions.append(editButton, deleteButton);
        card.append(title, description, details, actions);

        taskList.appendChild(card);
    });
}

// Criar tarefa
taskForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const task = {
        title: document.getElementById("title").value.trim(),
        description: document.getElementById("description").value.trim(),
        priority: document.getElementById("priority").value
    };

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(task)
        });

        if (!response.ok) {
            throw new Error("Erro ao criar tarefa.");
        }

        taskForm.reset();
        loadTasks();

    } catch (error) {
        alert("Não foi possível criar a tarefa.");
        console.error(error);
    }
});

// Editar tarefa
async function editTask(task) {
    const title = prompt("Novo título:", task.title);

    if (title === null) return;

    if (!title.trim()) {
        alert("O título não pode ficar vazio.");
        return;
    }

    const description = prompt("Nova descrição:", task.description || "");
    if (description === null) return;

    const priority = prompt(
        "Prioridade (baixa, média ou alta):",
        task.priority
    );

    if (priority === null) return;

    const status = prompt(
        "Status (A Fazer, Em Progresso ou Concluído):",
        task.status
    );

    if (status === null) return;

    try {
        const response = await fetch(`${API_URL}${task.id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: title.trim(),
                description,
                priority: priority.toLowerCase(),
                status
            })
        });

        if (!response.ok) {
            throw new Error("Erro ao atualizar tarefa.");
        }

        loadTasks();

    } catch (error) {
        alert("Não foi possível atualizar a tarefa. Verifique os valores.");
        console.error(error);
    }
}

// Excluir tarefa
async function deleteTask(taskId) {
    if (!confirm("Tem certeza que deseja excluir esta tarefa?")) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}${taskId}`, {
            method: "DELETE"
        });

        if (!response.ok) {
            throw new Error("Erro ao excluir tarefa.");
        }

        loadTasks();

    } catch (error) {
        alert("Não foi possível excluir a tarefa.");
        console.error(error);
    }
}

// Atualizar lista ao alterar o filtro
statusFilter.addEventListener("change", loadTasks);

// Carregar tarefas ao abrir a página
loadTasks();