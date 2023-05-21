from statsautochess.piece.ptype import PieceType
from statsautochess.piece.chesspiece import ChessPiece
from statsautochess.const.collections import PIECES_PER_LEVEL
from collections import defaultdict
from typing import List, Dict

def ban_piece(piece_type: PieceType, collections: List[ChessPiece]) -> List[ChessPiece]:
    res = []
    for piece in collections:
        if piece_type not in piece.piece_types:
            res.append(piece)
    return res

def collections2dict(collections: List[ChessPiece]) -> Dict[PieceType, Dict[int, List[ChessPiece]]]:
    res: Dict[PieceType, Dict[int, List[ChessPiece]]] = defaultdict(dict)
    for piece in collections:
        for piece_type in piece.piece_types:
            if piece.level not in res[piece_type]:
                res[piece_type][piece.level] = []
            res[piece_type][piece.level].append(piece)
    return res

def collections2stats(collections: List[ChessPiece]) -> Dict[PieceType, Dict[int, float]]:
    piece_dict = collections2dict(collections)
    collection_stats: Dict[PieceType, Dict[int, float]] = defaultdict(dict)

    for piece_type, level_info in piece_dict.items():
        for level, pieces in level_info.items():
            if level not in collection_stats[piece_type]:
                collection_stats[piece_type][level] = 0.0
            collection_stats[piece_type][level] = len(pieces) / PIECES_PER_LEVEL[level-1]
    return collection_stats

def summarize(collections: List[ChessPiece]) -> None:
    collection_stats = collections2stats(collections)
    
    for piece_type, level_stats in collection_stats.items():
        print(piece_type.name)
        for level, prob in level_stats.items():
            print(f"{level}: {prob*100:.2f}%".rjust(4, ' '))

def compare(collections: List[ChessPiece], ref_collections: List[ChessPiece]) -> None:
    stats_dict = collections2stats(collections)
    ref_dict = collections2stats(ref_collections)

    for piece_type in ref_dict.keys():
        print(piece_type.name)
        for level in ref_dict[piece_type].keys():
            ref_percent = ref_dict[piece_type][level] * 100.0
            stats_percent = 0.0
            if piece_type in stats_dict and level in stats_dict[piece_type]:
                stats_percent = stats_dict[piece_type][level] * 100.0
            diff = stats_percent - ref_percent
            if diff >= 0.0:
                print(f"{level}: {ref_percent:<5.2f}% -> {stats_percent:<5.2f}% {'':<2} (+{diff:.2f}%)")
            else:
                print(f"{level}: {ref_percent:<5.2f}% -> {stats_percent:<5.2f}% {'':<2} ({diff:.2f}%)")
