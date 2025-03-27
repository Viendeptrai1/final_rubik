import heapq
import time
from collections import deque
from rubik_chen import SOLVED_STATE_3x3, MOVE_NAMES, heuristic_3x3
from rubik_2x2 import Rubik2x2State, SOLVED_STATE_2x2, heuristic_2x2
def a_star(start_state, SOLVED_STATE, heuristic=heuristic_3x3):
    global dem_so_node
    counter = 0  # Counter to break ties in heap
    queue = [(heuristic(start_state), 0, counter, start_state, [])]
    visited = {start_state: 0}
    counter += 1

    start_time = time.time()
    while queue:
        _, g_score, _, state, path = heapq.heappop(queue)
        if state == SOLVED_STATE:
            return path, f"Thời gian: {time.time() - start_time:.2f} giây"

        for move in MOVE_NAMES:
            dem_so_node += 1
            new_state = state.apply_move(move)  # Fixed: call apply_move as a method of state
            new_g_score = g_score + 1
            if new_state not in visited or new_g_score < visited[new_state]:
                visited[new_state] = new_g_score
                h_score = heuristic(new_state)
                f_score = new_g_score + h_score
                heapq.heappush(queue, (f_score, new_g_score, counter, new_state, path + [move]))
                counter += 1

        if time.time() - start_time > 60:
            return None, "Hết thời gian"

    return None, "Không tìm thấy lời giải"

def bfs(start_state, SOLVED_STATE, heuristic=heuristic_3x3):
    global dem_so_node
    dem_so_node = 0
    queue = deque([(start_state, [])])  # (state, path)
    visited = {start_state}
    
    start_time = time.time()
    while queue:
        state, path = queue.popleft()
        
        if state == SOLVED_STATE:
            return path, f"Thời gian: {time.time() - start_time:.2f} giây"
        
        for move in MOVE_NAMES:
            dem_so_node += 1
            new_state = state.apply_move(move)  # Fixed: call apply_move as a method of state
            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, path + [move]))
        
        if time.time() - start_time > 60:
            return None, "Hết thời gian"
    
    return None, "Không tìm thấy lời giải"

# Tạo trạng thái ban đầu (xáo trộn nhẹ)
start_state = SOLVED_STATE_3x3.copy()
start_state = start_state.apply_move("R")  
start_state = start_state.apply_move("U") 

start_state_2x2 = SOLVED_STATE_2x2.copy()
start_state_2x2 = start_state_2x2.apply_move("F")  
start_state_2x2 = start_state_2x2.apply_move("L") 

dem_so_node = 0
print("Giải bằng A*:")
path, message = a_star(start_state, SOLVED_STATE_3x3)
if path:
    print("Đường đi:", path)
    print(message)
    print("Số node đã duyệt:", dem_so_node)
else:
    print("Kết quả:", message)

dem_so_node = 0
print("Giải bằng A*:")
path, message = a_star(start_state_2x2, SOLVED_STATE_2x2, heuristic=heuristic_2x2)
if path:
    print("Đường đi:", path)
    print(message)
    print("Số node đã duyệt:", dem_so_node)
else:
    print("Kết quả:", message)

dem_so_node = 0
print("Giải bằng BFS:")
path, message = bfs(start_state, SOLVED_STATE_3x3)
if path:
    print("Đường đi:", path)
    print(message)
    print("Số node đã duyệt:", dem_so_node)
else:
    print("Kết quả:", message)
    
dem_so_node = 0
print("Giải bằng BFS:")
path, message = bfs(start_state_2x2, SOLVED_STATE_2x2, heuristic=heuristic_2x2)
if path:
    print("Đường đi:", path)
    print(message)
    print("Số node đã duyệt:", dem_so_node)
else:
    print("Kết quả:", message)
