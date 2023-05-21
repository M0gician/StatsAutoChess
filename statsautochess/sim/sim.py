from numba import jit, prange
import numpy as np

@jit(nopython=True, parallel=True)
def sim_upgrade_one_piece(
        n_trials: int,
        n_pieces: int,
        threshold: int,
        total_target_pieces: int,
        target_draw_prob: float,
        total_pieces: np.ndarray,
        target_piece_level: int
    ):
    """
    Compute mean, max, min, and standard deviation of the number of pieces needed to upgrade a piece to three star.
    n_trials: number of trials for simulataion
    n_pieces: number of target piece one currently have
    total_target_pieces: total number of target pieces in the pool
    target_draw_prob: probability of drawing the target piece
    total_pieces: total number of pieces in the pool
    target_piece_level: level of the target piece
    """

    res = [0 for _ in range(n_trials)]

    for i in prange(n_trials):
        n_draws = 0
        curr_pieces = n_pieces
        while curr_pieces < threshold:
            target_prob = (total_target_pieces - curr_pieces) / (total_pieces[target_piece_level-1] - curr_pieces)
            target_prob *= target_draw_prob
            cands = [0 if np.random.random() >= target_prob else 1 for _ in range(5)]
            curr_pieces += np.sum(np.array(cands))
            n_draws += 1
        res[i] = n_draws

    return res


