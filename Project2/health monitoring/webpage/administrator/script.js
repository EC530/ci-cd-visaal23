function searchUser() {
    const searchTerm = document.getElementById('userSearch').value;
    // API request to search users
    fetch(`https://api.example.com/search_users?query=${searchTerm}`)
    .then(response => response.json())
    .then(data => {
        const userList = document.querySelector('.user-list');
        userList.innerHTML = ''; // Clear existing users
        data.forEach(user => {
            const userDiv = document.createElement('div');
            userDiv.textContent = user.name;
            userDiv.onclick = () => showUserDetails(user);
            userList.appendChild(userDiv);
        });
    });
}

function showUserDetails(user) {
    const detailsContent = document.getElementById('detailsContent');
    detailsContent.innerHTML = `<h3>${user.name}</h3>
                                <p>Roles: ${user.roles.join(', ')}</p>
                                <button onclick="changeRoles(${user.id})">Change Roles</button>
                                <button onclick="disableUser(${user.id})">Disable</button>
                                <button onclick="deleteUser(${user.id})">Delete</button>`;
}

function changeRoles(userId) {
    // Function to change roles
}

function disableUser(userId) {
    // Function to disable user
}

function deleteUser(userId) {
    // Function to delete user
}
