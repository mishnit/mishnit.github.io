---
title: "Python Concurrency: The Tricky Bits"
date: 2020-02-05
url: /concurrency
draft: false
description: "An exploration of threads, processes, and coroutines in Python, with interesting examples that illuminate the differences between each."
tags: ["concurrency"]
categories: ["concurrency"]

images:
- cpu.jpg
autoCollapseToc: true
twitter:
- card: "summary_large_image"

---

**An exploration of threads, processes, and coroutines in Python, with interesting examples that illuminate the differences between each.**

![](/cpu.jpg) Credit:[^4]

# Motivation

As [a data scientist who is spending more time on software engineering](https://hamel.dev/), I was recently forced to confront an ugly gap in my knowledge of Python: concurrency.  To be honest, I never completely understood how the terms async, threads, pools and coroutines were different and how these mechanisms could work together.  Every time I tried to learn about the subject, the examples were a bit too abstract for me, and I hard time internalizing how everything worked.  

This changed when a friend of mine[^6] recommended [a live coding talk](https://youtu.be/MCs5OvhV9S4) by [David Beazley](https://www.dabeaz.com/), an accomplished Python educator.  

_Because of restrictions with this YouTube video, I couldn't embed [the video](https://youtu.be/MCs5OvhV9S4) in this article, so you will have to open it in a different window_.

This talk is incredibly intimidating at first.  Not only is it coded live from scratch, but it also jumps immediately into socket programming, something that I had never encountered as a data scientist.  However, if you go through it slowly and understand all the components (as we do in this blog post) it turns out to be the best educational material on Python concurrency I have ever encountered.  This blog post documents what I learned along the way so others can benefit, too.

# Prerequisites

Before getting started, David sets up the following infrastructure that is used to demonstrate concurrency.

## A cpu-bound task: Fibonacci

To demonstrate concurrency, it is useful to create a task that can saturate your CPU (such as mathematical operations) for a noticeable period of time.  David uses a function that computes a [Fibonacci number](https://en.wikipedia.org/wiki/Fibonacci_number).

```py3
#fib.py
def fib(n):
    if n <= 2: return 1
    else: return fib(n-1) + fib(n-2)
```

This function takes much longer for large inputs versus smaller inputs[^1], which allows us to profile different workloads.

## A Simple Web Server

A web server is one of the best ways to illustrate different types of concurrency.  However, to really demonstrate how things work it is useful to use something that is sufficiently low level enough to see how all the pieces work.  For this, David sets up a web server using socket programming.  If you aren't familiar with socket programming, I'll explain the important bits below, but feel free to dive deeper [with this tutorial](https://ruslanspivak.com/lsbaws-part1/) later if you like.

To begin with, David starts with the below code (I've highlighted the most interesting bits):

```python3 {hl_lines=[11,13,17,21]}
# server-1.py
from socket import *
from fib import fib 

def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
    sock.bind(address)
    sock.listen(5)
    while True:
        client,addr = sock.accept()  # waits for a connection to be established
        print("Connection", addr)
        fib_handler(client) # passes the client to a handler which will listen for input data.
        
def fib_handler(client):
    while True:
        req = client.recv(100)  # waits for data that sent by the client.
        if not req: break
        result = fib(int(req))
        resp = str(result).encode('ascii') + b'\n'
        client.send(resp) # sends data back to the client.
    print("Closed")
    
fib_server(('', 25000))
```

Here is an explanation of this code:

- Lines 6-9 are socket programming boilerplate.  It's ok to just take this for granted as a reasonable way to set up a socket server.  This also matches the [the tutorial](https://ruslanspivak.com/lsbaws-part1/) I linked to above.
- Line 11 waits for an incoming connection from a client.  Once a connection is made, the server can begin receiving data from a client.  The code will stop execution on this line until a connection is made.
- Line 13: Once a connection is established, the client object is passed to a function which can handle data sent by the client.
- Line 17: waits for data to be sent by the client.  The code will stop execution on this line until data is received from the client.
- Line 21: The server sends a response back to the client.  The code _could_ stop execution on this line if the send buffers are full, but unlikely in this toy example.

# Testing the non-concurrent code

In the above example, the server will only be able to accept a connection from a single client, because the call to `fib_handler` will never return (because it will run in an infinite loop unless a kill signal is received).  This means that `sock.accept()` can only be called once.

You can test this out by first running the server:
```bash
python server-1.py
```

Then establish a client:
```bash
telnet localhost 25000
```

You can type numbers in [as David does in his video](https://youtu.be/MCs5OvhV9S4?t=293) and verifies that fibonacci numbers are returned.  However, if you try to connect with another client at the same time from a different terminal session:

```bash
telnet localhost 25000
```

You will notice that the second client just hangs and doesn't return anything from the server.  This is because the server is only able to accept a single connection.  Next, we explore how to tackle this issue.

# Threads

We can solve this issue with threads.  You can add threads to the handler so that more connections can be accepted with the following code highlighted in yellow:

```py3 {hl_lines=[3,13]}
from socket import *
from fib import fib
from threading import Thread

def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
    sock.bind(address)
    sock.listen(5)
    while True:
        client,addr = sock.accept()
        print("Connection", addr)
        Thread(target=fib_handler, args=(client,)).start()
        
def fib_handler(client):
    while True:
        req = client.recv(100) 
        if not req: break
        result = fib(int(req))
        resp = str(result).encode('ascii') + b'\n'
        client.send(resp)
    print("Closed")
    
fib_server(('', 25000))
```

You can verify that this works by connecting two separate clients to the server by running the following command in two separate terminal windows: 

```bash
telnet localhost 25000
```

By executing the `fib_handler` in a thread, the main while loop in `fib_server` will continue, allowing `sock.accept()` to receive additional clients.  If you haven't encountered threads before [this tutorial](https://realpython.com/intro-to-python-threading/) provides a good introduction to the topic.

## Thread performance & the GIL

When code stops execution and waits for an external event to occur (like a connection to be made, or data to be sent), this is often referred to as [blocking](https://stackoverflow.com/questions/2407589/what-does-the-term-blocking-mean-in-programming).

One important utility of threads is that it allows blocking tasks to release control of the CPU when the CPU is not being used.  However, the Python interpreter can only run on one thread at a time due to the [Global Interpreter Lock](https://wiki.python.org/moin/GlobalInterpreterLock).  Because Python can only run a single thread at any given time, any CPU-bound work in threads must take turn running one after the other.

Therefore, you have to think carefully about what kind of tasks you execute in threads with Python.  If you try to execute CPU bound tasks, these tasks will slow each other down.  David demonstrates this with the below script that sends requests to our threaded server:

```py
#perf1.py
from socket import *
import time

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('localhost', 25000))

while True:
    start = time.time()
    sock.send(b'30')
    resp = sock.recv(100)
    end = time.time()
    print(end-start)
```

If you run several instances of this script (after starting the server first):

```bash
python perf1.py
```

You will see the execution times for each script linearly increase as you increase the number of these scripts running in parallel.  **For this particular task, adding threads does not make anything faster.  But why?**  This is because the fibonacci task is CPU bound so threads will compete with each other for resources.

Python threads work by interleaving the execution of different tasks on your CPU.[^5]  Only one thread runs at a time, and have the ability to take turns executing in small bits until all threads are done.  The details of how thread processing is interleaved is carried out by the GIL and your operating system, so you need not worry about this detail (with one exception mentioned below).  Interleaving a bunch of CPU bound tasks will not speed up the total runtime of those tasks.  However, if your tasks involve lots of non-CPU time, such as waiting for network connections, or disk I/O, threading tasks may result in a considerable speedup.  A canonical way of simulating a non-cpu bound task in python is to use the built-in function `time.sleep()`.  

To check my understanding about threads and performance, I ran the below experiment[^7] and changed `time.sleep(2)` to `fib(20)` and back again:

```py {hl_lines=[4,8]}
import logging
import threading
import time
import fib

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)  ## Change this line of code to fib(20)
    logging.info("Thread %s: finishing", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    start = time.time()
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    threads = list()
    for index in range(3):
        logging.info("Main    : create and start thread %d.", index)
        x = threading.Thread(target=thread_function, args=(index,))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)
    end = time.time()
    print(f'total time: {end-start}')
```

As expected, increasing the number of threads while running `time.sleep(2)` did not increase the program's overall execution time (the program runs in roughly 2 seconds).  On the other hand, replacing `time.sleep(2)` with `fib(20)` causes this program's running time to increase as more threads are added. This is because `fib(20)` is a cpu bound task so interleaving the task doesn't really help much.  You should try running the same thing to see for yourself.

> You will often hear that Python is not good at parallelism and that you can only run on one CPU core at a time.  This is likely referring to the aforementioned issues with threads and the GIL.  Because you are limited to one thread, this  means that thread-based tasks can only use one CPU core at a time (a single thread cannot run across multiple CPUs).  Outside of Python, threads are a popular choice for parallelizing CPU-bound tasks because you are able to run a separate thread per CPU core simultaneously.  However, with Python you must look for other ways to accomplish parallelism for cpu-bound tasks.

Another interesting but less known aspect that David discusses is the relation between the following two types of tasks:

1. things that take much longer to compute on the CPU, like `fib(30)`, _demonstrated with  [perf1.py](https://github.com/dabeaz/concurrencylive/blob/master/perf1.py)_.
2. things that compute relatively fast on the CPU, like `fib(1)`, _demonstrated with [perf2.py](https://github.com/dabeaz/concurrencylive/blob/master/perf2.py)_.

The Python GIL will prioritize the first type of task at the expense of the second if they are made to compete for resources in threads.  You can optionally follow along with a demonstration of this [here](https://youtu.be/MCs5OvhV9S4?t=568).  This is interesting because this is the opposite of how typical operating systems prioritize threads (by favoring shorter running tasks) and is something unique to the implementation of the Python GIL.  More importantly, this behavior has a very practical consequence: if you are running a web-server where most tasks are fairly quick, an expensive cpu-bound task can grind everything to a halt.

## Threads are not just about making things faster

It is tempting to think of Python threads as a tool to make things run faster, but that's not the only use case.  Recall that the socket server used threads to allow multiple connections at once without any speedup.  David illustrates another way to use threads with his code used to measure the runtime of short-running tasks: 

[perf2.py](https://github.com/dabeaz/concurrencylive/blob/master/perf2.py):
```py3 {hl_lines=[3, 15, 18]}
# perf2.py
# requests/sec of fast requests
from threading import Thread
from socket import *
import time

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('localhost', 25000))

n = 0

def monitor():
    global n
    while True:
        time.sleep(1)
        print(n, 'reqs/sec')
        n = 0
Thread(target=monitor).start()

while True:
    sock.send(b'1')
    resp =sock.recv(100)
    n += 1
```

In this case, David uses a single thread with a blocking call to `sleep(1)` to make sure that `monitor` only prints once per second, while allowing the rest of the program to send requests hundreds of times per second.  In other words, this is a clever use of threads and blocking that allow part of a program to run at a desired time interval while allowing the rest of the program to run as usual. [^2]  

These different angles of looking at threads allowed me to understand threads more holistically.  Threads are not only about making certain things run faster or run in parallel, but also allows you to control how your program is executed.

## How threads work

A thread is always contained in a process, and each process contains one or more threads.  Threads in the same process can share memory which means they can easily communicate and write to common data structures.  Threads are useful in the following two scenarios:

- When there are lots of non-cpu bound tasks (disk I/O, network calls, etc.).
- Outside of Python, if you want to parallelize a CPU bound task by splitting up the task across individual threads running on separate CPU cores. 

A process can span across multiple CPU cores, however a single thread can only utilize one CPU core.

Generally speaking, only one thread can run cpu-bound tasks on a single core at any given time.  If multiple threads are sharing a CPU core, your operating system will interleave these threads.  There are some exceptions  to this rule. For example single CPU cores are able to run multiple threads concurrently by using things like [SMT/hyper-threading](https://en.wikipedia.org/wiki/Simultaneous_multithreading) or compute over data in parallel using [SIMD](https://en.wikipedia.org/wiki/SIMD), which is popular in scientific computing libraries.

On the other hand, processes offer isolation which is helpful when you have different users or different programs that should not be sharing information.  Since we cannot run more than a single thread at a time in Python, a common workaround is to spawn several Python processes.  This is discussed more below.

Chapter 2 of [This book](https://www.amazon.com/Modern-Operating-Systems-Andrew-Tanenbaum/dp/013359162X) discusses what processes and threads are in greater detail from an operating system perspective.

# Processes For CPU Bound Tasks

One way to solve the problem with the GIL and cpu-bound tasks competing for resources is to use processes instead of threads.  Processes are different from threads in the following respects:

- Python threads share a memory space, whereas each process has a separate memory space.  This is an important consideration if you need to share variables or data between tasks.
- Processes have significant overhead compared to threads because data and program state has to be replicated across each process.
- Unlike Python threads, processes are not constrained to run on a single CPU, so you can execute cpu-bound tasks in parallel on different cores.

David uses python processes in his server example by using a process pool.[^3]  The relevant lines of code are highlighted below:

```py {hl_lines=[7, 9, "27-28"]}
# server-3.py
# Fib microservice

from socket import *
from fib import fib
from threading import Thread
from concurrent.futures import ProcessPoolExecutor as Pool

pool = Pool(4)

def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        print("Connection", addr)
        Thread(target=fib_handler, args=(client,), daemon=True).start()

def fib_handler(client):
    while True:
        req = client.recv(100)
        if not req:
            break
        n = int(req)
        future = pool.submit(fib, n)
        result = future.result()
        resp = str(result).encode('ascii') + b'\n'
        client.send(resp)
    print("Closed")

fib_server(('',25000))
```

If you then start this version of the server with:
> python server-3.py

And run the profiler [perf2.py](https://github.com/dabeaz/concurrencylive/blob/master/perf2.py), we can make the following observations:

1. The requests/sec are lower than the thread based version, because there is more overhead required to execute tasks in a pool.
2. However, if you also run [perf1.py](https://github.com/dabeaz/concurrencylive/blob/master/perf1.py) it will not materially interfere with the first task (from `perf2.py`), as this will not compete for resources on the same CPU.
3. The above example involves a CPU-bound task (computing the fibonacci number).  However, if we simulated a non CPU-bound task instead such as `time.sleep()`, using processes instead of threads would actually be detrimental to overall performance.  A concrete example of this is provided in the [section below](#a-note-for-data-scientists-processes-vs-threads).

This is a realistic example that allow you to gain more intuition about how threads and processes work. [This tutorial](https://realpython.com/python-concurrency) contains more examples of Python processes and threads.

## A note for data scientists: processes vs. threads

I've found many data scientists (formerly including myself) blindly apply processes and completely ignore threads.  I understand why - processes are a kind of least common denominator where you can achieve some kind of parallelism regardless of if your task is CPU bound or not. However, I've found that this approach is very suboptimal and prevents full utilization of compute sources.  Some examples to clarify where threads or processes might be more appropriate:

- If you are downloading lots of files from the internet, consider using threads.  This is because most of your time is spent on network I/O, not on the CPU. For example, [this article](https://realpython.com/python-concurrency/) demonstrates a 50% speedup when using threads compared to processes for downloading files.

- If you are transforming or cleaning a large dataset, this work is mostly CPU bound so using processes makes sense.  The only part of this that isn't CPU-bound is reading and writing the data to disk.

- If you just want to load a bunch of files into memory or write a bunch of files to disk, without really doing any transformations, consider using threads as the work is mostly disk I/O and not CPU bound. 

- Keep in mind that threads can be more memory efficient than processes because of [differences in the way they work](#how-threads-work).  So using lots of processes when you don't need them can lead to memory bloat.

**Most importantly**, try avoid having to think about processes and threads where you can and use scientific computing libraries like [numpy](https://numpy.org/) and write [vectorized](https://realpython.com/numpy-array-programming/) operations wherever you can.  It is always worth being aware of the concurrency tools available in the library or framework you are using (especially numerical computing and other data science libraries) and consider using them when appropriate.

# Asynchronous programming

Recall that Python can only operate on one thread at a time, and the operating system automatically decides when to interrupt each thread to allow the threads to take turns running.  This is called [pre-emptive multitasking](https://en.wikipedia.org/wiki/Preemption_%28computing%29#Preemptive_multitasking) since the operating system, not you, determine when your thread makes the switch.  When you don't care about how tasks are interleaved, threads are great because you don't have to worry about how they are scheduled.

However, there is third type of concurrency paradigm in Python that allows you to control how this switching occurs: Asynchronous Programming.  This is also called [cooperative multitasking](https://en.wikipedia.org/wiki/Cooperative_multitasking) which means each task must announce when it wants to switch. One way to achieve cooperative multitasking is to create a [coroutine](https://www.geeksforgeeks.org/coroutine-in-python/).

One way to create coroutines in Python is by using the `yield` statement.  David provides some intuition on how you can achieve multi-tasking with yield in the following code:

```py
from collections import deque

def countdown(n):
    while n > 0:
        yield n
        n -=1

tasks = deque()
tasks.extend([countdown(10), countdown(5), countdown(20)])

def run():
    while tasks:
        task = tasks.popleft()
        try:
            x=next(task)
            print(x)
            tasks.append(task)
        except StopIteration: print("Task")
```

When you run this code, you can see from the output the three countdown tasks are being interleaved:

```
> run()

10
5
20
9
4
19
8
3
18
...
```

This clever use of `yield` allows you to pause execution of a task and move onto a different task kind of like threading, except **you**, not the operating system are controlling how compute is interleaved.  This is the key intuition for understanding the rest of the talk, which goes on to to push this example further.

One of the most popular ways to accomplish async programming is by using the various utilities in the built-in [asyncio](https://docs.python.org/3/library/asyncio.html) module, which uses similar yield statements under the hood. I didn't end up diving deeply into the asyncio module or this particular flavor of programming as my goal was to understand the concept so that I wouldn't be lost when encountering this in the wild.

# Conclusion

There is no silver bullet with regards to choosing the correct type of concurrency in Python.  You have to consider how much of your task is CPU bound vs non-CPU bound (and if it is feasible to break up the task appropriately) to determine whether tweaking your code will make a material difference.

Most importantly, I recommend only reaching for these tools when you need them rather than trying to prematurely optimize your code.  **Always start with the simplest code, without any concurrency, and build incrementally from there.**  If you do add concurrency, make sure you can justify it through a measurable difference in performance or functionality.  I've sometimes found that my code was slow in places I didn't expect and that concurrency wasn't the tool I needed at all! 

Profiling your code is beyond the scope of this blog post, however I hope this post demystified the confusing jungle of terminology of python concurrency so that you can more quickly navigate these topics in the future.

# Other Notes

Not all programs that run in Python using threads are limited to a single CPU.  It is possible to escape the constraints of the GIL by carefully writing C code that has a Python interface.  This is what popular scientific computing libraries such as [NumPy and SciPy](https://scipy.github.io/old-wiki/pages/ParallelProgramming) do to achieve parallelism.

In David's code, [deque](https://docs.python.org/3/library/collections.html#collections.deque) from the `collections` module was introduced, which is a very handy data structure not only for async programming but also for threads because they are thread-safe, which means that you don't have to worry about [race conditions](https://realpython.com/intro-to-python-threading/#race-conditions). Similarly, the [queue](https://docs.python.org/3/library/queue.html) module provides other types of thread-safe queues.

Furthermore, one of my favorite python libraries, [fastcore](https://fastcore.fast.ai/), contains a module called [parallel](https://fastcore.fast.ai/parallel.html) which makes using threads and processes easy for many use cases.  

## Terminology

The following is terminology associated with Python concurrency that is often confused that we didn't touch on in this blog post:

- **Concurrency**: this means creating programs do more than one thing at a time.  It does not mean parallelization.  If two parts of a program take turns executing until they are both complete this is concurrency even if they don't run any faster than if run separately.
- **Multiplexing**: this means sharing resources.
- **Mutex**: (stands for Mutual Exclusion) this is used to enforce exclusive access to a resource across threads to avoid race conditions. 

## Resources & Thanks

- [GitHub repo](https://github.com/dabeaz/concurrencylive) that contains David's code.
- The PyCon [youtube video](https://youtu.be/MCs5OvhV9S4) for this talk.
- David's [page](https://www.dabeaz.com/) including links to courses.  I recently took David's [Advanced Python class](https://www.dabeaz.com/advprog.html) and it was excellent.
- I read the first two chapters of [this book](https://www.amazon.com/Modern-Operating-Systems-Andrew-Tanenbaum/dp/013359162X) on operating systems to research how processes and threads worked. However, I've been told[^8] that [this free book](https://pages.cs.wisc.edu/~remzi/OSTEP/) and [this book](https://www.amazon.com/Advanced-Programming-UNIX-Environment-3rd/dp/0321637739) are good choices as well.

Thanks to [Jeremy Howard](https://twitter.com/jeremyphoward), [Dan Becker](https://twitter.com/dan_s_becker), and [Zach Mueller](https://twitter.com/TheZachMueller)  for reviewing this post.

[^1]: This fibonacci algorithm runs in O(2<sup>n</sup>) time.
[^2]: If the `monitor` task took any meaningful CPU time then the rest of the program would not run as "usual" because it might be competing for resources.  But that is not the case here.
[^3]: One of the most popular ways of using process pools is with the built-in [multiprocessing](https://docs.python.org/3/library/multiprocessing.html) module.
[^4]: Photo is from Luan Gjokaj on [UnSplash](https://unsplash.com/photos/nsr4hePZGYI).
[^5]: Python threads are idiosyncratic because of the [Global Interpreter Lock](https://wiki.python.org/moin/GlobalInterpreterLock) (GIL), which prevent multiple threads from executing code Python code at once.  It is important not to confuse the behavior of Python threads with threads generally.
[^6]: That friend is  [Jeremy Howard](https://www.fast.ai/about/#jeremy).  He kept recommending the talk to me anytime the topic of concurrency came up.  I eventually caved and decided to really focus on this talk.
[^7]: Code is originally from [this tutorial on threads](https://realpython.com/intro-to-python-threading/#working-with-many-threads).
