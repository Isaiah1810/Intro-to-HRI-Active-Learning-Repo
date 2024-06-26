import learning
from mistyPy.Robot import Robot
import numpy as np
from shape_detector import get_colors_shapes
from misty import *
ip = "172.26.232.220"
house = ['pink', 'triangle', '*', '*', 'square', '*', 'house']
snowman = ['*', 'circle', 'small', '*', 'circle', '*', 'snowman']
alien = ['green', 'circle', '*', 'green', '*', '*', 'alien']
icecream = ['*', 'circle', '*', 'yellow', 'triangle', '*', 'icecream']
concepts = dict()
concepts['house'] = house
concepts['snowman'] = snowman
concepts['alien'] = alien
concepts['icecream'] = icecream


def generate_mod_hypotheses():
    colors = ['pink', 'green', 'yellow', 'orange']
    shapes = ['square', 'triangle', 'circle']
    sizes = ['small', 'large']
    all_hypotheses = []
    for color in colors:
        for shape in shapes:
            for size in sizes:
                for color2 in colors:
                    for shape2 in shapes:
                        for size2 in sizes:
                            hypothesis = [color, shape,
                                          size, color2, shape2, size2]
                            all_hypotheses.append(hypothesis)
    return all_hypotheses


def predict_label_query(example, H, consistencies):
    concept = example[-1]
    index = ['house', 'snowman', 'alien', 'icecream'].index(concept)
    BestConsist = max(consistencies[index])
    positive_count = 0
    negative_count = 0
    for count2, consistency in enumerate(consistencies[index]):
        if consistency == BestConsist:
            if learning.is_consistent(H[count2], example[:-1]):
                positive_count += 1
            else:
                negative_count += 1
    if positive_count > negative_count:
        label = '+'
    elif negative_count > positive_count:
        label = '-'
    else:
        label = '?'
    return positive_count - negative_count

# Hamming distance between the two hypothesis(total number of different things)


def get_distance(hyp1, hyp2):
    num_diff = 0
    for i in range(len(hyp1)):
        if (hyp1[i] != hyp2[i] or hyp1[i] == "*" or hyp2[i] == "*"):
            i += 1
    return num_diff


def is_one_away(curr_example, new_example):
    return (curr_example[0:3] == new_example[0:3] or
            curr_example[3:5] == new_example[3:5])


def get_one_away(curr_example, new_example):
    if curr_example[0:3] == new_example[0:3]:
        return 1
    elif curr_example[3:5] == new_example[3:5]:
        return 2
    return -1

# The robot makes a query about the current concept


def make_query(curr_example, hypotheses, consistencies, H):
    pos_hyps = generate_mod_hypotheses()
    examples = []
    concept = curr_example[-2]
    for i in range(len(pos_hyps)):
        hyp = pos_hyps[i]
        hyp.append(concept)
        example = predict_label_query(hyp, H, consistencies)
        if (abs(example) != len(hypotheses)):
            examples.append((abs(example), hyp))
    examples.sort(key=(lambda x: abs(x[0])))
    possible_queries = []
    for example in examples:
        if (is_one_away(curr_example, example[1:][0])):
            possible_queries.append(example[1:][0])
    if (possible_queries != []):
        new_query = possible_queries[0]
        diff_block = get_one_away(curr_example, new_query)
        match diff_block:
            case 1:
                string = f"Can you replace the bottom piece with a {new_query[5]} {new_query[3]} {new_query[4]}? "
                print(string)
                rob.speak(string)
                return
            case 2:
                string = f"Can you replace the top piece with a {new_query[2]} {new_query[0]} {new_query[1]}? "
                print(string)
                rob.speak(string)
                return
            case -1:
                assert (1 == 2)
    else:
        best_query = examples[0][1]
        string = f"Can you replace the top piece with a {best_query[2]} {best_query[0]} {best_query[1]}? "
        print(string)
        rob.speak(string)


H, consistencies = learning.generate_all_hypotheses()
H_LEN = len(H)
hypothesis_size = [H_LEN, H_LEN, H_LEN, H_LEN]


def step():
    choice = input(
        "press 1 for learning a concept, press 2 for making a prediction\n")
    match choice:
        case "1":
            example = input("give example\n").split()
            if (example[0] not in ['p', 'o', 'y', 'g']):
                return
            input_array = []
            for c in example:
                match c:
                    case "p":
                        input_array.append('pink')
                    case "o":
                        input_array.append('orange')
                    case "y":
                        input_array.append("yellow")
                    case "g":
                        input_array.append('green')
                    case "sq":
                        input_array.append('square')
                    case "c":
                        input_array.append("circle")
                    case "t":
                        input_array.append('triangle')
                    case "sm":
                        input_array.append('small')
                    case "l":
                        input_array.append("large")
                    case "sn":
                        input_array.append("snowman")
                    case "h":
                        input_array.append("house")
                    case "-":
                        input_array.append("-")
                    case "+":
                        input_array.append("+")
                    case _:
                        pass
            example = input_array
            concept = example[-2]
            index = ['house', 'snowman', 'alien', 'icecream'].index(concept)
            learned_hypothesis = learning.concept_learning(
                example, H, consistencies)
            if non_verbal:
                rob.start_action("think")
            num_hypothesis = len(learned_hypothesis)
            if non_verbal:
                rob.start_action("head-up-down-nod")
            rob.speak("O kay")
            print(num_hypothesis)
            if (num_hypothesis >= hypothesis_size[index] and num_hypothesis != 1):
                if (num_hypothesis == hypothesis_size[index]):
                    print("Uninformative label")
                make_query(example, learned_hypothesis, consistencies, H)

            hypothesis_size[index] = num_hypothesis
            rob.speak("Your turn")

        case "2":
            new_instance = input("give new instance\n").split()
            if (new_instance[0] not in ['p', 'o', 'y', 'g']):
                return
            input_array = []
            for c in new_instance:
                match c:
                    case "p":
                        input_array.append('pink')
                    case "o":
                        input_array.append('orange')
                    case "y":
                        input_array.append("yellow")
                    case "g":
                        input_array.append('green')
                    case "sq":
                        input_array.append('square')
                    case "c":
                        input_array.append("circle")
                    case "t":
                        input_array.append('triangle')
                    case "sm":
                        input_array.append('small')
                    case "l":
                        input_array.append("large")
                    case "sn":
                        input_array.append("snowman")
                    case "h":
                        input_array.append("house")
                    case _:
                        pass
            new_instance = input_array
            label, confidence = learning.predict_label(
                new_instance, H, consistencies)
            if non_verbal:
                rob.start_action("think")
            match label:
                case "+":
                    if non_verbal:
                        rob.start_action("admiration")
                    if non_verbal:
                        rob.start_action("head-up-down-nod")
                    rob.speak(f"Yes, this is a {new_instance[-1]}")
                case "-":
                    if non_verbal:
                        rob.start_action("fear")
                    rob.speak(f"No, it is not")
                case "?":
                    rob.speak(f"I'm not sure what this is yet")
            print("Instance:", new_instance)
            print("Predicted Label:", label)
            print("Confidence:", confidence)
            rob.speak("Your turn")
        case "3":
            curr_concept = input("give concept\n")
            pos_hyps = generate_mod_hypotheses()
            num_pred_false = 0
            num_true = 0
            num_false = 0
            num_pred_true = 0
            for hyp in pos_hyps:
                hyp.append(curr_concept)
                label, confidence = learning.predict_label(
                    hyp, H, consistencies)
                right_answer = learning.is_consistent(
                    concepts[curr_concept], hyp)
                if (label == "+"):
                    if (right_answer):
                        num_pred_true += 1
                elif (label == "-"):
                    if (not right_answer):
                        num_pred_false += 1 
                if (right_answer): num_true += 1
                if (not right_answer): num_false += 1
            print(f"Final Accuracy for {curr_concept}:",
                    f"Predicted true/Real true {num_pred_true/num_true}, Predicted false/real false{num_pred_false/num_false} ")
            print(f"Combined accuracy {(num_pred_true+num_pred_false)/(num_true+num_false)}")
        case _:
            return


rob = Robot(ip)
rob.start_action("body-reset")
non_verbal_input = input("Do you want non-verbal mode? [y/n] \n")
if (non_verbal_input == "y"):
    non_verbal = True
else:
    non_verbal = False
rob.speak("Hello, I'm Misty. It's nice to meet you!")
#rob.speak("Welcome back! I'm excited to learn from you again!")
if non_verbal:
    rob.start_action("hi")
while True:
    try:
        step()
    except KeyboardInterrupt:
        quit()
    except:
        pass