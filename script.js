const admins = [
    { name: 'Mousa Ashraf', email: 'mousaashraf@gmail.com', verified: true },
    { name: 'Mohamed Elsadaany', email: 'mohamedelsadaany@hotmail.com', verified: true }
];

const users = [
    { name: 'Doaa Hamdy', email: 'doaa@gmail.com', verified: false },
];

const tasks = [
    { title: 'Complete report', description: 'Finish the quarterly report', category: 'Work', budget: 500, deadline: '2024-12-31', owner: 'Mousa Ashraf', assignedUser: 'Doaa Hamdy' }
];

function showSection(sectionId) {
    document.querySelectorAll('section').forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(sectionId).classList.add('active');
    renderList(sectionId);
}

function renderList(type) {
    const listId = type === 'admins' ? 'adminList' : type === 'users' ? 'userList' : 'taskList';
    const list = type === 'admins' ? admins : type === 'users' ? users : tasks;
    const container = document.getElementById(listId);
    container.innerHTML = '';

    list.forEach((item, index) => {
        const row = document.createElement('tr');
        if (type === 'admins' || type === 'users') {
            row.innerHTML = `
                <td>${item.name}</td>
                <td>${item.email}</td>
                <td>${item.verified ? 'Yes' : 'No'}</td>
                <td>
                    <button onclick="editItem('${type}', ${index})">Edit</button>
                    <button onclick="deleteItem('${type}', ${index})">Delete</button>
                </td>
            `;
        } else {
            row.innerHTML = `
                <td>${item.title}</td>
                <td>${item.description}</td>
                <td>${item.category}</td>
                <td>${item.budget}</td>
                <td>${item.deadline}</td>
                <td>
                    <select onchange="updateOwner(${index}, this.value)">
                        <option value="">Select Owner</option>
                        ${admins.map(admin => `
                            <option value="${admin.name}" ${item.owner === admin.name ? 'selected' : ''}>
                                ${admin.name}
                            </option>
                        `).join('')}
                    </select>
                </td>
                <td>
                    <select onchange="assignUser(${index}, this.value)">
                        <option value="">Select User</option>
                        ${users.map(user => `
                            <option value="${user.name}" ${item.assignedUser === user.name ? 'selected' : ''}>
                                ${user.name}
                            </option>
                        `).join('')}
                    </select>
                </td>
                <td>
                    <button onclick="editItem('${type}', ${index})">Edit</button>
                    <button onclick="deleteItem('${type}', ${index})">Delete</button>
                </td>
            `;
        }
        container.appendChild(row);
    });
}

function addItem(type) {
    if (type === 'admins' || type === 'users') {
        const name = prompt(`Enter ${type.slice(0, -1)} name:`);
        const email = prompt('Enter email:');
        const verified = confirm('Is the user verified?');

        if (name && email) {
            if (type === 'admins') {
                admins.push({ name, email, verified });
            } else {
                users.push({ name, email, verified });
            }
            renderList(type);
        }
    } else {
        const title = prompt('Enter task title:');
        const description = prompt('Enter task description:');
        const category = prompt('Enter task category:');
        const budget = parseFloat(prompt('Enter task budget:'));
        const deadline = prompt('Enter task deadline (YYYY-MM-DD):');
        const owner = prompt('Enter task owner (Admin):');
        const assignedUser = prompt('Enter assigned user:');

        if (title && description && category && budget && deadline && owner && assignedUser) {
            tasks.push({ title, description, category, budget, deadline, owner, assignedUser });
            renderList(type);
        }
    }
}

function editItem(type, index) {
    const list = type === 'admins' ? admins : type === 'users' ? users : tasks;
    const item = list[index];

    if (type === 'admins' || type === 'users') {
        const newName = prompt(`Edit ${type.slice(0, -1)} name:`, item.name);
        const newEmail = prompt('Edit email:', item.email);
        const newVerified = confirm('Is the user verified?');

        if (newName && newEmail) {
            list[index] = { name: newName, email: newEmail, verified: newVerified };
            renderList(type);
        }
    } else {
        const newTitle = prompt('Edit task title:', item.title);
        const newDescription = prompt('Edit task description:', item.description);
        const newCategory = prompt('Edit task category:', item.category);
        const newBudget = parseFloat(prompt('Edit task budget:', item.budget));
        const newDeadline = prompt('Edit task deadline (YYYY-MM-DD):', item.deadline);
        const newOwner = prompt('Edit task owner (Admin):', item.owner);
        const newAssignedUser = prompt('Edit assigned user:', item.assignedUser);

        if (newTitle && newDescription && newCategory && newBudget && newDeadline && newOwner && newAssignedUser) {
            tasks[index] = { title: newTitle, description: newDescription, category: newCategory, budget: newBudget, deadline: newDeadline, owner: newOwner, assignedUser: newAssignedUser };
            renderList(type);
        }
    }
}

function deleteItem(type, index) {
    if (confirm('Are you sure?')) {
        const list = type === 'admins' ? admins : type === 'users' ? users : tasks;
        list.splice(index, 1);
        renderList(type);
    }
}

function updateOwner(index, newOwner) {
    tasks[index].owner = newOwner;
    renderList('tasks');
}

function assignUser(index, userName) {
    tasks[index].assignedUser = userName;
    renderList('tasks');
}

showSection('admins');