# get_results.py

import utils


def main():
    engine = utils.get_db_engine()
    results = engine.execute('select * from results order by dateof desc limit 1').fetchone()
    prediction = results.prediction

    if prediction >= .6:
        utils.send_email('Take Action', 'Preemptive action may be necessary')


if __name__ == '__main__':
    main()
