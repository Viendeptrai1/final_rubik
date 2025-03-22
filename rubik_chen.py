class RubikState:
    def __init__(self, cp, co, ep, eo):
        self.cp = cp  # Hoán vị góc
        self.co = co  # Định hướng góc
        self.ep = ep  # Hoán vị cạnh
        self.eo = eo  # Định hướng cạnh

    def __eq__(self, other):
        return (self.cp == other.cp and self.co == other.co and
                self.ep == other.ep and self.eo == other.eo)

    def __hash__(self):
        return hash((tuple(self.cp), tuple(self.co), tuple(self.ep), tuple(self.eo)))

    def copy(self):
        return RubikState(self.cp.copy(), self.co.copy(), self.ep.copy(), self.eo.copy())

# Trạng thái mục tiêu
SOLVED_STATE = RubikState(
    cp=[0, 1, 2, 3, 4, 5, 6, 7],
    co=[0, 0, 0, 0, 0, 0, 0, 0],
    ep=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    eo=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
)

# Định nghĩa các nước đi
MOVES = {
    # Mặt phải (R)
    "R": {
        "cp_perm": [3, 1, 2, 6, 0, 5, 4, 7],  # urf -> urb -> drb -> drf -> urf
        "co_change": [1, 0, 0, 2, 2, 0, 1, 0],  # Định hướng thay đổi
        "ep_perm": [11, 1, 2, 3, 8, 5, 6, 7, 4, 9, 10, 0],  # ur -> rb -> dr -> fr -> ur
        "eo_change": [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1]
    },
    "R'": {
        "cp_perm": [4, 1, 2, 0, 6, 5, 3, 7],
        "co_change": [2, 0, 0, 1, 1, 0, 2, 0],
        "ep_perm": [0, 1, 2, 3, 8, 5, 6, 7, 4, 9, 10, 11],
        "eo_change": [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1]
    },
    "R2": {
        "cp_perm": [6, 1, 2, 4, 3, 5, 0, 7],  # Thực hiện R hai lần
        "co_change": [0, 0, 0, 0, 0, 0, 0, 0],  # Tổng thay đổi định hướng là 0
        "ep_perm": [4, 1, 2, 3, 0, 5, 6, 7, 11, 9, 10, 8],
        "eo_change": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    },

    # Mặt trái (L)
    "L": {
        "cp_perm": [0, 1, 5, 3, 4, 7, 6, 2],  # ulf -> dlb -> dlf -> ulf
        "co_change": [0, 0, 1, 0, 0, 2, 0, 1],
        "ep_perm": [0, 1, 9, 3, 4, 5, 10, 7, 8, 6, 2, 11],  # ul -> fl -> dl -> bl -> ul
        "eo_change": [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0]
    },
    "L'": {
        "cp_perm": [0, 1, 7, 3, 4, 2, 6, 5],
        "co_change": [0, 0, 2, 0, 0, 1, 0, 2],
        "ep_perm": [0, 1, 10, 3, 4, 5, 9, 7, 8, 2, 6, 11],
        "eo_change": [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0]
    },
    "L2": {
        "cp_perm": [0, 1, 5, 3, 4, 7, 6, 2],
        "co_change": [0, 0, 0, 0, 0, 0, 0, 0],
        "ep_perm": [0, 1, 6, 3, 4, 5, 2, 7, 8, 10, 9, 11],
        "eo_change": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    },

    # Mặt trên (U)
    "U": {
        "cp_perm": [1, 2, 3, 0, 4, 5, 6, 7],  # urf -> ufr -> ulf -> ubr -> urf
        "co_change": [0, 0, 0, 0, 0, 0, 0, 0],
        "ep_perm": [1, 2, 3, 0, 4, 5, 6, 7, 8, 9, 10, 11],  # ur -> uf -> ul -> ub -> ur
        "eo_change": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    },
    "U'": {
        "cp_perm": [3, 0, 1, 2, 4, 5, 6, 7],
        "co_change": [0, 0, 0, 0, 0, 0, 0, 0],
        "ep_perm": [3, 0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11],
        "eo_change": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    },
    "U2": {
        "cp_perm": [2, 3, 0, 1, 4, 5, 6, 7],
        "co_change": [0, 0, 0, 0, 0, 0, 0, 0],
        "ep_perm": [2, 3, 0, 1, 4, 5, 6, 7, 8, 9, 10, 11],
        "eo_change": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    },

    # Mặt dưới (D)
    "D": {
        "cp_perm": [0, 1, 2, 3, 7, 4, 5, 6],  # dfr -> dlf -> dlb -> dbr -> dfr
        "co_change": [0, 0, 0, 0, 0, 0, 0, 0],
        "ep_perm": [0, 1, 2, 3, 5, 6, 7, 4, 8, 9, 10, 11],  # dr -> df -> dl -> db -> dr
        "eo_change": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    },
    "D'": {
        "cp_perm": [0, 1, 2, 3, 5, 6, 7, 4],
        "co_change": [0, 0, 0, 0, 0, 0, 0, 0],
        "ep_perm": [0, 1, 2, 3, 7, 4, 5, 6, 8, 9, 10, 11],
        "eo_change": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    },
    "D2": {
        "cp_perm": [0, 1, 2, 3, 6, 7, 4, 5],
        "co_change": [0, 0, 0, 0, 0, 0, 0, 0],
        "ep_perm": [0, 1, 2, 3, 6, 7, 4, 5, 8, 9, 10, 11],
        "eo_change": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    },

    # Mặt trước (F)
    "F": {
        "cp_perm": [1, 4, 2, 3, 7, 5, 6, 0],  # urf -> ufr -> dfr -> dlf -> urf
        "co_change": [1, 2, 0, 0, 1, 0, 0, 2],
        "ep_perm": [0, 8, 2, 3, 4, 9, 6, 7, 5, 1, 10, 11],  # uf -> fr -> df -> fl -> uf
        "eo_change": [0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0]
    },
    "F'": {
        "cp_perm": [7, 0, 2, 3, 1, 5, 6, 4],
        "co_change": [2, 1, 0, 0, 2, 0, 0, 1],
        "ep_perm": [0, 9, 2, 3, 4, 8, 6, 7, 1, 5, 10, 11],
        "eo_change": [0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0]
    },
    "F2": {
        "cp_perm": [4, 7, 2, 3, 0, 5, 6, 1],
        "co_change": [0, 0, 0, 0, 0, 0, 0, 0],
        "ep_perm": [0, 5, 2, 3, 4, 1, 6, 7, 9, 8, 10, 11],
        "eo_change": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    },

    # Mặt sau (B)
    "B": {
        "cp_perm": [0, 1, 3, 6, 4, 2, 5, 7],  # ubr -> dbr -> dlb -> ulf -> ubr
        "co_change": [0, 0, 2, 1, 0, 1, 2, 0],
        "ep_perm": [0, 1, 2, 10, 4, 5, 6, 11, 8, 9, 7, 3],  # ub -> bl -> db -> br -> ub
        "eo_change": [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1]
    },
    "B'": {
        "cp_perm": [0, 1, 5, 2, 4, 6, 3, 7],
        "co_change": [0, 0, 1, 2, 0, 2, 1, 0],
        "ep_perm": [0, 1, 2, 11, 4, 5, 6, 10, 8, 9, 3, 7],
        "eo_change": [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1]
    },
    "B2": {
        "cp_perm": [0, 1, 6, 5, 4, 3, 2, 7],
        "co_change": [0, 0, 0, 0, 0, 0, 0, 0],
        "ep_perm": [0, 1, 2, 7, 4, 5, 6, 3, 8, 9, 11, 10],
        "eo_change": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    }
}

MOVE_NAMES = list(MOVES.keys())

# Hàm áp dụng một nước đi
def apply_move(state, move):
    new_state = state.copy()
    move_data = MOVES[move]

    # Áp dụng hoán vị góc
    new_cp = [0] * 8
    for i in range(8):
        new_cp[i] = state.cp[move_data["cp_perm"][i]]
    new_state.cp = new_cp

    # Áp dụng thay đổi định hướng góc
    new_co = [0] * 8
    for i in range(8):
        new_co[i] = (state.co[move_data["cp_perm"][i]] + move_data["co_change"][i]) % 3
    new_state.co = new_co

    # Áp dụng hoán vị cạnh
    new_ep = [0] * 12
    for i in range(12):
        new_ep[i] = state.ep[move_data["ep_perm"][i]]
    new_state.ep = new_ep

    # Áp dụng thay đổi định hướng cạnh
    new_eo = [0] * 12
    for i in range(12):
        new_eo[i] = (state.eo[move_data["ep_perm"][i]] + move_data["eo_change"][i]) % 2
    new_state.eo = new_eo

    return new_state
def calculate_parity(perm):
    """Tính dấu hoán vị (chẵn: 0, lẻ: 1)"""
    inversions = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            if perm[i] > perm[j]:
                inversions += 1
    return inversions % 2

def heuristic(state):
    # Heuristic cho các khối góc
    corner_misplaced = sum(1 for i in range(8) if state.cp[i] != i)
    corner_misoriented = sum(1 for i in range(8) if state.co[i] != 0)
    corner_total = corner_misplaced + corner_misoriented  # Tổng số lỗi của các khối góc
    h_corner = corner_total // 4  # Mỗi nước đi sửa tối đa 4 khối

    # Heuristic cho các khối cạnh
    edge_misplaced = sum(1 for i in range(12) if state.ep[i] != i)
    edge_misoriented = sum(1 for i in range(12) if state.eo[i] != 0)
    edge_total = edge_misplaced + edge_misoriented
    h_edge = edge_total // 4

    # Heuristic cho dấu hoán vị
    corner_parity = calculate_parity(state.cp)
    edge_parity = calculate_parity(state.ep)
    h_parity = 1 if corner_parity != edge_parity else 0  # Cần ít nhất 1 nước đi để sửa dấu hoán vị

    # Heuristic cho định hướng tổng
    corner_orient_sum = sum(state.co) % 3
    edge_orient_sum = sum(state.eo) % 2
    h_orient = 1 if corner_orient_sum != 0 or edge_orient_sum != 0 else 0  # Cần ít nhất 1 nước đi để sửa định hướng

    # Lấy giá trị lớn nhất
    return max(h_corner, h_edge, h_parity, h_orient)