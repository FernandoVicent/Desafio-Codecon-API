from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Project:
    name: str
    completed: bool

@dataclass
class Team:
    name: str
    leader: bool
    projects: List[Project]

@dataclass
class Log:
    date: str
    action: str  # login / logout

@dataclass
class User:
    id: str
    name: str
    age: int
    score: int
    active: bool
    country: str
    team: Team
    logs: List[Log]
