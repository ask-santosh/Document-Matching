# Document-Matching
Python Program for document matching using ROI extraction and Leveinstein distance 

The Levenshtein Distance

The Levenshtein distance is a metric to measure how apart are two sequences of words. In other words, it measures the minimum number of edits that you need to do to change a one-word sequence into the other. These edits can be insertions, deletions or substitutions. This metric was named after Vladimir Levenshtein, who originally considered it in 1965.

The formal definition of the Levenshtein distance between two strings a and b can be seen as follows:

![alt text](https://github.com/ask-santosh/Document-Matching/blob/main/old_code/Screen_Shot_2019-02-04_at_10.55.46_AM_kxnz1h.png?raw=true)


Where 1(ai≠bj) denotes 0 when a=b and 1 otherwise. It is important to note that the rows on the minimum above correspond to a deletion, an insertion, and a substitution in that order.

It is also possible to calculate the Levenshtein similarity ratio based on the Levenshtein distance. This can be done using the following formula:

(|a|+|b|)−leva,b(i,j)|a|+|b|
where |a| and |b| are the lengths of sequence a and sequence b respectively.
