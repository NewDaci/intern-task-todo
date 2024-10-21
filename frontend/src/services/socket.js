// src/services/socket.js
import { io } from "socket.io-client";

const socket = io('http://localhost:5000', {
    reconnection: false, // Disable automatic reconnections
  });

export default socket;
