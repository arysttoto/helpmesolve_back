from typing import Any, Optional

import logging

from fastapi import Depends, HTTPException, status
from pydantic import Field

from app.utils import AppModel 

from ..service import Service, get_service
from . import router

from .errors import InvalidCredentialsException

from random import randint 


coding_questions = [
    "What is time complexity?",
    "What is space complexity?",
    "Explain the difference between an array and a linked list.",
    "What is a hash table?",
    "What is a binary search tree?",
    "Explain the difference between BFS and DFS.",
    "What is memoization?",
    "What is dynamic programming?",
    "What is the greedy algorithm?",
    "What is an algorithm?",
    "What is a data structure?",
    "Explain the concept of recursion.",
    "What are the different types of sorting algorithms?",
    "Explain the concept of Big O notation.",
    "What is a stack and a queue?",
    "What is a priority queue?",
    "What is the difference between a stack and a heap?",
    "What is the two-pointer technique?",
    "What is the sliding window technique?",
    "Explain the concept of backtracking.",
    "What is an NP-complete problem?",
    "What is the traveling salesman problem?",
    "What is an adjacency matrix?",
    "Explain the concept of graph traversal.",
    "What is a directed acyclic graph (DAG)?",
    "What is the difference between a function and a method?",
    "What is an abstract data type (ADT)?",
    "Explain the concept of a linked list cycle.",
    "What is an in-place algorithm?",
    "What is a stable sorting algorithm?",
    "Explain the concept of a binary search.",
    "What is a semaphore?",
    "What is the dining philosophers problem?",
    "Explain the producer-consumer problem.",
    "What is the CAP theorem?",
    "What is a cache?",
    "Explain the concept of parallel computing.",
    "What is a race condition?",
    "What is the difference between parallelism and concurrency?",
    "Explain the concept of virtual memory.",
    "What is the role of an operating system?",
    "What is a system call?",
    "Explain the difference between a process and a thread.",
    "What is deadlock?",
    "What is a mutex?",
    "Explain the concept of pipelining in processors.",
    "What is Moore's law?",
    "What is the von Neumann architecture?",
    "Explain the concept of RAID in data storage.",
    "What is the difference between TCP and UDP?",
]


class ResponseModel(AppModel):
    question: str

@router.get("/random", 
            status_code=status.HTTP_201_CREATED,
            response_model=ResponseModel)
def generate_question(
    svc: Service = Depends(get_service),
):
    return ResponseModel(
        question=coding_questions[randint(0, len(coding_questions)-1)]
    ) 