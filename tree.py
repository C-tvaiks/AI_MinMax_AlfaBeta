import random

class GameNode:
    def __init__(self, state, player1_score, player2_score, level, action, player_turn=1):
        self.state = state
        self.player1_score = player1_score
        self.player2_score = player2_score
        self.level = level
        self.action = action
        self.player_turn = player_turn
        self.children = []
        self.flat_list = []

def generate_sequence(length):
    return [random.randint(1, 4) for _ in range(length)]

def build_tree(node, max_depth):
    if node.level == max_depth:
        return
    
    for i, num in enumerate(node.state):
        # Возможный ход: взять число
        if num in [1, 2, 3, 4]:  # Проверяем наличие числа для выполнения хода
            new_state = node.state[:]
            new_state.pop(i)  # Удаляем взятое число
            if node.player_turn == 1:
                child = GameNode(new_state, node.player1_score + num, node.player2_score, node.level + 1, f"take {num}", 2)
            else:
                child = GameNode(new_state, node.player1_score, node.player2_score + num, node.level + 1, f"take {num}", 1)
            node.children.append(child)
            build_tree(child, max_depth)
    
    # Проверяем возможность выполнения других действий
    if 2 in node.state:
        new_state = node.state[:]
        new_state.remove(2)
        new_state.extend([1, 1])  # Разделяем 2 на два числа 1
        child = GameNode(new_state, node.player1_score, node.player2_score, node.level + 1, "split 2", node.player_turn)
        node.children.append(child)
        build_tree(child, max_depth)
    
    if 4 in node.state:
        new_state = node.state[:]
        new_state.remove(4)
        new_state.extend([2, 2])  # Разделяем 4 на два числа 2
        child = GameNode(new_state, node.player1_score + 1, node.player2_score, node.level + 1, "split 4", node.player_turn)
        node.children.append(child)
        build_tree(child, max_depth)

def flatten_tree(node, unique_nodes=None):
    if unique_nodes is None:
        unique_nodes = set()
    node_key = (tuple(node.state), node.player1_score, node.player2_score, node.action)
    if node_key in unique_nodes:
        return []
    unique_nodes.add(node_key)
    flat_list = [node]
    for child in node.children:
        flat_list.extend(flatten_tree(child, unique_nodes))
    return flat_list