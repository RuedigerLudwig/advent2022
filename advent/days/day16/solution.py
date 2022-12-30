from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from itertools import product
from queue import PriorityQueue

from typing import Iterator, Literal, Self
from advent.parser.parser import P

day_num = 16


def part1(lines: Iterator[str]) -> int:
    system = Network.parse(lines)
    return system.under_pressure(30, 1)


def part2(lines: Iterator[str]) -> int:
    system = Network.parse(lines)
    return system.under_pressure(26, 2)


valve_parser = P.map3(
    P.second(P.string("Valve "), P.upper().word()),
    P.second(P.string(" has flow rate="), P.unsigned()),
    P.second(P.either(P.string("; tunnels lead to valves "), P.string("; tunnel leads to valve ")),
             P.upper().word().sep_by(P.string(", "))),
    lambda name, flow_rate, following: RawValve(name, flow_rate, following)
)


@dataclass(slots=True)
class RawValve:
    name: str
    flow_rate: int
    following: list[str]

    @classmethod
    def parse(cls, line: str) -> Self:
        result = valve_parser.parse(line).get()
        return result


@dataclass(slots=True, unsafe_hash=True)
class Valve:
    name: str
    flow_rate: int
    following: list[Valve] = field(hash=False, compare=False)
    paths: dict[str, int] | None = field(default=None, hash=False, init=False, compare=False)

    def __repr__(self) -> str:
        return f"{self.name}:{self.flow_rate}->{','.join(v.name for v in self.following)}"

    def travel_time(self, to: str) -> int:
        if self.paths is None:
            self.create_paths()
        return self.paths[to]  # type: ignore

    def create_paths(self):
        paths: dict[str, int] = {}
        to_check: list[tuple[Valve, int]] = [(self, 0)]
        while to_check:
            current, steps = to_check[0]
            to_check = to_check[1:]

            paths[current.name] = steps
            for next in current.following:
                if paths.get(next.name, steps + 2) > steps + 1:
                    to_check.append((next, steps + 1))
        self.paths = paths


@dataclass(slots=True, frozen=True)
class Actor:
    position: Valve
    next_time: int
    finished: bool


@dataclass(slots=True, frozen=True)
class SystemProgress(ABC):
    max_time: int
    prev_time: int
    time: int
    pressure: int
    flow_rate: int
    closed_valves: frozenset[Valve]
    path: frozenset[tuple[str, int, bool]]

    def one_actor(self, actor: Actor) -> Iterator[Actor]:
        if actor.finished or actor.next_time != self.time:
            yield actor
        elif not self.closed_valves:
            yield Actor(actor.position, self.max_time, True)
        else:
            reached_any_target = False
            for target in self.closed_valves:
                finished = self.time + actor.position.travel_time(target.name) + 1
                if finished < self.max_time:
                    reached_any_target = True
                    yield Actor(target, finished, False)
            if not reached_any_target:
                yield Actor(actor.position, self.max_time, True)

    @classmethod
    def create(cls, max_time: int, pressure: int, flow_rate: int,
               closed_valves: frozenset[Valve], start: Valve,
               num_actors: Literal[1] | Literal[2]) -> SystemProgress:
        match num_actors:
            case 1:
                return OneActorProgress(max_time, 0, 0, pressure, flow_rate, closed_valves,
                                        frozenset(), Actor(start, 0, False))
            case 2:
                return TwoActorProgress(max_time, 0, 0, pressure, flow_rate, closed_valves,
                                        frozenset(), Actor(start, 0, False), Actor(start, 0, False))
            case _:
                assert False, "Unreachable"

    def __lt__(self, other: OneActorProgress) -> bool:
        if self.time != other.time:
            return self.time < other.time
        return self.pressure > other.pressure

    @abstractmethod
    def max_possible_pressure(self) -> int:
        ...

    @abstractmethod
    def open_valves(self) -> Iterator[SystemProgress]:
        ...


@dataclass(slots=True, frozen=True)
class OneActorProgress(SystemProgress):
    actor: Actor

    def max_possible_pressure(self) -> int:
        closed = sum(valve.flow_rate for valve in self.closed_valves)
        return self.pressure + (self.flow_rate + closed) * (self.max_time - self.time)

    def open_valves(self) -> Iterator[SystemProgress]:
        for actor in self.one_actor(self.actor):
            closed_valves = self.closed_valves
            if not actor.finished:
                closed_valves = closed_valves.difference({actor.position})
                flow_rate = self.flow_rate + actor.position.flow_rate
            else:
                flow_rate = self.flow_rate
            next = OneActorProgress(
                max_time=self.max_time,
                prev_time=self.time,
                time=actor.next_time,
                flow_rate=flow_rate,
                pressure=self.pressure + self.flow_rate * (actor.next_time - self.time),
                closed_valves=closed_valves,
                actor=actor,
                path=self.path | {(actor.position.name, actor.next_time, True)}
            )
            yield next


@dataclass(slots=True, frozen=True)
class TwoActorProgress(SystemProgress):
    actor1: Actor
    actor2: Actor

    def max_possible_pressure(self) -> int:
        closed = sum(valve.flow_rate for valve in self.closed_valves)

        other = 0
        if self.actor1.next_time != self.time and not self.actor1.finished:
            other += self.actor1.position.flow_rate * (self.max_time - self.actor1.next_time)
        if self.actor2.next_time != self.time and not self.actor2.finished:
            other += self.actor2.position.flow_rate * (self.max_time - self.actor2.next_time)

        return self.pressure + (self.flow_rate + closed) * (self.max_time - self.time) + other

    def open_valves(self) -> Iterator[SystemProgress]:
        if self.actor1.next_time == self.time:
            actor1_actions = self.one_actor(self.actor1)
        else:
            actor1_actions = [self.actor1]

        if self.actor2.next_time == self.time:
            actor2_actions = self.one_actor(self.actor2)
        else:
            actor2_actions = [self.actor2]

        for actor1, actor2 in product(actor1_actions, actor2_actions):
            if not actor1.finished and not actor2.finished and actor1.position == actor2.position:
                continue

            closed_valves = self.closed_valves
            flow_rate = self.flow_rate
            next_time = min(actor1.next_time, actor2.next_time)

            path: set[tuple[str, int, bool]] = set(self.path)

            if not actor1.finished:
                closed_valves = closed_valves.difference({actor1.position})
                if actor1.next_time == next_time:
                    flow_rate += actor1.position.flow_rate
                    path -= {(actor2.position.name, actor1.next_time, False)}
                    path.add((actor1.position.name, actor1.next_time, True))
                else:
                    path.add((actor1.position.name, actor1.next_time, False))

            if not actor2.finished:
                closed_valves = closed_valves.difference({actor2.position})
                if actor2.next_time == next_time:
                    flow_rate += actor2.position.flow_rate
                    path -= {(actor2.position.name, actor1.next_time, False)}
                    path.add((actor2.position.name, actor2.next_time, True))
                else:
                    path.add((actor2.position.name, actor2.next_time, False))

            next = TwoActorProgress(
                max_time=self.max_time,
                prev_time=self.time,
                time=next_time,
                flow_rate=flow_rate,
                pressure=self.pressure + self.flow_rate * (next_time - self.time),
                closed_valves=closed_valves,
                actor1=actor1,
                actor2=actor2,
                path=frozenset(path)
            )
            yield next


@dataclass(slots=True)
class Network:
    valves: dict[str, Valve]
    paths: dict[tuple[str, str], list[str]] = field(default_factory=dict)

    @classmethod
    def parse(cls, lines: Iterator[str]) -> Self:
        raw_system = [RawValve.parse(line) for line in lines]
        valves = {valve.name: Valve(valve.name, valve.flow_rate, []) for valve in raw_system}
        for raw in raw_system:
            current = valves[raw.name]
            for follow in raw.following:
                current.following.append(valves[follow])

        return Network(valves)

    def under_pressure(self, minutes: int, number_actors: Literal[1] | Literal[2]) -> int:
        closed_valves = [valve for valve in self.valves.values() if valve.flow_rate > 0]
        start = self.valves["AA"]
        queue: PriorityQueue[SystemProgress] = PriorityQueue()
        queue.put(SystemProgress.create(
            max_time=minutes,
            pressure=0,
            flow_rate=0,
            closed_valves=frozenset(closed_valves),
            start=start,
            num_actors=number_actors
        ))
        max_pressure = 0
        seen: set[frozenset[tuple[str, int, bool]]] = set()
        while not queue.empty():
            current = queue.get()
            if current.time == minutes:
                return current.pressure
            if max_pressure > current.max_possible_pressure():
                continue
            if current.path in seen:
                continue
            seen.add(current.path)
            max_pressure = max(max_pressure, current.pressure)

            for next in current.open_valves():
                queue.put(next)

        raise Exception("No best System found")
