const express = require('express');
const http = require('http');
const mongoose = require('mongoose');
const socketIo = require('socket.io');
const cors = require('cors');
require('dotenv').config();

const authMiddleware = require('./middleware/authMiddleware'); // Make sure this path is correct
const userRoutes = require('./Routes/userRoutes'); // Make sure this path is correct

// Initialize Express and HTTP server
const app = express();
const server = http.createServer(app);
const io = socketIo(server); // Initialize socket.io with the HTTP server

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public')); // Serve static files from the 'public' directory

// MongoDB Connection
console.log("DB " , process.env.MONGO_URI)
console.log("PORT ", process.env.PORT)
mongoose.connect(process.env.MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true
}).then(() => {
  console.log('MongoDB connected...');
}).catch((err) => {
  console.error('MongoDB connection error:', err);
});

// Routes
app.use('/api', userRoutes);
app.get('/', (req, res) => res.send('Hello World!'));
app.get('/protected-route', authMiddleware, (req, res) => {
  res.send("This is a protected route.");
});

// Socket.io connection and event handlers setup
io.on('connection', (socket) => {
  console.log('New WebSocket connection:', socket.id);

  // Simulate user authentication and associate the socket with a user ID
  socket.on('authenticate', (token) => {
    // TODO: Validate the token and extract user ID
    // For now, let's simulate with a fake user ID
    const userId = 'fakeUserId';
    socket.userId = userId;
  });

  // Handle private messages
  socket.on('privateMessage', ({ senderId, receiverId, message }) => {
    // TODO: You would normally verify senderId matches the authenticated user
    // Find the socket associated with the receiverId
    const receiverSocketId = Object.values(io.sockets.sockets).find(
      (s) => s.userId === receiverId
    )?.id;

    if (receiverSocketId) {
      io.to(receiverSocketId).emit('privateMessage', { senderId, message });
    }
  });

  socket.on('disconnect', () => {
    console.log(`User with ID ${socket.userId} disconnected`);
    // Perform any cleanup if necessary
  });
});

// Start the server
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
