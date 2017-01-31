import argparse
import re
from collections import Counter

import numpy as np
from matplotlib import font_manager as fm
from matplotlib import pyplot as plt


def collect_statistics(input_path, query_words):
    pattern = r'^\[(.+?)] \[.+?\] (.+?)$'
    all_count = Counter()
    query_count = Counter()
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.startswith('['):
                continue
            line = line.strip()
            name, content = re.search(pattern, line).groups()
            all_count[name] += 1
            for w in query_words:
                if w in content:
                    query_count[name] += 1
                    break
    return all_count, query_count


def main():
    input_path = args.i
    query_words = args.q
    query_words = [w for w in  query_words.split(',') if w]
    all_count, query_count = collect_statistics(input_path, query_words)
    names, q_values = list(zip(*query_count.most_common(len(query_count))))
    a_values = [all_count[n] for n in names]
    abs_values = np.array(q_values)
    rel_values = abs_values / np.array(a_values)
    num_persons = len(names)
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    prop = fm.FontProperties(fname='./NanumGothic.ttf')
    ax1.bar(np.arange(num_persons), abs_values, width=0.8, color='r')
    ax1.tick_params(axis='x', labelbottom='off')
    ax1.set_title('Query words: {}'.format(', '.join(query_words)),
                  fontproperties=prop)
    ax2.bar(np.arange(num_persons), rel_values, width=0.8, color='r')
    ax2.set_xticks(np.arange(num_persons) + 0.4)
    ax2.set_xticklabels(names, fontproperties=prop)
    ax2.set_title('Query words (relative): {}'.format(', '.join(query_words)),
                  fontproperties=prop)
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', required=True,
                        help='The path of an input log file')
    parser.add_argument('-q', required=True,
                        help='Query words; which are optionally separated '
                             'by commas')
    args = parser.parse_args()
    main()
