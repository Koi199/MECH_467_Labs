import numpy as np

def deriv(U, Ts):
    """
    Compute discrete-time derivative estimates using 5-point stencil
    (with special handling for edges and short signals).

    Parameters
    ----------
    U : array_like, shape (N,) or (N, M)
        Input signal(s). Each column is treated as a separate signal.
    Ts : float
        Sampling time.

    Returns
    -------
    V : ndarray, shape (N, M)
        Estimated derivatives.
    """
    U = np.atleast_2d(U)
    ist = False
    if U.shape[0] == 1:   # row vector -> column
        U = U.T
        ist = True

    ly, ncols = U.shape
    V = np.zeros_like(U, dtype=float)

    # Case: only 2 points
    if ly == 2:
        V[0, :] = U[1, :] - U[0, :]
        V[1, :] = V[0, :]
        V = V / Ts
        return V.T if ist else V

    # Case: less than 5 points (but >2)
    if ly < 5:
        V[1:ly-1, :] = (U[2:ly, :] - U[0:ly-2, :]) / 2.0
        V[0, :] = 2*U[1, :] - 1.5*U[0, :] - 0.5*U[2, :]
        V[ly-1, :] = 1.5*U[ly-1, :] - 2*U[ly-2, :] + 0.5*U[ly-3, :]
        V = V / Ts
        return V.T if ist else V

    # Case: 5 points or more
    Cde = np.array([[-25/12, 4, -3, 4/3, -1/4],
                    [-1/4, -5/6, 3/2, -1/2, 1/12]])
    Cd = np.array([1/12, -2/3, 0, 2/3, -1/12])

    # First two rows
    V[0:2, :] = Cde @ U[0:5, :]
    # Last two rows (explicit indexing instead of tricky slice)
    V[[ly-1, ly-2], :] = (-np.fliplr(Cde)) @ U[ly-5:ly, :]

    # Interior rows (vectorised)
    V[2:ly-2, :] = (Cd[0]*U[0:ly-4, :] +
                    Cd[1]*U[1:ly-3, :] +
                    Cd[2]*U[2:ly-2, :] +
                    Cd[3]*U[3:ly-1, :] +
                    Cd[4]*U[4:ly, :])

    V = V / Ts
    return V.T if ist else V
