# Elan testing system backend
Elan is a modern platform and testing system for holding programming contests. It is like [ejudge](https://ejudge.ru/) or [Yandex Contest](https://contest.yandex.ru/), but a way better.

This repository contains API code, please reffer to [another repo](https://github.com/elansteam/runner) for seeing the runner source code.

## Why Elan?
- **Modern.** Elan has a very nice and intuitive UI based on Google Material Design 3 design system.
- **Powerful.** It supports holding IOI and ICPC contests formats, groups creation (could be useful in schools) and online VS Code-like code editor.
- **Self-hosted and open source.** You can deploy Elan on your own and enjoy all its advantages, storing all your data locally on your servers. Say "bye" to closed-source Codeforces & Yandex Contests :)

## What does Elan consist of?
### Elan API (backend)
<p align="center">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi">
  <img src="https://img.shields.io/badge/Rabbitmq-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white">
  <img src="https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white">
</p>
Well-documented JSON API, written on FastAPI Python framework

### Elan Runner
<p align="center">
  <img src="https://img.shields.io/badge/c++-%2300599C.svg?style=for-the-badge&logo=c%2B%2B&logoColor=white">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
</p>
Runner is a low-level engine, a subsystem of Elan, which is responsible for safely running isolated processes that are strictly limited in terms of resource consumption: memory, CPU and real-time, number of threads and file descriptors. Runner is based on the Linux kernel cgroups v2 mechanism. It imposes rlimits and ulimits and keeps track of all system calls of the running process.

Runner is written from scratch on C++, and it has Python API.
