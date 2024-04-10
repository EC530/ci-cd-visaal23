// profile.js

document.addEventListener('DOMContentLoaded', function () {
  const profilePicture = document.getElementById('profile-picture');
  const usernameDisplay = document.getElementById('username');
  const addContactButton = document.getElementById('add-contact-button');
  const contactUsernameInput = document.getElementById('contact-username');

  // Function to fetch and display the user profile
  function fetchUserProfile() {
    const token = localStorage.getItem('token'); // Retrieve the token from local storage

    // Check if the token is available
    if (!token) {
      window.location.href = 'login.html'; // If no token, redirect to the login page
      return;
    }

    // Fetch the user profile from the backend
    fetch('/api/profile', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}` // Use the token for authorization
      }
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Profile fetch failed');
      }
      return response.json();
    })
    .then(profile => {
      // Set the user's profile data on the page
      usernameDisplay.textContent = profile.username;
      profilePicture.src = profile.pictureUrl || 'default-avatar.png'; // Use a default picture if none is provided
    })
    .catch(error => {
      console.error('Error fetching profile:', error);
    });
  }

  // Function to handle adding a new contact
  function addContact() {
    const contactUsername = contactUsernameInput.value.trim();
    const token = localStorage.getItem('token');

    // Check if there is a contact username entered
    if (!contactUsername) {
      alert('Please enter a username to add.');
      return;
    }

    // Send the request to add a new contact
    fetch('/api/add-contact', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      // Correct the property name according to your server's expected request body
    body: JSON.stringify({ username: contactUsername })

    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Add contact failed');
      }
      return response.json();
    })
    .then(data => {
      alert('Contact added successfully!');
      contactUsernameInput.value = ''; // Clear the input after adding
    })
    .catch(error => {
      console.error('Error adding contact:', error);
    });
  }

  // Event listener for the add contact button
  addContactButton.addEventListener('click', addContact);

  // Fetch and display the user profile on initial load
  fetchUserProfile();
});
