import utils
import ranker
from pprint import pprint
import statistics

repetitions = 10
set_size = 1000

for version in [0, 1, 2]:
    utils.title('version {}'.format(version))
    print(f'ranking sets of {set_size} trips ({repetitions} reps)')
    ranking_function = lambda x: ranker.rank_elements(x, version=version)
    info = utils.profile_ranker(ranking_function,
                                set_size=set_size,
                                repetitions=repetitions)
    print('average number of base function calls {}'.format(
        statistics.mean([run['rank_call_count'] for run in info])))
