import learning 
import random


#Hamming distance between the two hypothesis(total number of different things)
def get_distance(hyp1, hyp2):
    num_diff = 0
    for i in range(len(hyp1)):
        if (hyp1[i] != hyp2[i] or hyp1[i] == "*" or hyp2[i] == "*"):
            i += 1
    return num_diff


#The robot makes a query about the current concept
def make_query(index, hypotheses, consistencies):
    hyp_len = len(hypotheses)
    diff_matrix = [0]*hyp_len
    for i in range(hyp_len):
        for j in range(i+1, hyp_len):
            hyp1 = hypotheses[i]
            hyp2 = hypotheses[j]
            num_diff = get_distance(hyp1, hyp2)
            diff_matrix[i] += num_diff
            diff_matrix[j] += num_diff
    max_val = max(diff_matrix)
    diff_example = hypotheses[diff_matrix.index(max_val)]
    colors = ["pink", "green", "yellow", "orange"]
    shapes = ["triangle", "square", "circle"]
    sizes = ["large", "small"]
    for k in range(len(diff_example)):
        if (diff_example[k] == "*"):
            match (k%3):
                case 0:
                    diff_example[k] = random.choice(colors)
                case 1:
                    diff_example[k] = random.choice(shapes)
                case 2:
                    diff_example[k] = random.choice(sizes)
    concepts = ['house', 'snowman', 'alien', 'icecream']
    concept = concepts[index]
    diff_example.append(concept)
    print(diff_example)
    choice = input("+ if this is correct, - if its incorrect\n")
    diff_example.append(choice)
    learned_hypothesis = learning.concept_learning(diff_example, H, consistencies)
    num_hypothesis = len(learned_hypothesis)
    hypothesis_size[index] = num_hypothesis
    print(num_hypothesis)
    

# Define target concepts
house = ['pink', 'triangle', '*', '*', 'square', '*']
snowman = ['*', 'circle', 'small', '*', 'circle', '*']
alien = ['green', 'circle', '*', 'green', '*', '*']
icecream = ['*', 'circle', '*', 'yellow', 'triangle', '*']
H, consistencies = learning.generate_all_hypotheses()
H_LEN = len(H)
hypothesis_size = [H_LEN, H_LEN, H_LEN, H_LEN]
while True:
    choice = input("press 1 for learning a concept, press 2 for making a prediction\n")
    match choice:
        case "1":
            example = input("give example\n").split()
            concept = example[-2]
            index = ['house', 'snowman', 'alien', 'icecream'].index(concept)
            learned_hypothesis = learning.concept_learning(example, H, consistencies)
            num_hypothesis = len(learned_hypothesis)
            print(num_hypothesis)
            if(num_hypothesis >= hypothesis_size[index]):
                if (num_hypothesis == hypothesis_size[index]):
                    print("Uninformative label")
                make_query(index,learned_hypothesis, consistencies)
            hypothesis_size[index] = num_hypothesis

        case "2":
            new_instance = input("give new instance\n").split()
            label, confidence = learning.predict_label(new_instance, H, consistencies)
            print("Instance:", new_instance)
            print("Predicted Label:", label)
            print("Confidence:", confidence)
        case _:
            continue