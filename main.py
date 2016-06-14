#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import psycopg2
import argparse
from datetime import datetime, timedelta
import random
import time


def cli_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--days', action='store',
                        dest='days', default=5,
                        type=int)

    parser.add_argument('--chunk_size', action='store',
                        dest='chunk_size', default=100,
                        type=int)

    parser.add_argument('--delay', action='store',
                        dest='delay', default=100,
                        type=int)

    parser.add_argument('--host', action='store',
                        dest='host', default='localhost')

    parser.add_argument('--user', action='store',
                        dest='user', default='test')

    parser.add_argument('--password', action='store',
                        dest='password', default='password')

    parser.add_argument('--database', action='store',
                        dest='database', default='test')

    return parser.parse_args()


def main():
    args = cli_args()
    conn_string = "host=%(host)s dbname=%(database)s user=%(user)s password=%(password)s" % {'host': args.host,
                                                                                             'database': args.database,
                                                                                             'user': args.user,
                                                                                             'password': args.password}
    db = psycopg2.connect(conn_string)

    affected_rows = args.chunk_size
    date_barrier = (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d")
    while affected_rows == args.chunk_size:
        cursor = db.cursor()
        cursor.execute("DELETE FROM ids WHERE id IN (SELECT id FROM ids WHERE date > '%s' LIMIT %s)" % (date_barrier, args.chunk_size))
        affected_rows = cursor.rowcount
        db.commit()
        print "%s rows deleted" % affected_rows

        sleep_delay = random.randint(args.delay/4, args.delay) / float(1000)
        print "Delay = %s" % sleep_delay
        time.sleep(sleep_delay)

        cursor.close()

    db.close()

if __name__ == "__main__":
    main()
