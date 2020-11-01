import os
import random
import re
import sys
import numpy as np
from collections import Counter
from copy import *
DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    T = dict()

    if len(corpus[page]) == 0 :
        for new_page in corpus.keys():
            T[new_page] = 1 / len(corpus.keys())
        return T

    L = corpus.keys()
    for new_page in L:
        if new_page in list(corpus[page]) and new_page != page :
            T[new_page] = damping_factor * (1 / len(corpus[page])) + (1 - damping_factor) * (1 / len(corpus))
        else:
            T[new_page] = (1 - damping_factor) * (1 / len(corpus))
    return T



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    S=[]
    first = (random.choice(list(corpus)))
    S.append(first)
    for i in range(n-1):
        T = transition_model(corpus,first,damping_factor)
        keys = T.keys()
        probs = T.values()
        first = np.array2string(np.random.choice(list(keys), 1, replace=True, p=list(probs)),separator='')
        first=first[2:-2]
        S.append(first)
    K=Counter(S)
    for word in K:
        K[word]=K[word]/n

    return(K)


def linked_pages(page,corpse):
    T=[]
    for i in corpse:
        if page in corpse[i]:
            T.append(i)
    return T





def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    N=len(corpus)
    PR=dict()
    for i in corpus:
        PR[i]=1/N

    while True:
        j = 0
        PR_Beta=deepcopy(PR)
        for page in corpus:
            T = linked_pages(page,corpus)
            PR[page] = ((1 - damping_factor) / N)
            for i in T:
                PR[page] = PR[page]+damping_factor * (PR_Beta[i]/len(corpus[i]))
        for i in PR:
            if abs(PR[i]-PR_Beta[i])>0.001:
                j=1
        if j==0:
            break

    return(PR)



    raise NotImplementedError


if __name__ == "__main__":
    main()

