import { io } from 'socket.io-client';
import { writable } from 'svelte/store';
import { gameState } from './store';

export const socket = io('http://192.168.18.5:5000');

socket.on('connect', () => {
  console.log('Connected to server');
});

// Host events
socket.on('game_created', (data) => {
  gameState.update((state) => ({
    ...state,
    roomCode: data.room_code,
    isHost: true,
    error: null
  }));
});

socket.on('player_joined', (data) => {
  gameState.update((state) => ({
    ...state,
    players: {
      ...state.players,
      [data.player_id]: {
        name: data.name,
        score: 0
      }
    }
  }));
  console.log(gameState.players);
});

// Remove player from game
socket.on('player_left', (data) => {
  gameState.update(state => ({
    ...state,
    players: {
      ...state.players,
      [data.player_id]: null
    }
  }));
});

// Player events
socket.on('game_joined', (data) => {
  gameState.update((state) => ({
    ...state,
    roomCode: data.room_code,
    playerId: data.player_id,
    players: data.players,
    isHost: false,
    error: null
  }));
});

socket.on('game_started', (data) => {
  gameState.update(state => ({
    ...state,
    gamePhase: 'choosing',
    currentPlayer: data.currentPlayer
  }));
});

socket.on('category_recieved', (data) => {
  gameState.update(state => ({
    ...state,
    selectedCategory: data.category,
    selectedDifficulty: data.difficulty,
    gamePhase: 'generating'
  }));
});

socket.on('question_generated', (data) => {
  gameState.update(state => ({
    ...state,
    gamePhase: 'question',
    currentQuestion: data.question,
    answers: data.answers
  }));
});

socket.on('timer_update', (data) => {
  gameState.update(state => ({
    ...state,
    timeLeft: data.timeLeft
  }));
});

socket.on('answer_submitted', (data) => {
  gameState.update(state => ({
    ...state,
    answers: [...state.answers, data]
  }));
});

socket.on('round_ended', (data) => {
  gameState.update(state => ({
    ...state,
    scores: data.scores,
    gamePhase: "results"
  }));
});

socket.on('game_ended', (data) => {
  gameState.update(state => ({
    ...state,
    gamePhase: 'winner',
    winnerPlayer: data.winner
  }));
});

socket.on('error', (data) => {
  gameState.update((state) => ({
    ...state,
    error: data.message
  }));
});