import asyncio

from sqlalchemy.orm import joinedload

from models import Route
from robot import Robot
from utils import session_scope

# should be take from environment variables
workers = 1


async def producer():
    while True:
        with session_scope() as session:
            route = session.query(Route).options(joinedload(Route.routing_point)).filter_by(
                is_finished=False).order_by(Route.created_date.desc()).first()
            robot = Robot()
            if route:
                for rp in route.routing_point:
                    robot.move(x=rp.start_point, y=rp.end_point)
                    print('x: {x}\ny: {y}'.format(x=rp.start_point, y=rp.end_point))
                    await asyncio.sleep(2)
                route.is_finished = True
                session.add(route)
            else:
                break


async def processor():
    for i in range(workers):
        asyncio.ensure_future(producer())
