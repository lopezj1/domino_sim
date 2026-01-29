"""Game orchestrator: discrete event simulation loop for domino game."""

from typing import List, Tuple
from dataclasses import replace

from ..models.game_state import GameState
from ..models.move import Move
from ..models.events import Event
from ..models.tile import Tile
from ..models.result import GameOutcome
from ..engine.rules import validate_play_move, calculate_round_winner, calculate_round_score
from ..strategy.base import Strategy


class Game:
    """
    Discrete event simulation (DES) orchestrator for domino game.
    
    Maintains:
    - Immutable game state
    - Event queue (ordered by timestamp)
    - Strategy interface for player decision-making
    - Deterministic game flow (same seed → same outcome)
    """
    
    def __init__(
        self,
        initial_state: GameState,
        player_0_strategy: Strategy,
        player_1_strategy: Strategy,
        seed: int,
    ):
        """
        Initialize game with initial state and strategies.
        
        Args:
            initial_state: Starting GameState (after deal)
            player_0_strategy: Strategy for player 0
            player_1_strategy: Strategy for player 1
            seed: RNG seed for reproducibility
        """
        self.state = initial_state
        self.strategies = [player_0_strategy, player_1_strategy]
        self.seed = seed
        self.events: List[Event] = []
        self.turn_count = 0
    
    def play_round(self) -> bool:
        """
        Play a single round (exchange of turns until someone can't play).
        
        Returns:
            True if round continues, False if round ends
        """
        consecutive_passes = 0
        
        while consecutive_passes < 2:
            # Get legal moves for current player
            legal_moves = self.state.get_legal_moves()
            strategy = self.strategies[self.state.current_player]
            
            # Choose move
            move = strategy.choose_move(self.state, legal_moves)
            
            # Record event
            event_timestamp = len(self.events)
            event = Event(
                type=move.action,
                timestamp=event_timestamp,
                data={
                    "player": self.state.current_player,
                    "move": {
                        "action": move.action,
                        "tile": move.tile.id if move.tile else None,
                    },
                },
            )
            self.events.append(event)
            
            # Update state based on move
            if move.action == "play":
                self.state = self._apply_play_move(move)
                consecutive_passes = 0
                self.turn_count += 1
            elif move.action == "draw":
                self.state = self._apply_draw_move()
                consecutive_passes = 0
            elif move.action == "pass":
                consecutive_passes += 1
                self.state = replace(self.state, current_player=1 - self.state.current_player)
            
            # Check if board is playable (don't end round if only 1 pass)
            if consecutive_passes >= 2:
                break
        
        return consecutive_passes < 2
    
    def _apply_play_move(self, move: Move) -> GameState:
        """Apply a play move, updating board and hand."""
        if move.tile is None:
            raise ValueError("Play move must have a tile")
        
        if not validate_play_move(move, self.state):
            raise ValueError(f"Invalid play move: {move}")
        
        tile = move.tile
        current_hand = list(self.state.players_hands[self.state.current_player])
        current_hand.remove(tile)
        
        # Add tile to board
        new_board = list(self.state.board)
        if not new_board:
            new_board.append(tile)
        else:
            # Check which end matches and place appropriately
            left_end = self.state.board[0].pips_a
            right_end = self.state.board[-1].pips_b
            
            if tile.pips_a == right_end:
                new_board.append(tile)
            elif tile.pips_b == right_end:
                new_board.append(tile.flip())
            elif tile.pips_a == left_end:
                new_board.insert(0, tile.flip())
            elif tile.pips_b == left_end:
                new_board.insert(0, tile)
            else:
                raise ValueError(f"Tile {tile} doesn't match board endpoints")
        
        # Update player hands
        new_hands = list(self.state.players_hands)
        new_hands[self.state.current_player] = tuple(current_hand)
        
        # Switch to next player
        next_player = 1 - self.state.current_player
        
        return replace(
            self.state,
            players_hands=tuple(new_hands),
            board=tuple(new_board),
            current_player=next_player,
        )
    
    def _apply_draw_move(self) -> GameState:
        """Apply a draw move, drawing from boneyard."""
        if not self.state.boneyard:
            raise ValueError("Cannot draw from empty boneyard")
        
        # Draw first tile from boneyard
        drawn_tile = self.state.boneyard[0]
        new_boneyard = self.state.boneyard[1:]
        
        # Add to current player's hand
        current_hand = list(self.state.players_hands[self.state.current_player])
        current_hand.append(drawn_tile)
        
        new_hands = list(self.state.players_hands)
        new_hands[self.state.current_player] = tuple(current_hand)
        
        # Switch to next player
        next_player = 1 - self.state.current_player
        
        return replace(
            self.state,
            players_hands=tuple(new_hands),
            boneyard=new_boneyard,
            current_player=next_player,
        )
    
    def play_game(self, max_rounds: int = 100) -> GameOutcome:
        """
        Play complete game until one player wins.
        
        Winner is first to reach 100 points (via round scoring).
        
        Args:
            max_rounds: Safety limit (prevents infinite loops)
        
        Returns:
            GameOutcome with result, seed, and event trace
        """
        # Add initial deal event
        self.events.append(Event(type="deal", timestamp=0, data={"seed": self.seed}))
        
        rounds_played = 0
        while self.state.scores[0] < 100 and self.state.scores[1] < 100 and rounds_played < max_rounds:
            self.play_round()
            rounds_played += 1
            
            # End round: calculate winner and score
            round_winner = calculate_round_winner(
                self.state.players_hands[0],
                self.state.players_hands[1],
            )
            loser_id = 1 - round_winner
            points = calculate_round_score(
                round_winner,
                self.state.players_hands[loser_id],
            )
            
            # Update scores
            new_scores = list(self.state.scores)
            new_scores[round_winner] += points
            
            # Record round end event
            self.events.append(Event(
                type="round_end",
                timestamp=len(self.events),
                data={
                    "round": self.state.round_num,
                    "winner": round_winner,
                    "points": points,
                    "scores": tuple(new_scores),
                },
            ))
            
            # Prepare for next round
            self.state = replace(
                self.state,
                scores=tuple(new_scores),
                round_num=self.state.round_num + 1,
                board=tuple(),  # Clear board
                current_player=0,  # Reset to player 0
            )
        
        # Game over: record final event
        winner_id = 0 if self.state.scores[0] > self.state.scores[1] else 1
        winner_strategy = self.strategies[winner_id].name
        score_diff = abs(self.state.scores[0] - self.state.scores[1])
        
        self.events.append(Event(
            type="game_end",
            timestamp=len(self.events),
            data={
                "winner": winner_id,
                "winner_strategy": winner_strategy,
                "final_scores": self.state.scores,
                "score_differential": score_diff,
            },
        ))
        
        return GameOutcome(
            winner=winner_strategy,
            score_differential=score_diff,
            turns=self.turn_count,
            seed=self.seed,
            trace=self.events,
        )
