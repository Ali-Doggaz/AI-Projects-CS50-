


import csv
import itertools
import sys
#from pomegranate import *
PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    p = float(1)
    names = set(people.keys())
    no_gene = names - (set(one_gene).union(set(two_genes)))
    no_trait = names - set(have_trait)

    '''
    for person in two_genes:
        genes = (
            2 if person in two_genes else
            1 if person in one_gene else
            0
        )

        trait = person in have_trait
        mother = people[person]["mother"]
        father = people[person]["father"]

        # If person has no parents calculate unconditional probability
        if mother is None and father is None:
            probability *= PROBS["gene"][genes]

        # Otherwise calculate probabilities based on parents passing genes
        else:
            passing = {mother: 0, father: 0}

            for parent in passing:
                passing[parent] = (
                    # If the parent has two genes then it has 100% probability of passing unless it mutates
                    1 - PROBS["mutation"] if parent in two_genes else

                    # If the parent has only one gene then it has 50% probability of passing
                    0.5 if parent in one_gene else

                    # If the parent doesn't have a gene, the only way to get the gene is if it mutates
                    PROBS["mutation"]
                )

            probability *= (
                # Probability that both parents pass a gene
                passing[mother] * passing[father] if genes == 2 else

                # Probability of getting the gene from his mother and not his father or vice versa
                passing[mother] * (1 - passing[father]) + (1 - passing[mother]) * passing[father] if genes == 1 else

                # Probability of not getting the gene from any of the parents
                (1 - passing[mother]) * (1 - passing[father])
            )
    '''
    for person in two_genes:  # validé
        if people[person]["mother"] == None:
            p = p * PROBS["gene"][2]
        else:
            mom = people[person]["mother"]
            dad = people[person]["father"]
            if ((mom in two_genes) and (dad in two_genes)):
                p = p * (1 - PROBS["mutation"]) * (1 - PROBS["mutation"])  # correct
            elif ((mom in two_genes) and (dad in one_gene)) or ((dad in two_genes) and (mom in one_gene)):
                p = p * (1 - PROBS["mutation"]) * 0.5  # correct
            elif (mom in one_gene) and (dad in one_gene):
                p = p * 0.5 * 0.5  # correct
            elif ((mom in one_gene) and (dad in no_gene)) or ((dad in one_gene) and (mom in no_gene)):
                p = p * 0.5 * PROBS["mutation"]
            elif ((mom in two_genes) and (dad in no_gene)) or ((dad in two_genes) and (mom in no_gene)) :
                p = p * ( (1-PROBS["mutation"]) * PROBS["mutation"]) # correct
            else:
                p = p * PROBS["mutation"] * PROBS["mutation"]

    '''
    for person in one_gene:
        genes = (
            2 if person in two_genes else
            1 if person in one_gene else
            0
        )

        trait = person in have_trait
        mother = people[person]["mother"]
        father = people[person]["father"]

        # If person has no parents calculate unconditional probability
        if mother is None and father is None:
            probability *= PROBS["gene"][genes]

        # Otherwise calculate probabilities based on parents passing genes
        else:
            passing = {mother: 0, father: 0}

            for parent in passing:
                passing[parent] = (
                    # If the parent has two genes then it has 100% probability of passing unless it mutates
                    1 - PROBS["mutation"] if parent in two_genes else

                    # If the parent has only one gene then it has 50% probability of passing
                    0.5 if parent in one_gene else

                    # If the parent doesn't have a gene, the only way to get the gene is if it mutates
                    PROBS["mutation"]
                )

            probability *= (
                # Probability that both parents pass a gene
                passing[mother] * passing[father] if genes == 2 else

                # Probability of getting the gene from his mother and not his father or vice versa
                passing[mother] * (1 - passing[father]) + (1 - passing[mother]) * passing[father] if genes == 1 else

                # Probability of not getting the gene from any of the parents
                (1 - passing[mother]) * (1 - passing[father])
            )
    '''
    for person in one_gene:
        if people[person]["mother"] == None:
            p = p * PROBS["gene"][1]
        else:
            mom = people[person]["mother"]
            dad = people[person]["father"]
            if ((mom in two_genes) and (dad in two_genes)):
                p = p * PROBS["mutation"] * (1 - PROBS["mutation"]) * 2  # Correct
            elif (mom in two_genes and dad in one_gene) or (dad in two_genes and mom in one_gene):
                p = p * ((1 - PROBS["mutation"]) * 0.5 + PROBS["mutation"] * 0.5)  # Correct
            elif (mom in one_gene) and (dad in one_gene):
                p = p * 0.5  # correct
            elif ((mom in one_gene) and (dad in no_gene)) or ((dad in one_gene) and (mom in no_gene)):
                p = p * (0.5*(1-PROBS["mutation"]) + 0.5* (PROBS["mutation"]))  # correct
            elif ((mom in two_genes) and (dad in no_gene)) or ((dad in two_genes) and (mom in no_gene)) :
                p = p * ((1 - PROBS["mutation"]) * (1 - PROBS["mutation"]) + PROBS["mutation"] * PROBS["mutation"] ) # correct
            else:
                p = p * (PROBS["mutation"] * (1 - PROBS["mutation"]) * 2)

    '''
    for person in no_gene:
        genes = (
            2 if person in two_genes else
            1 if person in one_gene else
            0
        )

        trait = person in have_trait
        mother = people[person]["mother"]
        father = people[person]["father"]

        # If person has no parents calculate unconditional probability
        if mother is None and father is None:
            probability *= PROBS["gene"][genes]

        # Otherwise calculate probabilities based on parents passing genes
        else:
            passing = {mother: 0, father: 0}

            for parent in passing:
                passing[parent] = (
                    # If the parent has two genes then it has 100% probability of passing unless it mutates
                    1 - PROBS["mutation"] if parent in two_genes else

                    # If the parent has only one gene then it has 50% probability of passing
                    0.5 if parent in one_gene else

                    # If the parent doesn't have a gene, the only way to get the gene is if it mutates
                    PROBS["mutation"]
                )

            probability *= (
                # Probability that both parents pass a gene
                passing[mother] * passing[father] if genes == 2 else

                # Probability of getting the gene from his mother and not his father or vice versa
                passing[mother] * (1 - passing[father]) + (1 - passing[mother]) * passing[father] if genes == 1 else

                # Probability of not getting the gene from any of the parents
                (1 - passing[mother]) * (1 - passing[father])
            )
    '''
    for person in no_gene:  # validé
        if people[person]["mother"] == None:
            p = p * PROBS["gene"][0]
        else:
            mom = people[person]["mother"]
            dad = people[person]["father"]
            if ((mom in two_genes) and (dad in two_genes)):
                p = p * PROBS["mutation"] * (PROBS["mutation"])  # correct
            elif (mom in two_genes and dad in one_gene) or (dad in two_genes and mom in one_gene):
                p = p * (PROBS["mutation"] * 0.5)  # correct
            elif (mom in one_gene) and (dad in one_gene):
                p = p * 0.25  # correct
            elif ((mom in one_gene) and (dad in no_gene)) or ((dad in one_gene) and (mom in no_gene)):
                p = p * 0.5 * (1-PROBS["mutation"])  # correct
            elif ((mom in two_genes) and (dad in no_gene)) or ((dad in two_genes) and (mom in no_gene)) :
                p = p * PROBS["mutation"] * (1 - PROBS["mutation"]) # correct
            else:
                p = p * ((1 - PROBS["mutation"]) * (1 - PROBS["mutation"]))  # correct










                
    for person in have_trait:
        if person in one_gene:
            k = PROBS["trait"][1][True]
            p = p * k
        elif person in two_genes:
            k = PROBS["trait"][2][True]
            p = p * k
        else:
            k = PROBS["trait"][0][True]
            p = p * k
    for person in no_trait:
        if person in one_gene:
            k = PROBS["trait"][1][False]
            p = p * k
        elif person in two_genes:
            k = PROBS["trait"][2][False]
            p = p * k
        else:
            k = PROBS["trait"][0][False]
            p = p * k
    return p

    '''
    probability = float(1)

    for person in people:
        genes = (
            2 if person in two_genes else
            1 if person in one_gene else
            0
        )

        trait = person in have_trait
        mother = people[person]["mother"]
        father = people[person]["father"]

        # If person has no parents calculate unconditional probability
        if mother is None and father is None:
            probability *= PROBS["gene"][genes]

        # Otherwise calculate probabilities based on parents passing genes
        else:
            passing = {mother: 0, father: 0}

            for parent in passing:
                passing[parent] = (
                    # If the parent has two genes then it has 100% probability of passing unless it mutates
                    1 - PROBS["mutation"] if parent in two_genes else

                    # If the parent has only one gene then it has 50% probability of passing
                    0.5 if parent in one_gene else

                    # If the parent doesn't have a gene, the only way to get the gene is if it mutates
                    PROBS["mutation"]
                )

            probability *= (
                # Probability that both parents pass a gene
                passing[mother] * passing[father] if genes == 2 else

                # Probability of getting the gene from his mother and not his father or vice versa
                passing[mother] * (1 - passing[father]) + (1 - passing[mother]) * passing[father] if genes == 1 else

                # Probability of not getting the gene from any of the parents
                (1 - passing[mother]) * (1 - passing[father])
            )

        # Compute probability that a person does or does not have a particular trait
        probability *= PROBS["trait"][genes][trait]

    return probability
    '''









    



def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in one_gene:
        probabilities[person]["gene"][1] = probabilities[person]["gene"][1] + p
    for person in two_genes:
        probabilities[person]["gene"][2] = probabilities[person]["gene"][2] + p
    no_gene = list(set(probabilities) - (set(one_gene).union(set(two_genes))))
    for person in no_gene:
        probabilities[person]["gene"][0] = probabilities[person]["gene"][0] + p
    for person in have_trait:
        probabilities[person]["trait"][True] = probabilities[person]["trait"][True] + p
    no_trait = list(set(probabilities) - set(have_trait))
    for person in no_trait:
        probabilities[person]["trait"][False] = probabilities[person]["trait"][False] + p



def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        a = 1 / (probabilities[person]["trait"][True] + probabilities[person]["trait"][False])
        probabilities[person]["trait"][True] = probabilities[person]["trait"][True] * a
        probabilities[person]["trait"][False] = probabilities[person]["trait"][False] * a

        a= 1 / (probabilities[person]["gene"][0] + probabilities[person]["gene"][1] + probabilities[person]["gene"][2])
        probabilities[person]["gene"][0] = a * probabilities[person]["gene"][0]
        probabilities[person]["gene"][1] = a * probabilities[person]["gene"][1]
        probabilities[person]["gene"][2] = a * probabilities[person]["gene"][2]


if __name__ == "__main__":
    main()
