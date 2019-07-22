import argparse
import sys
import asyncio

from models import (
    Landmark,
    Route,
    RoutingPoint)
from serializers import LandmarkSerializer
from tasks import processor
from utils import session_scope, create_table
from core import RouteParser


def read_command(file):
    f = open(file, 'r')
    while True:
        data = f.readline().rstrip()
        if not data:
            break
        yield data


def handler(args):
    # loaddata
    if args.loaddata:
        route_handler = RouteParser()
        stop_point = route_handler.parse_routing_points(args.loaddata)
        print(stop_point)

        with session_scope() as session:
            route = Route()
            session.add(route)
            session.flush()
            sp_obj = []
            for i in stop_point:
                routing_point = RoutingPoint(start_point=i[0],
                                             end_point=i[1],
                                             base_route=route.id)
                sp_obj.append(routing_point)
            session.add_all(sp_obj)
    # landmark func
    elif args.landmark:
        dr_data, error = LandmarkSerializer().load({'coordinate': args.landmark[0],
                                                    'name': args.landmark[1]})
        if error:
            print(error)
            sys.exit(0)
        with session_scope() as session:
            landmark = Landmark(**dr_data)
            session.add(landmark)
    # robot
    elif args.run:
        print('<<START>>')
        loop = asyncio.get_event_loop()
        loop.run_until_complete(processor())
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            print('<<END>>')
            loop.close()


if __name__ == '__main__':
    create_table()

    parser = argparse.ArgumentParser(description='Robot Navigation')

    parser.add_argument(
        '--loaddata', help='Loading data is easy: just call \'manage.py loaddata <filename>\' where'
                           ' <filename> is the name of the data file you\'ve created'
    )
    parser.add_argument(
        '--landmark', nargs='+', help='Creating landmark is easy: just call \'manage.py landmark <coords>'
                                      '<landmarkname>\' where <coords> is the coordinates of landmark and'
                                      '<landmarkname> is the name of the landmark you\'ve crated'
    )
    parser.add_argument('--run', help='Start to work with your routes')
    args = parser.parse_args()
    handler(args)
