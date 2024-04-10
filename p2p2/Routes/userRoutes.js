const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const express = require('express');
const router = express.Router();
const User = require('../models/User'); // Path to the User model
const authMiddleware = require('../middleware/authMiddleware'); // Path to the auth middleware

// POST endpoint for user registration
router.post('/register', async (req, res) => {
  try {
    // Hash the password with a salt round of 10
    const hashedPassword = await bcrypt.hash(req.body.password, 10);
    // Create a new user instance and save it to the database
    const newUser = new User({
      username: req.body.username,
      password: hashedPassword,
    });

    await newUser.save();
    res.status(201).send("User registered successfully.");
  } catch (error) {
    // Check for duplicate username error
    if (error.code === 11000) {
      return res.status(400).send("Username already taken.");
    }
    // Generic error fallback
    res.status(500).send(error.message);
  }
});

// POST endpoint for user login
router.post('/login', async (req, res) => {
  // Find the user by their username
  const user = await User.findOne({ username: req.body.username });
  if (user) {
    // Compare the submitted password with the hashed password in the database
    const passwordMatch = await bcrypt.compare(req.body.password, user.password);
    if (passwordMatch) {
      // Generate a JWT token
      const token = jwt.sign(
        { userId: user._id },
        process.env.JWT_SECRET, // Make sure to define JWT_SECRET in your .env file
        { expiresIn: '24h' } // Token expires in 24 hours
      );

      res.json({ message: "Login successful", token });
    } else {
      // Incorrect password
      res.status(401).send("Invalid username or password.");
    }
  } else {
    // User not found
    res.status(401).send("Invalid username or password.");
  }
});

// GET endpoint for user profile, protected by authMiddleware

// Existing registration and login routes here...

// GET user profile
router.get('/profile', authMiddleware, async (req, res) => {
  try {
    // authMiddleware should add the user's ID to the request object
    const user = await User.findById(req.user.id).populate('contacts', 'username');
    if (!user) {
      return res.status(404).send('User not found');
    }
    // Return the user profile and contacts
    res.json({
      username: user.username,
      email: user.email,
      contacts: user.contacts
    });
  } catch (error) {
    res.status(500).send('Server error');
  }
});

// POST add a contact
router.post('/add-contact', authMiddleware, async (req, res) => {
  try {
    const userId = req.user.id;
    const contactUsername = req.body.username;

    const user = await User.findById(userId);
    const contactToAdd = await User.findOne({ username: contactUsername });

    if (!contactToAdd) {
      return res.status(404).send('User to add as contact not found');
    }

    // Check if the user is already in the contacts list
    if (user.contacts.includes(contactToAdd._id)) {
      return res.status(400).send('User already in contacts list');
    }

    // Add the user to the contacts list
    user.contacts.push(contactToAdd);
    await user.save();

    res.status(200).send('Contact added successfully');
  } catch (error) {
    res.status(500).send('Server error');
  }
});

module.exports = router;
