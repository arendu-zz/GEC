# Feature Templates 

## aspect features
Format of the examples: Each case has a state followed by '|||' and then the next state. Then the '--->' shows the features that will be fired given the first and second states.

- case1: Det_i-1 W_i-1(Asp_i-1) ||| Det_i W_i(Asp_i) -->  Det_i-Asp_i
- case2: Det_i-1 W_i-1(*) ||| W_i(Asp_i) -->  Det_i-1-Asp_i
- case3: W_i-1(Asp_i-1) ||| W_i(Asp_i) --> Asp_i-1-Asp_i

## Bigram LM feature
- It basically computes P(w|w_i-1) for all the candidates.
- In insertion or deletion cases, we compute LM score with the following principle.
  - e.g. [W0 W1] [W2 W3]. W0 and W1 are in a previous state (W0 is inserted).
  - P(W2|W1) * P(w3|W2)

