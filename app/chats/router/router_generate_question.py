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
    "Find the missing number in an array of integers from 1 to N.",
    "Check if a string is a palindrome.",
    "Reverse a linked list.",
    "Implement a stack using an array.",
    "Implement a queue using two stacks.",
    "Find the maximum subarray sum in an array.",
    "Find the first non-repeating character in a string.",
    "Check if two strings are anagrams.",
    "Find the kth smallest element in an unsorted array.",
    "Implement a binary search tree.",
    "Reverse a string without using any built-in functions or libraries.",
    "Find the longest common prefix among an array of strings.",
    "Implement a priority queue.",
    "Remove duplicates from an array in-place.",
    "Check if a number is prime.",
    "Count the number of occurrences of an element in an array.",
    "Find the intersection of two arrays.",
    "Implement a hash table.",
    "Sort an array using merge sort.",
    "Check if a linked list contains a cycle.",
    "Find the factorial of a number.",
    "Find the largest element in an array.",
    "Check if a binary tree is balanced.",
    "Reverse a sentence word by word.",
    "Find the middle element of a linked list.",
    "Sort an array using quicksort.",
    "Check if a string has all unique characters.",
    "Implement a depth-first search (DFS) algorithm.",
    "Find the sum of all elements in a binary tree.",
    "Count the number of vowels in a string.",
    "Implement a doubly linked list.",
    "Check if a string is a valid parentheses expression.",
    "Merge two sorted linked lists.",
    "Find the longest increasing subsequence in an array.",
    "Implement a circular queue.",
    "Find the maximum depth of a binary tree.",
    "Sort an array using selection sort.",
    "Check if a string is an integer.",
    "Reverse the order of words in a string.",
    "Check if a binary tree is a binary search tree.",
    "Find the second smallest element in an array.",
    "Implement a breadth-first search (BFS) algorithm.",
    "Rotate an array to the right by K steps.",
    "Find the common elements in multiple arrays.",
    "Implement a graph using an adjacency list.",
    "Check if a string is a valid palindrome.",
    "Find the median of two sorted arrays.",
    "Remove all duplicates from a string.",
    "Count the number of leaf nodes in a binary tree.",
    "Implement a min heap.",
    "Check if a linked list is a palindrome.",
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