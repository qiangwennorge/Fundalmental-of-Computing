"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    
    if not hand:
        return 0
    
    max_score = 0
    
    for dice in hand:
        temp = list(hand).count(dice) * dice
        if temp > max_score:
            max_score = temp
            
    return max_score

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    die_outcomes = set(range(1, num_die_sides + 1))
    
    possible_sequences = gen_all_sequences(die_outcomes, num_free_dice)
    
    total_score = 0.0
    for sequence in possible_sequences:
        total_score += score(held_dice + sequence)
    
    return float(total_score / len(possible_sequences))

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    possible_holds = set([()])
    
    for dice in hand:
        temp_holds = possible_holds.copy()
        for hold in temp_holds:
            temp_seq = list(hold)
            temp_seq.append(dice)
            possible_holds.add(tuple(temp_seq))
    
    return possible_holds


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    
    best_value = 0.0
    best_hold = ()
    
    possible_holds = gen_all_holds(hand)
    
    for hold in possible_holds:
        current_value = expected_value(hold, num_die_sides, len(hand) - len(hold))
        if current_value > best_value:
            best_value = current_value
            best_hold = hold
        
    return (best_value, best_hold)

def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
#run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



