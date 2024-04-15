from SequenceAnalyzer import SequenceAnalyzer

def input_values():
    """Input x and eps values from user and validate them."""

    while True:
        try:
            x = float(input("Enter the value of x such that (|x| < 1): "))
            if abs(x) >= 1:
                raise ValueError("The value entered must be less than 1 in absolute terms")
            break
        except ValueError as e:
            print(f"Error: {e}. Please try again.")

    while True:
        try:
            eps = float(input("Enter the precision (eps) for calculations: "))
            break
        except ValueError:
            print("Error: Please enter a numerical value for eps.")

    return x, eps

def task3_solve():
    """Main function for task 3."""

    x, eps = input_values()
    sequence_analyzer = SequenceAnalyzer(x, eps)

    terms, n = sequence_analyzer.calculate_function(x, eps)
    print(f"x : {x}")
    print(f"n : {n}")
    print(f"F(x) : {terms[-1]}")
    print(f"Math F(x) : {1/(1-x)}")
    print(f"eps : {eps}")

    sequence_mean = sequence_analyzer.mean()
    sequence_median = sequence_analyzer.median()
    sequence_mode = sequence_analyzer.mode()
    sequence_variance = sequence_analyzer.variance()
    sequence_std_dev = sequence_analyzer.standard_deviation()

    print(f"Mean of the sequence: {sequence_mean}")
    print(f"Median of the sequence: {sequence_median}")
    print(f"Mode of the sequence: {sequence_mode}")
    print(f"Variance of the sequence: {sequence_variance}")
    print(f"Standard Deviation of the sequence: {sequence_std_dev}")

    sequence_analyzer.plot_graphs(eps)

