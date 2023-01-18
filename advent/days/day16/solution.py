from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from itertools import product
from queue import PriorityQueue

from typing import Iterator, Literal, NamedTuple, Self
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


class RawValve(NamedTuple):
    name: str
    flow_rate: int
    following: list[str]

    @classmethod
    def parse(cls, line: str) -> Self:
        return valve_parser.parse(line).get()


@dataclass(slots=True)
class Valve:
    name: str
    flow_rate: int
    following: list[Valve]
    paths: dict[str, int] = field(default_factory=dict, init=False)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Valve):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __lt__(self, other: Valve) -> bool:
        return self.name < other.name

    def __repr__(self) -> str:
        return f"{self.name}:{self.flow_rate}->{','.join(v.name for v in self.following)}"

    def travel_time(self, to: str) -> int:
        return self.paths[to]

    def create_paths(self):
        paths: dict[str, tuple[int, bool]] = {}
        to_check: list[tuple[Valve, int]] = [(self, 0)]
        while to_check:
            current, steps = to_check[0]
            to_check = to_check[1:]

            paths[current.name] = steps, (current.flow_rate > 0)
            for next in current.following:
                known_path, _ = paths.get(next.name, (steps + 2, False))
                if known_path > steps + 1:
                    to_check.append((next, steps + 1))

        self.paths = {name: steps
                      for name, (steps, has_valve) in paths.items()
                      if has_valve is True}


class Actor(NamedTuple):
    position: Valve
    next_time: int

    @property
    def finished(self) -> bool:
        return self.next_time <= 0


@dataclass(slots=True, frozen=True, kw_only=True)
class SystemProgress(ABC):
    time: int
    pressure: int
    flow_rate: int
    closed_valves: list[Valve]

    def next_steps_for(self, actor: Actor) -> Iterator[Actor]:
        if actor.next_time != self.time:
            yield actor

        else:
            reached_any_target = False
            for target in self.closed_valves:
                next_time = self.time - (actor.position.travel_time(target.name) + 1)
                if next_time > 0:
                    reached_any_target = True
                    yield Actor(target, next_time)

            if not reached_any_target:
                yield Actor(actor.position, 0)

    @classmethod
    def create(cls, run_time: int,
               valves: dict[str, Valve], start: str,
               num_actors: Literal[1] | Literal[2]) -> SystemProgress:
        closed_valves = list(sorted(valve for valve in valves.values() if valve.flow_rate > 0))
        start_valve = valves[start]
        for valve in valves.values():
            if valve.name == start or valve.flow_rate > 0:
                valve.create_paths()

        match num_actors:
            case 1:
                return OneActorProgress(time=run_time,
                                        pressure=0,
                                        flow_rate=0,
                                        closed_valves=closed_valves,
                                        actor=Actor(start_valve, run_time))
            case 2:
                return TwoActorProgress(time=run_time,
                                        pressure=0,
                                        flow_rate=0,
                                        closed_valves=closed_valves,
                                        actor1=Actor(start_valve, run_time),
                                        actor2=Actor(start_valve, run_time))
            case _:
                assert False, "Unreachable"

    def __lt__(self, other: OneActorProgress) -> bool:
        if self.time != other.time:
            return self.time > other.time
        return self.min_potential_pressure() > other.min_potential_pressure()

    @abstractmethod
    def open_valves(self) -> Iterator[SystemProgress]:
        ...

    @abstractmethod
    def info(self) -> str:
        ...

    @abstractmethod
    def min_potential_pressure(self) -> int:
        ...

    @abstractmethod
    def still_possible(self) -> int:
        ...

    def max_potential_pressure(self) -> int:
        return self.min_potential_pressure() + self.still_possible()


@dataclass(slots=True, frozen=True)
class OneActorProgress(SystemProgress):
    actor: Actor

    def min_potential_pressure(self) -> int:
        return self.pressure + self.flow_rate * self.time

    def still_possible(self) -> int:
        result = 0
        for valve in self.closed_valves:
            time = self.actor.position.travel_time(valve.name) + 1
            if self.time > time:
                result += (self.time - time) * valve.flow_rate
        return result

    def open_valves(self) -> Iterator[SystemProgress]:
        for actor in self.next_steps_for(self.actor):
            closed_valves = self.closed_valves.copy()
            if not actor.finished:
                closed_valves.remove(actor.position)
                flow_rate = self.flow_rate + actor.position.flow_rate
            else:
                flow_rate = self.flow_rate

            yield OneActorProgress(
                time=actor.next_time,
                flow_rate=flow_rate,
                pressure=self.pressure + self.flow_rate * (self.time - actor.next_time),
                closed_valves=closed_valves,
                actor=actor,
            )

    def info(self) -> str:
        return ",".join(valve.name for valve in self.closed_valves)


@dataclass(slots=True, frozen=True)
class TwoActorProgress(SystemProgress):
    actor1: Actor
    actor2: Actor

    def min_potential_pressure(self) -> int:
        pressure = self.pressure + self.flow_rate * self.time
        if self.actor1.next_time != self.time:
            pressure += self.actor1.position.flow_rate * self.actor1.next_time
        if self.actor2.next_time != self.time:
            pressure += self.actor2.position.flow_rate * self.actor2.next_time
        return pressure

    def still_possible(self) -> int:
        result = 0
        for valve in self.closed_valves:
            t1 = self.actor1.position.travel_time(valve.name)
            t2 = self.actor2.position.travel_time(valve.name)
            time = min(t1, t2) + 1
            if self.time > time:
                result += (self.time - time) * valve.flow_rate
        return result

    def open_valves(self) -> Iterator[SystemProgress]:
        actor1_actions = self.next_steps_for(self.actor1)
        actor2_actions = self.next_steps_for(self.actor2)

        for actor1, actor2 in product(actor1_actions, actor2_actions):
            if actor1.position == actor2.position:
                continue

            closed_valves = self.closed_valves.copy()
            next_time = max(actor1.next_time, actor2.next_time, 0)

            flow_rate = self.flow_rate
            if next_time > 0:
                if actor1.position in closed_valves:
                    closed_valves.remove(actor1.position)
                if actor1.next_time == next_time:
                    flow_rate += actor1.position.flow_rate

                if actor2.position in closed_valves:
                    closed_valves.remove(actor2.position)
                if actor2.next_time == next_time:
                    flow_rate += actor2.position.flow_rate

            next = TwoActorProgress(
                time=next_time,
                flow_rate=flow_rate,
                pressure=self.pressure + self.flow_rate * (self.time - next_time),
                closed_valves=closed_valves,
                actor1=actor1,
                actor2=actor2,
            )
            yield next

    def info(self) -> str:
        opening = ""
        if self.actor1.next_time != self.time:
            opening = self.actor1.position.name
        if self.actor2.next_time != self.time:
            opening = self.actor2.position.name

        closed = ",".join(valve.name for valve in self.closed_valves)
        if opening:
            return f"{closed}+{opening}"
        else:
            return closed


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
        queue: PriorityQueue[SystemProgress] = PriorityQueue()
        queue.put(SystemProgress.create(
            run_time=minutes,
            valves=self.valves,
            start="AA",
            num_actors=number_actors
        ))
        min_pressure = 0
        known: dict[str, int] = {}
        ticks = 0
        drop_known = 0
        drop_pressure = 0
        while not queue.empty():
            ticks += 1
            current = queue.get()
            if current.time == 0:
                print(f"{ticks=} {drop_known=} {drop_pressure=} {len(known)=}")
                return current.pressure

            info = current.info()
            prev_pressure = known.get(info)
            if prev_pressure is not None and prev_pressure >= current.pressure:
                drop_known += 1
                continue
            known[info] = current.pressure

            if min_pressure > current.max_potential_pressure():
                drop_pressure += 1
                continue
            min_pressure = max(min_pressure, current.min_potential_pressure())
            min_pressure = min_pressure

            for next in current.open_valves():
                queue.put(next)

        raise Exception("No best System found")
