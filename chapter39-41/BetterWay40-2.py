"""
생명 게임

임의의 크기로 된 2차원 그리드가 있다. 그리드의 각 셀은 살아 있음 또는 죽어 있음이 될 수 있다.

Query 객체를 넘겨주는 count_neighbors 코루틴으로 수행한다. Query 클래스는 직접 정의하고 클래스의 목적은
제너레이터 코루틴이 주변 환경에 정보를 요청할 방법을 제공하는 것이다.
"""
from collections import namedtuple

ALIVE = '*'
EMPTY = '-'
Query = namedtuple('Query', ('y', 'x'))

"""
코루틴은 각 이웃별로 Query를 넘겨준다.
count_neighbors 제너레이터는 이웃의 상태를 확인하고 살아 있는 이웃의 수를 반환 한다.
그리고 send 메서드를 통해 Query에 대응하는 셀의 상태를 받을 것이라고 기대한다.
최종 개수는 제너레이터가 return 문으로 끝날때 일어나는 StopIteration 예외로 반환 된다.
"""

def count_neighbors(y, x):
    n_ = yield Query(y + 1, x + 0)  # North
    ne = yield Query(y + 1, x + 1)  # Northeast
    e_ = yield Query(y + 0, x + 1)  # East
    se = yield Query(y - 1, x + 1)  # Southeast
    s_ = yield Query(y - 1, x + 0)  # South
    sw = yield Query(y - 1, x - 1)  # Southwest
    w_ = yield Query(y + 0, x - 1)  # West
    nw = yield Query(y + 1, x - 1)  # Northwest
    neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0
    for state in neighbor_states:
        if state == ALIVE:
            count += 1
    return count


"""
이제 셀이 이웃 카운터에 대응하도록 새로운 상태로 변할 것을 알릴 기능이 필요하다. 즉 죽을것인지 살릴것인지 말하는것같다
이 작업을 위해서 step_cell 이라는 또 다른 코루틴을 정의하고. 이 제너레이터는 Transition 객체를 얻어와서
셀의 상태 변화를 알린다. 이 코루틴은 좌표의 초기 상태를 얻어오는 Query를 돌려주고 count_neighbors 를 실행하여
주변에 있는 셀들을 조사한다. 그 다음 셀이 어떤 상태가 되어야 하는지 결정하고 객체를 넘겨준다.
"""

Transition = namedtuple('Transition', ('y', 'x', 'state'))


def game_logic(state, neighbors):
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY
        elif neighbors > 3:
            return EMPTY
    else:
        if neighbors == 3:
            return ALIVE
    return state


def step_cell(y, x):
    state = yield Query(y, x)  # 좌표의 초기 상태를 얻어오는 Query
    # yield from 표현식을 통해 코루틴들을 조합, 재사용하여 간단한 코루틴들로 복잡한 코루틴을 구축할수 있다.
    neighbors = yield from count_neighbors(y, x)  # 주변에 있는 셀들을 조사
    next_state = game_logic(state, neighbors)  # 셀이 어떤상태가 되어야 하는지 결정
    yield Transition(y, x, next_state)  # 셀의 다음 상태를 Transition 객체에 넘겨줌


"""
게임의 최종 목표는 그리드의 모든 셀에 이 로직을 똑같은 방식으로 실행하는 것이다.
step_cell 코루틴으로 simulate 코루틴을 구성하여 이렇게 만들어 보자.
simulate 코루틴은 step_cell 여러번 넘겨서 셀로 구성된 그리드를 진행한다. 모든 좌표를 진행 한 후
TICK 객체를 넘겨서 현재 세대의 셀을 모두 반환했음을 알린다.
"""
TICK = object()


def simulate(height, width):
    while True:
        for y in range(height):
            for x in range(width):
                yield from step_cell(y, x)
        yield TICK


"""
simulate에서 인상적인 부분은 외부 환경과 완전히 분리되어 있다는 점이다.
그리드를 파이썬 객체로 표현할 방법과 Query, Transition, TICK 값을 외부에서 처리할 방법. 게임의 초기 상태를
얻을 방법을 정의하진 않았지만 로직은 명확하다.
각 셀은 step_cell을 실행하여 변이하고 그런 다음 게임 클록이 틱(상태 변화한것을 알림?)을 발생시킨다.
이 동작은 simulate 코루틴이 전진하는한 계속 된다.

이것이 바로 코루틴의 장점 중 하나다. ?
코루틴을 이용하면 처리할 로직에 집중할 수 있다. 원하는 작업을 구현한 부분에서 환경에 해당하는 코드의 명령어를
분리할 수 있다(원하는 부분까지만 함수를 실행 할 수 있다는것 같다)
이렇게 분리하면 코루틴을 병렬로 동작하는 것처럼 실행할 수 있다. 또한 시간이 지나서
코루틴을 변경하지 않고 이러한 명령어 이후에 오는 구현을 개선할 수 있다.
(코루틴은 데이터를 변경하는게 아닌 소비하는것이기 때문에 이후에 다른 구현을 한다 하더라도 코루틴을 변경하지 않고
구현을 할 수 있다는것 같다.)
"""


class Grid(object):
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rows = []
        for _ in range(self.height):
            self.rows.append([EMPTY] * self.width)

    def __str__(self):
        output = ''
        for row in self.rows:
            for cell in row:
                output += cell
            output += '\n'
        return output

    def query(self, y, x):
        return self.rows[y % self.height][x % self.width]

    def assign(self, y, x, state):
        self.rows[y % self.height][x % self.width] = state


def live_a_generation(grid, sim):
    progeny = Grid(grid.height, grid.width)
    item = next(sim)
    while item is not TICK:
        if isinstance(item, Query):
            state = grid.query(item.y, item.x)
            item = sim.send(state)
        else:
            progeny.assign(item.y, item.x, item.state)
            item = next(sim)
    return progeny

"""
마지막으로 simulate 에서 넘겨준 값을 해석하는 함수와 그 내부에서 사용하는 코루틴을 모두 정의한다.
이 함수는 코루틴에서 나온 명령어를 주변 환경과의 상호작용으로 변환한다. 셀의 그리드 전체를 한단계
전진시킨 후 다음 상태를 담은 새로운 그리드를 반환한다.
"""
class ColumnPrinter(object):
    def __init__(self):
        self.columns = []

    def append(self, data):
        self.columns.append(data)

    def __str__(self):
        row_count = 1
        for data in self.columns:
            row_count = max(row_count, len(data.splitlines()) + 1)
        rows = [''] * row_count
        for j in range(row_count):
            for i, data in enumerate(self.columns):
                line = data.splitlines()[max(0, j - 1)]
                if j == 0:
                    padding = ' ' * (len(line) // 2)
                    rows[j] += padding + str(i) + padding
                else:
                    rows[j] += line
                if (i + 1) < len(self.columns):
                    rows[j] += ' | '
        return '\n'.join(rows)


grid = Grid(5, 5)
grid.assign(1, 1, ALIVE)
grid.assign(2, 2, ALIVE)
grid.assign(2, 3, ALIVE)
grid.assign(3, 3, ALIVE)
columns = ColumnPrinter()
sim = simulate(grid.height, grid.width)
for i in range(5):
    columns.append(str(grid))
    grid = live_a_generation(grid, sim)
print(columns)

"""
이 방법의 백미는 주변 코드를 업데이트 하지 않아도 game_logic 함수를 변경할 수 있다는점이다.
코루틴은 데이터를 동시에 소비하게 하는것이지 변경이 아니여서 기존의 메커니즘이 바뀌여도 코루틴을 바꿀 필요가 없다. 
이는 코루틴이 어떤 방법으로 관심 영역의 분리를 가능하게 하는지 보여준다.
"""