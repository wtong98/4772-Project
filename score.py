import metrics
import sys
import numpy as np
import os
import json
from internal.music2vec import ScoreFetcher, ScoreToWord, ScoreToVec

SCORE_WORD_PATH = r'data/score_word_cache.json'

file_name = sys.argv[1]
eval_scores = []
if os.path.isdir(file_name):
    files = os.listdir(file_name)
    for fi in files:
        my_score = json.loads(open(file_name + fi, 'r').read())
        eval_scores.append((fi, my_score))
else:
    my_score = json.loads(open(file_name, 'r').read())
    eval_scores.append((file_name, my_score))

# Load in scores
print('Loading test scores...')
myScoreToWord = ScoreToWord(SCORE_WORD_PATH)
myScoreToWord.load_cache()

all_costs = []
for i in eval_scores:
    # Test chord_similarity metric
    print('Testing chord_similarity for {}...'.format(i[0]))
    cost = metrics.chord_similarity(i[1], myScoreToWord.test_scores)
    print('chord_similarity', cost)
    all_costs.append(cost)
if len(all_costs) > 1:
    z_score = 1.96
    std = np.std(all_costs)
    mean = np.mean(all_costs)
    print('{:.2f} \pm {:.2f}'.format(mean, std*z_score))

