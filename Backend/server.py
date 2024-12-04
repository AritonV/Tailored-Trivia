import json
import random
import string
import time

import ollama
from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store active games and their players
games = {}
pervious_questions = [{}]

# Load previous questions
with open('previous_questions.json', 'r') as f:
  pervious_questions = json.load(f)


def generate_question(category, difficulty):
  """Generate a random question"""
  prompt = """
  You are a trivia question generator. Given a category and difficulty level, generate a unique, interesting trivia question following these requirements:

  1. The question must be factually accurate and verifiable
  2. The question should be appropriately challenging for the given difficulty level
  3. Include exactly 4 multiple choice answers, with only one correct answer
  4. All incorrect answers (distractors) should be plausible and related to the topic
  5. Order the options randomly, don't always put the correct answer first
  6. Format the output as a JSON object with these exact fields:
    - category: the provided category
    - difficulty: the provided difficulty level
    - question: the trivia question text
    - answers: array of 4 answer choices
    - correct_answer: the correct answer (matching one of the options exactly)
    
  Example input:
  Category: Science
  Difficulty: Medium

  Example output:
  {
      "category": "Science",
      "difficulty": "Medium",
      "question": "What is the most abundant element in the Earth's atmosphere?",
      "options": [
          "Oxygen",
          "Nitrogen",
          "Carbon dioxide",
          "Argon"
      ],
      "correct_answer": "Nitrogen",
  }

  Here are the previously generated questions:

  """ + f"""
  {json.dumps(pervious_questions, indent=2)}
  """ + f"""

  Generate one unique trivia question with the following parameters:
  Category: {category}
  Difficulty: {difficulty}

  ONLY RETURN THE JSON OBJECT NOTING ELSE
  """
  return json.loads(ollama.generate(model="llama3.1", prompt=prompt)["response"])


def generate_room_code():
  """Generate a unique 4-character room code"""
  while True:
    code = ''.join(random.choices(string.ascii_uppercase, k=4))
    if code not in games:
      return code


def check_all_answers_submitted(game):
  """Check if all players have submitted answers"""
  points = game['points_to_win'] - 1
  answers = game['answers']
  if len(answers) == len(game['players']):
    max_score_players = 0
    for player_id, answer in answers.items():
      if game["players"][player_id]['score'] == points and answer:
        max_score_players += 1
      if max_score_players > 1:
        break
    if max_score_players > 1:
      for player_id, answer in answers.items():
        if answer and not game["players"][player_id]["score"] == points:
          game["players"][player_id]["score"] += 1
        else:
          answers[player_id] = False
    elif max_score_players <= 1:
      for player_id, answer in answers.items():
        if answer:
          game["players"][player_id]["score"] += 1
    return True
  return False


@socketio.on('create_game')
def handle_create_game():
  """Handle game creation"""
  host_id = request.sid
  room_code = generate_room_code()

  games[room_code] = {
      'host': host_id,
      'players': {},
      'answers': {},
      'state': 'lobby',
      'max_players': 8,
      'points_to_win': 1
  }

  join_room(room_code)
  emit('game_created', {
      'room_code': room_code
  })


@socketio.on('join_game')
def handle_join_game(data):
  """Handle player joining a game"""
  room_code = data['room_code']
  player_id = request.sid

  if room_code not in games:
    emit('error', {'message': 'Game not found'})
    return

  game = games[room_code]

  if len(game['players']) >= game['max_players']:
    emit('error', {'message': 'Game is full'})
    return

  if game['state'] != 'lobby':
    emit('error', {'message': 'Game already in progress'})
    return

  game['players'][player_id] = {
      'name': data['name'],
      'score': 0
  }

  join_room(room_code)

  # Notify everyone in the room about the new player
  emit('player_joined', {
      'player_id': player_id,
      'name': data['name']
  }, room=room_code)

  # Send current game state to the new player
  emit('game_joined', {
      'room_code': room_code,
      'player_id': player_id,
      'is_host': False,
      'players': game['players']
  })


@socketio.on('disconnect')
def handle_disconnect():
  """Handle player disconnection"""
  for room_code in games:
    game = games[room_code]
    if request.sid in game['players']:
      # Remove player from game
      player_name = game['players'][request.sid]['name']
      del game['players'][request.sid]

      # If host disconnects, end game
      if request.sid == game['host']:
        emit('game_ended', {'message': 'Host disconnected'}, room=room_code)
        del games[room_code]
      else:
        # Notify others about disconnection
        emit('player_left', {
            'player_id': request.sid,
            'name': player_name
        }, room=room_code)

      leave_room(room_code)
      break


@socketio.on('start_game')
def handle_start_game(data):
  """Handle game start"""
  room_code = data['room_code']

  if room_code not in games:
    emit('error', {'message': 'Game not found'})
    return

  game = games[room_code]

  current_player = random.choice(list(game['players'].keys()))
  game['currentPlayer'] = current_player
  game["state"] = "choosing"
  print(game)

  emit('game_started', {
      'currentPlayer': game['currentPlayer']
  }, room=room_code)


@socketio.on('category_selected')
def handle_category_selected(data):
  """Handle category selection"""
  room_code = data['room_code']
  category = data['category']
  difficulty = data['difficulty']

  if room_code not in games:
    emit('error', {'message': 'Game not found'})
    return

  emit('category_recieved', {
      'category': category,
      'difficulty': difficulty
  }, room=room_code)

  game = games[room_code]

  question = generate_question(category, difficulty)
  print("\n\n", question, "\n\n")

  pervious_questions.append(question)
  with open('previous_questions.json', 'w') as f:
    json.dump(pervious_questions, f, indent=2)

  emit('question_generated', {
    'question': question
  }, room=room_code)


@socketio.on('start_timer')
def handle_start_timer(data):
  """Handle timer start"""
  room_code = data['room_code']
  time_left = data['time']
  while True:
    emit('timer_update', {
        'timeLeft': time_left
    }, room=room_code)
    time.sleep(1)
    if time_left == 0:
      break
    time_left -= 1


@socketio.on('answer_submitted')
def handle_answer_submitted(data):
  """Handle answer submission"""
  room_code = data['room_code']
  player_id = data['player_id']
  answer = data['answer']
  correct_answer = data['correct_answer']

  if room_code not in games:
    emit('error', {'message': 'Game not found'})
    return

  game = games[room_code]

  if player_id not in game['players']:
    emit('error', {'message': 'Player not found'})
    return

  if answer == correct_answer:
    game['answers'][player_id] = True
  else:
    game['answers'][player_id] = False

  if check_all_answers_submitted(game):
    emit('round_ended', {
        'room_code': room_code,
        'scores': game['answers']
    }, room=room_code)
    game['answers'] = {}


if __name__ == '__main__':
  socketio.run(app, host='0.0.0.0', debug=True)
