from statsautochess.piece.ptype import PieceType

class Piece:
    def __init__(self, name: str, piece_types: PieceType, level: int) -> None:
        self.name = name
        self.piece_types = piece_types
        self.level = level
