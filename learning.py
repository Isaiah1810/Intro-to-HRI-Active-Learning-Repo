def generate_all_hypotheses():
    colors = ['pink', 'green', 'yellow', 'orange', '*']
    shapes = ['square', 'triangle', 'circle', '*']
    sizes = ['small', 'large', '*']
    all_hypotheses = []
    for color in colors:
        for shape in shapes:
            for size in sizes:
                for color2 in colors:
                    for shape2 in shapes:
                        for size2 in sizes:
                            hypothesis = [color, shape, size, color2, shape2, size2]
                            all_hypotheses.append(hypothesis)
    all_hypotheses.pop()  # Remove the last hypothesis which is all '*'                        
    consistencies = [[0 for _ in range(len(all_hypotheses))] for _ in range(4)]                        
    return all_hypotheses, consistencies

def is_consistent(hypothesis, example):
    for i in range(len(example)):
        if hypothesis[i] != '*' and hypothesis[i] != example[i]:
            return False
    return True


def concept_learning(example, H, consistencies):
    label = example[-1]
    concept = example[-2]
    index = ['house', 'snowman', 'alien', 'icecream'].index(concept)
    V = []
    for count, hypothesis in enumerate(H):
        if is_consistent(hypothesis, example[:-2]):
            if label == '+':
                consistencies[index][count] += 1
            else:
                consistencies[index][count] -= 1
    BestConsist = max(consistencies[index])
    for count2, consistency in enumerate(consistencies[index]):
        if consistency == BestConsist:
            V.append(H[count2])

    return V

def predict_label(example, H, consistencies):
    concept = example[-1]
    index = ['house', 'snowman', 'alien', 'icecream'].index(concept)
    BestConsist = max(consistencies[index])
    positive_count = 0
    negative_count = 0
    for count2, consistency in enumerate(consistencies[index]):
        if consistency == BestConsist:
            if is_consistent(H[count2], example[:-1]):
                positive_count += 1
            else:
                negative_count += 1
    if positive_count > negative_count:
        label = '+'
    elif negative_count > positive_count:
        label = '-'
    else:
        label = '?'

    confidence = abs(positive_count - negative_count) / (positive_count + negative_count)
    return label, confidence


# def understand(BestConsist, H, one_consistencies):
#     V = []
#     for count, consistency in enumerate(one_consistencies):
#         if consistency == BestConsist:
#             V.append(H[count])
#     for j in range(len(V)):
#         for i in range(6):
#             if V[0][i] == V[1][i]:
#                 V[1][i] = '*'


if __name__ == "__main__":
    # Define target concepts
    house = ['pink', 'triangle', '*', '*', 'square', '*']
    snowman = ['*', 'circle', 'small', '*', 'circle', '*']
    alien = ['green', 'circle', '*', 'green', '*', '*']
    icecream = ['*', 'circle', '*', 'yellow', 'triangle', '*']

    # Initialize H and consistency arrays for each concept
    H, consistencies = generate_all_hypotheses()

    # Labeled examples
    labeled_examples = [
        ['pink', 'triangle', 'large', 'yellow', 'square', 'large', 'house', '+'],
        ['orange', 'triangle', 'large', 'yellow', 'square', 'large', 'house', '-'],
        ['pink', 'triangle', 'small', 'yellow', 'square', 'small', 'house', '+']
        # ['pink', 'circle', 'large', 'yellow', 'square', 'small', 'house', '-'],
        # ['orange', 'triangle', 'large', 'yellow', 'square', 'small', 'house', '-']
        # ['pink', 'triangle', 'large', 'yellow', 'square', 'small',  'snowman', '-']
    ]

    # Perform concept learning
    for example in labeled_examples:
        learned_hypotheses = concept_learning(example, H, consistencies)

    # Print learned hypotheses
    print("Learned Hypotheses:")
    for i, hypotheses in enumerate(learned_hypotheses):
        print(f"Concept {i+1}:")
        for hypothesis in hypotheses:
            print(hypothesis)
        print()

    # Predictions
    new_instances = [
        ['pink', 'circle', 'large', 'yellow', 'square', 'small', 'house'],  # Example 1
        ['green', 'triangle', 'large', 'yellow', 'circle', 'small', 'house'],  # Example 2
        ['pink', 'triangle', 'large', 'yellow', 'square', 'large', 'house'],  # Example 3
        ['pink', 'triangle', 'large', 'green', 'square', 'small', 'house'],  # Example 4
    ]

    for instance in new_instances:
        label, confidence = predict_label(instance, H, consistencies)
        print("Instance:", instance)
        print("Predicted Label:", label)
        print("Confidence:", confidence)
        print()

