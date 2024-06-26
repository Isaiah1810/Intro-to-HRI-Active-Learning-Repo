import learning
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
                            hypothesis = [color, shape, size, color2, shape2, size2]
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
    else: 
        label = '-'
    return positive_count - negative_count

#Hamming distance between the two hypothesis(total number of different things)
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

#The robot makes a query about the current concept
def make_query(curr_example, hypotheses, consistencies, H):
    pos_hyps = generate_mod_hypotheses()
    examples = []
    concept = curr_example[-2]
    for i in range(len(pos_hyps)):
        hyp = pos_hyps[i]
        hyp.append(concept)
        example = predict_label_query(hyp, H, consistencies)
        if (abs(example) != len(hypotheses)) : examples.append((abs(example), hyp))
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
                print(f"Replace bottom piece with {new_query[3]} {new_query[4]} {new_query[5]}")
                return
            case 2:
                print(f"Replace top piece with {new_query[0]} {new_query[1]} {new_query[2]}")
                return
            case -1:
                assert(1 == 2)
    else:
        best_query = examples[0][1]
        print(f"Replace top piece with {best_query[0]} {best_query[1]} {best_query[2]}")

H, consistencies = learning.generate_all_hypotheses()
H_LEN = len(H)
hypothesis_size = [H_LEN, H_LEN, H_LEN, H_LEN]

def step():
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
                make_query(example, learned_hypothesis, consistencies, H)
            hypothesis_size[index] = num_hypothesis

        case "2":
            new_instance = input("give new instance\n").split()
            label, confidence = learning.predict_label(new_instance, H, consistencies)
            print("Instance:", new_instance)
            print("Predicted Label:", label)
            print("Confidence:", confidence)
        case _:
            return