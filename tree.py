import random

def generate_sequence(length):
    return [random.randint(1, 4) for _ in range(length)]

def computer(sequence, current_depth, player_scores, current_player):
    index = []
    move = []
    results = game_tree(sequence, current_depth, index, player_scores, current_player, move)

    sorted_tree = [results[0]]

    for i in range(3):
        for each in results:
            if each[1] == i+1:
                eksiste = False
                for each_sorted in sorted_tree:
                    if sorted(each[2]) == sorted(each_sorted[2]) and each[3] == each_sorted[3]:
                        eksiste = True
                if eksiste == False:
                    sorted_tree.append(each)

    for each in sorted_tree:
        print(each)


def game_tree(sequence, current_depth, index, player_scores, current_player, move):
    results = []
    if current_depth > 3 or len(sequence) == 0:
        return results
    else:
        varianti = algo(sequence, current_depth, index, player_scores, current_player, move)
        for each in varianti:
            results.extend([[each[1], current_depth, each[0], each[2], each[3]]])
            result_sequence = game_tree(each[0], current_depth+1, each[1], each[2], (current_player + 1) % 2, each[3])
            results.extend(result_sequence)
        return results

def algo(sequence, current_depth, index, player_scores, current_player, move):
    new_player_scores = [player_scores[0], player_scores[1]]
    variants = []
    for i in range(len(sequence)):
        new_index = index + [i]  # Jauna indeksa pievienošana
        if sequence[i] == 2:
            new_sequence = sequence[:i] + [1, 1] + sequence[i+1:]
            new_move = move + ["split"]
            variants.append([new_sequence, new_index, [new_player_scores[0],new_player_scores[1]], new_move])
        elif sequence[i] == 4:
            new_sequence = sequence[:i] + [2, 2] + sequence[i+1:]
            new_player_scores[current_player] = player_scores[1] + 1
            new_move = move + ["split"]
            variants.append([new_sequence, new_index, [new_player_scores[0],new_player_scores[1]], new_move])
            new_player_scores[current_player] = player_scores[1] -1
        new_move = move + ["take"]
        new_sequence = sequence[:i] + sequence[i+1:]
        new_player_scores[current_player] = player_scores[1] + sequence[i]
        variants.append([new_sequence, new_index, [new_player_scores[0],new_player_scores[1]], new_move])

    return variants

if __name__ == "__main__":
    length = int(input("Enter the length of the sequence (15-20): "))
    sequence = generate_sequence(length)
    print(sequence)
    current_depth = 1
    player_scores = [0,0]
    current_player = 0
    computer(sequence, current_depth, player_scores, current_player)