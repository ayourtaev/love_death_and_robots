import re

from models import Landmark
from utils import session_scope

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

LEFT = -1
RIGHT = 1

SIDES_OF_WORLD = {'north': NORTH, 'east': EAST, 'south': SOUTH, 'west': WEST}
ALL_SIDES_OF_THE_WORLD = ['north', 'east', 'south', 'west']
LEFT_RIGHT = {'left': LEFT, 'right': RIGHT}


class RoutingPointObj:
    def __init__(self, start_point='', end_point=''):
        self.start_point = start_point
        self.end_point = end_point

    def __repr__(self):
        return '"start_point": {start_point} ' \
               '"end_point": {end_point}'.format(start_point=self.start_point,
                                                 end_point=self.end_point)


class RoutingException(Exception):
    def __int__(self, message=''):
        self.message = 'Routing mechanism can\'t handle this route, plz adhere to the established format'


class RouteParser:
    routing_points = []
    looking_at = 0

    def _parse_command(self, data):
        original_command = next(data)
        command = original_command.lower()
        if 'start' in command:
            return self._parse_start_command(command)
        elif command.lower().startswith('turn'):
            return self._parse_turn_command(command, data)
        elif 'landmark' in command:
            return self._get_landmark_point(original_command)
        elif {'north', 'south', 'west', 'east'}.intersection(command.split(' ')):
            return self._calc_distance_with_side(command)
        else:
            # that's mean command like 'go 3 blocks
            return self._calc_distance(command)

    @staticmethod
    def _get_landmark_point(command):
        # search landmark by name
        landmark_name = re.search(r"'(.*?)'", command, re.DOTALL).group(1)
        with session_scope() as session:
            landmark = session.query(Landmark).filter_by(name=landmark_name).scalar()
            return landmark.coordinate

    def parse_routing_points(self, route):
        result = []
        data = self._read_route_file(route)
        try:
            while True:
                stop_point = self._parse_command(data)
                self.routing_points.append(stop_point)
        except StopIteration:
            for idx, val in enumerate(self.routing_points):
                try:
                    result.append([val, self.routing_points[idx + 1]])
                except IndexError:
                    break
            return result

    @staticmethod
    def _parse_start_command(command):
        pattern = '\((.+?)\)'
        result = re.search(pattern, command)
        if result:
            return result.group()

    @staticmethod
    def _read_route_file(file):
        f = open(file, 'r')
        while True:
            data = f.readline().rstrip()
            if not data:
                break
            yield data

    def _parse_turn_command(self, command, data):
        # this method should parse the command like 'Turn right/left'
        # return new side of the world
        turn_command = command.lower()

        side_str = 'right' if 'right' in turn_command else 'left'
        side = int(LEFT_RIGHT[side_str])

        if self.looking_at + side < 0:
            self.looking_at = 3
        elif self.looking_at + side > 3:
            self.looking_at = 0
        else:
            self.looking_at = self.looking_at + side

        # according to rules after turn we should start movement to landmark or just go to some blocks
        next_original_command = next(data)
        next_command = next_original_command.lower()
        if 'landmark' in next_command:
            landmark = self._get_landmark_point(next_original_command)
            if self._is_landmark_valid(self._get_current_point(), self._convert_points(landmark)):
                return landmark
            else:
                # unit never meet that landmark
                raise RoutingException
        else:
            return self._calc_distance(next_command)

    def _get_current_point(self):
        if self.routing_points:
            current_point = self.routing_points[-1]
            return self._convert_points(current_point)
        else:
            raise RoutingException

    def _calc_distance_with_side(self, command):
        next_view = set(ALL_SIDES_OF_THE_WORLD).intersection(command.split(' ')).pop()
        self.looking_at = SIDES_OF_WORLD[next_view]
        return self._calc_distance(command)

    def _is_landmark_valid(self, current_point, landmark):
        curr_x, curr_y = current_point
        land_x, land_y = landmark

        if (self.looking_at == NORTH and land_y < curr_y) or \
                (self.looking_at == SOUTH and land_y > curr_y) or \
                (self.looking_at == EAST and land_x < curr_x) or \
                (self.looking_at == WEST and land_x > curr_x):
            return False
        return True

    @staticmethod
    def _convert_points(points):
        '''
        :param points: coordinate points like "(0,0)"
        :return: tuple of int value (0,0)
        '''
        result = [int(s.strip('()')) for s in points.split(',')]
        x, y = result
        return x, y

    def _calc_distance(self, command):
        x, y = self._get_current_point()

        value = [int(s) for s in command.split(' ') if s.isdigit()]
        if len(value) > 1:
            raise RoutingException
        else:
            value = value[0]

        if self.looking_at == NORTH:
            y += value
        elif self.looking_at == EAST:
            x += value
        elif self.looking_at == SOUTH:
            y -= value
        elif self.looking_at == WEST:
            x -= value

        if x < 0: x = 0
        if y < 0: y = 0

        return '({x},{y})'.format(x=x, y=y)
