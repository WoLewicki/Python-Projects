import re
import itertools
bin_operators = "*+^>="
unary_operators = "!"
logic_vars = ["0", "1"]


def parse_variables(input):
    result = re.findall(r'[A-Za-z]\w*', input)
    return list(set(result))  # set cuts reaccuring vars


def validate(x):
    chars_from_strings = re.sub(r'\w+', 'c', x)
    bracket_counter = 0
    if chars_from_strings[0] is not 'c' and chars_from_strings[0] not in unary_operators \
            and chars_from_strings[0] is not "(" and chars_from_strings[0] is not " ":
        return False
    state = 1
    for letter in chars_from_strings:
        if letter == " ":
            continue
        if bracket_counter < 0:
            return False
        if state == 1:
            if letter == "(":
                bracket_counter += 1
            elif letter == 'c':
                state = 2
            elif letter in unary_operators:
                pass
            else:
                return False
        else:
            if letter in bin_operators:
                state = 1
            elif letter == ")":
                bracket_counter -= 1
            else:
                return False
    return bracket_counter == 0 and state == 2


def eval_unary(operator, operand):
    if operator == "!":
        if operand == "0":
            return "1"
        else:
            return "0"


def eval_binary(operator, operand1, operand2):
    if operator == "*":
        if operand1 == "1" and operand2 == "1":
            return "1"
        else:
            return "0"
    elif operator == "+":
        if operand1 == "0" and operand2 == "0":
            return "0"
        else:
            return "1"
    elif operator == "^":
        if operand1 == "0" and operand2 == "1":
            return "1"
        elif operand1 == "1" and operand2 == "0":
            return "1"
        else:
            return "0"
    elif operator == ">":
        if operand1 == "1" and operand2 == "0":
            return "0"
        else:
            return "1"
    elif operator == "=":
        if operand1 == "1" and operand2 == "1":
            return "1"
        elif operand1 == "0" and operand2 == "0":
            return "1"
        else:
            return "0"


# given number and length of the list returns binary representation of length equal to length of list
def transform_to_bin(number, length):
    if length == 0:
        return ""
    binary = bin(number)
    binary = binary[2:]
    return "0" * (length-len(binary)) + binary


#shunting-yard algorythm evaluating all true/false options of ready binary representation with its variable number
def shunting_yard (bin_expr):
    operator_stack = []
    operand_stack = []
    for elem in bin_expr:
        if elem in logic_vars:
            operand_stack.append(elem)
        elif elem == "(" or elem in unary_operators:
            operator_stack.append(elem)
        elif elem == ")":
            while operator_stack[-1] != "(":  # waiting for start of paren
                operator = operator_stack.pop()
                if operator in bin_operators:
                    operand2 = operand_stack.pop()
                    operand1 = operand_stack.pop()
                    operand_stack.append(eval_binary(operator, operand1, operand2))
                elif operator in unary_operators:
                    operand = operand_stack.pop()
                    operand_stack.append(eval_unary(operator, operand))
                else:
                    operator_stack.pop()  # popping (
        elif elem in bin_operators:
            while operator_stack and operator_stack[-1] != "(":
                operator = operator_stack.pop()
                if operator in unary_operators:
                    operand = operand_stack.pop()
                    operand_stack.append(eval_unary(operator, operand))
                elif operator in bin_operators:
                    operand2 = operand_stack.pop()
                    operand1 = operand_stack.pop()
                    operand_stack.append(eval_binary(operator, operand1, operand2))
            operator_stack.append(elem)
    while operator_stack:  # use rest of operators
        operator = operator_stack.pop()
        if operator in unary_operators:
            operand = operand_stack.pop()
            operand_stack.append(eval_unary(operator, operand))
        elif operator in bin_operators:
            operand2 = operand_stack.pop()
            operand1 = operand_stack.pop()
            operand_stack.append(eval_binary(operator, operand1, operand2))
    return operand_stack.pop()  # the last operand in stack is the result of the expression


def get_true_list(expr, var_list):
    result_list = []
    for i in range(0, 2 ** len(var_list)):
        helper = expr
        bin_representation = transform_to_bin(i, len(var_list))
        for j in range(0, len(bin_representation)):
            helper = re.sub("(?<!\w)" + var_list[j] + "(?!\w)", bin_representation[j], helper)
        if shunting_yard(helper) == "1":
            result_list.append(bin_representation)
    return result_list


def check_empty(group):  # returns False if there are only empty lists in group too

    if len(group) == 0:
        return True

    else:
        count = 0
        for i in group:
            if i:
                count += 1
        if count == 0:
            return True
    return False


def compare_bites(x1, x2):
    counter = 0
    pos = -1
    for i in range(len(x1)):
        if x1[i] != x2[i]:
            counter += 1
            pos = i
    if counter == 1:
        return True, pos
    return False, pos


def combine_pairs(group, unchecked):
    length = len(group) - 1
    check_list = []  # list of procedured binaries
    new_group = [[] for x in range(length)]  # list of new group to procedure
    for i in range(length):
        for x1 in group[i]:
            for x2 in group[i+1]:  # compare bites in two closest groups
                logic, position = compare_bites(x1, x2)
                if logic:
                    check_list.append(x1)
                    check_list.append(x2)
                    element = list(x1)
                    element[position] = "-"
                    element = "".join(element)
                    new_group[i].append(element)
    for i in group:
        for j in i:
            if j not in check_list:
                unchecked.append(j)  # if it wasnt procedured even once, add it to the group of unchecked
    return new_group, unchecked


def remove_redundant(group):
    new_group = []
    for i in group:
        new = []
        for j in i:
            if j not in new:
                new.append(j)
        new_group.append(new)
    return new_group


def compare_weird(bin_list, weird_list):
    for i in range(len(weird_list)):
        if weird_list[i] != "-":
            if weird_list[i] != bin_list[i]:
                return False
    return True


def find_essential_primes(array):
    primes = []
    for column in range(len(array[0])):
        pos = 0
        counter = 0
        for row in range(len(array)):
            if array[row][column] == 1:
                counter += 1
                pos = row
        if counter == 1:
            primes.append(pos)
    return primes


def check_if_all_are_zeros(array):
    for column in range(len(array[0])):
        for row in range(len(array)):
            if array[row][column] == 1:
                return False
    return True


def multiply(x1, x2):  # multiplies factors in efficient way
    result = []
    for i in x1:
        for j in x2:
            if i == j:  # if both digits are the same, apply only one
                result.append(i)
            else:
                result.append(list(set(i+j)))  # removes redundant and makes a list from it
    result.sort()
    return list(result for result, _ in itertools.groupby(result))  # removes redundant elements and returns list of elements


def petrick(array):  # finds the minimal form of needed implicants
    result = []
    for column in range(len(array[0])):
        part_of_result_list = []
        for row in range(len(array)):
            if array[row][column] == 1:
                part_of_result_list.append([row])
        if part_of_result_list:  # if is not empty
            result.append(part_of_result_list)
    for line in range(len(result) -1):
        result[line+1] = multiply(result[line], result[line+1])  # get new elements list and do multiply on the new one and the next element
    multiplied_list = result[-1]  # the last element is the end of the multipication
    multiplied_list.sort(key=len)
    min_length = len(multiplied_list[0])
    ending_list = []
    for i in range(len(multiplied_list)):  # take only those who have the least length
        if len(multiplied_list[i]) == min_length:
            ending_list.append(multiplied_list[i])
        else:
            break
    return ending_list


def calculate_length_of_unchecked(unchecked):
    counter = 0
    for elem in unchecked:  # i don't care about length of each variable
        if elem == 0:  #!var
            counter += 2
        elif elem == 1:
            counter += 1
    return counter


def make_unchecked(indexes, unchecked):
    result = []
    for elem in indexes:
        result.append(unchecked[elem])
    return result


def find_minimal_result(array, unchecked):  # unchecked now have all elements which the array is made of(filled)
    essential_primes = find_essential_primes(array)  # returning positions of columns with one 1
    essential_primes = list(set(essential_primes))  # should cut redundant rows
    unique_primes_list = []
    for index in essential_primes:  # adding unchecked that have to be in result
        unique_primes_list.append(unchecked[index])
    for i in range(len(essential_primes)):  # make 0 in all columns where there are essential primes
        for column in range(len(array[0])):
            if array[essential_primes[i]][column] == 1:
                for row in range(len(array)):
                    array[row][column] = 0
    if check_if_all_are_zeros(array):
        return unique_primes_list
    petrick_result = petrick(array)
    cost_list = []  # we must choose the minimal result from minimal result options of petrick's algorithm
    for element in petrick_result:  # we find the length of each result of petrick's algo
        count = 0
        for index in element:
            count += calculate_length_of_unchecked(unchecked[index])
        cost_list.append(count)
    min_cost_index = -1
    min_cost = cost_list[0]
    for i in range(len(cost_list)):  # we find the shortest result in petrick's result list
        if cost_list[i] < min_cost:
            min_cost = cost_list[i]
            min_cost_index = i
    final_list = make_unchecked(petrick_result[min_cost_index], unchecked)  # gives binary representation of min result
    for primes_elem in unique_primes_list:
        if primes_elem not in final_list:
            final_list.append(primes_elem)
    return final_list


def transform_to_vars(bin_repr, variables):  # transform every binary representation into variable names
    result = ""
    for i in range(len(bin_repr)):
        if bin_repr[i] == "0":
            result += "!"
            result += variables[i]
            if i != len(bin_repr) - 1:
                result += "*"
        elif bin_repr[i] == "1":
            result += variables[i]
            if i != len(bin_repr) - 1:
                result += "*"
    if result[-1] == "*":
        return result[0:-1]
    return result


def quine_mc(expr):
    var_list = parse_variables(expr)
    true_list = get_true_list(expr, var_list)
    if not true_list:
        return "0"
    if len(true_list) == 2 ** len(parse_variables(expr)):  # always true
        return "1"
    var_number = len(true_list[0])
    group = [[] for x in range(var_number+1)]  # if we have 4 variables they can have 0,1,2,3,4 "1" elements so 5.
    unchecked = []
    for elem in true_list:
        index = elem.count("1")
        group[index].append(elem)
    while not check_empty(group):  # after this all expressions are in unchecked list
        new_group, unchecked = combine_pairs(group, unchecked)
        group = remove_redundant(new_group)
    array = [[0 for x in range(len(true_list))] for x in range(len(unchecked))]  # array [all true results][unchecked length]
    for i in range(len(true_list)):
        for j in range(len(unchecked)):
            if compare_weird(true_list[i], unchecked[j]):
                array[j][i] = 1
    minimal_result = find_minimal_result(array, unchecked)
    result = []
    for i, elem in enumerate(minimal_result):
        result += transform_to_vars(elem, var_list)
        if i != len(minimal_result) - 1:
            result += " + "
    print("".join(result))
