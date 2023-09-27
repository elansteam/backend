"""Кастомные типы данных проекта"""
import typing

ObjectId = typing.NewType("ObjectId", int)
"""ID объекта в базе данных"""
