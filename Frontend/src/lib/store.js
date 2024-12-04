import { writable } from 'svelte/store';

const initialState = {
  roomCode: null,
  isHost: false,
  playerId: null,
  players: {},
  currentPlayer: null,
  currentQuestion: null,
  selectedCategory: null,
  selectedDifficulty: null,
  pointsToWin: 1,
  timeLeft: 30,
  answers: [],
  scores: {},
  winnerPlayer: null,
  error: null,
  gamePhase: 'lobby', // lobby, choosing, question, answer, leaderboard, winner
};

export const gameState = writable(initialState);

// Helper function to reset game state
export function resetGame() {
  gameState.set(initialState);
}