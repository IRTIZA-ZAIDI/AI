def get_keys_by_value(input_dict, target_value):
    return [key for key, value in input_dict.items() if value == target_value]


def swap_characters_by_indices(input_string, index1, index2):
    string_list = list(input_string)

    if 0 <= index1 < len(string_list) and 0 <= index2 < len(string_list):

        string_list[index1], string_list[index2] = (
            string_list[index2],
            string_list[index1],
        )
        swapped_string = "".join(string_list)
        return swapped_string
    else:

        return "Invalid"


def generate_children(input_string):
    children_list = []
    zero_index = input_string.index("0")

    if zero_index - 2 >= 0:
        char_behind_1 = input_string[zero_index - 1]
        char_behind_2 = input_string[zero_index - 2]
        if char_behind_1 == "2":
            children_list.append(
                swap_characters_by_indices(input_string, zero_index, zero_index - 1)
            )
        if char_behind_2 == "2":
            children_list.append(
                swap_characters_by_indices(input_string, zero_index, zero_index - 2)
            )
    elif zero_index - 1 >= 0:
        char_behind_1 = input_string[zero_index - 1]
        if char_behind_1 == "2":
            children_list.append(
                swap_characters_by_indices(input_string, zero_index, zero_index - 1)
            )

    if zero_index + 2 < len(input_string):
        char_ahead_1 = input_string[zero_index + 1]
        char_ahead_2 = input_string[zero_index + 2]
        if char_ahead_1 == "1":
            children_list.append(
                swap_characters_by_indices(input_string, zero_index, zero_index + 1)
            )
        if char_ahead_2 == "1":
            children_list.append(
                swap_characters_by_indices(input_string, zero_index, zero_index + 2)
            )
    elif zero_index + 1 < len(input_string):
        char_ahead_1 = input_string[zero_index + 1]
        if char_ahead_1 == "1":
            children_list.append(
                swap_characters_by_indices(input_string, zero_index, zero_index + 1)
            )

    return children_list


def bfs_search(start, end):
    visited_array = {}
    queue = []
    count = 0

    current_level = 0
    queue.append(start)
    queue.append(None)

    while queue:
        curr_string = queue.pop(0)

        if curr_string is None:
            if queue:
                queue.append(None)
            current_level += 1
            print(f"\n--- Level {current_level} ---")
            continue

        print(curr_string)
        children = generate_children(curr_string)
        flag = False

        if len(children) > 0:
            for child in children:
                if child == end:
                    flag = True
                    visited_array.update({child: current_level + 1})
                    count += 1
                    break

                visited_array.update({child: current_level + 1})
                queue.append(child)
                count += 1

        if flag:
            break

    if not flag:
        print("Failed")

    max_value = max(visited_array.values())
    print("\n--- States ---")
    for i in range(1, max_value + 1):
        list_states = get_keys_by_value(visited_array, i)
        for state in list_states:
            print(state)
        print("\n---")
    print("Number of moves to achieve the goal state are: ", max_value)
    print("Number of states visited are: ", count)


bfs_search("2220111", "1110222")


# def bfs_search(start, end):
#     list_states = []
#     visited_array = {}
#     queue = []
#     count = 0

#     current_level = 0
#     queue.append(start)
#     queue.append(None)

#     while queue:
#         curr_string = queue.pop(0)

#         if curr_string is None:
#             if queue:
#                 queue.append(None)
#             current_level += 1
#             continue

#         children = generate_children(curr_string)
#         flag = False

#         if len(children) > 0:
#             print(
#                 "Children nodes for level", current_level, ":", children
#             )  # Print children nodes
#             for child in children:
#                 if child == end:
#                     flag = True
#                     visited_array.update({child: current_level + 1})
#                     count += 1
#                     break

#                 visited_array.update({child: current_level + 1})
#                 queue.append(child)
#                 count += 1

#         if flag:
#             break

#     if not flag:
#         print("Failed")

#     max_value = max(visited_array.values())
#     for i in range(1, max_value + 1):
#         list_states.extend(get_keys_by_value(visited_array, i))
#     list_states.insert(0, start)

#     for state in list_states:
#         print(state)
#         print("\n")
#     print("Number of moves to achieve the goal state are: ", max_value)
#     print("Number of states visited are: ", count)


# bfs_search("2220111", "1110222")
