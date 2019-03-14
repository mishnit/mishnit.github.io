In functional programmers, currying is the technique of translating a function which takes multiple arguments into a sequence of functions, each with a single argument.

For example, a function like:

go_to_lunch?(time,place,person)
might be curried to the form:

go_to_lunch?(time)(place)(person)
In this case, go_to_lunch take a single argument (time) and returns an anonymous function which takes a single argument (place). The anonymous function which takes the argument (place) returns a second anonymous function that takes a single argument (person).

I believe the return stack looks like this:

Evaluate who to go to lunch with (person)
Evaluate where to go to lunch with that person (place)
Evaluate what time to go to that place with that person (time)
The biggest reason for doing this that I see is it simplifies each function, making it easier to reason about, and increasing the chance each function is correct.

The human equivalent

I often hear people struggling to make complex decisions that involve many variables.

For example:

Should I change jobs?
Should I reprimand an employee?
Should I talk to my boss about what I’m upset about?
In each case the decision isn’t simple – many factors come into play.

One strategy I use is to curry my decisions, or in human-speak, “separate my decisions.”

Imagine you are considering quitting your job.  A complex decision for sure.

Instead of trying to reason through the decision like this:

quit_job?(why,when,how,next_job)
Try separating the decisions:

Why do you want to quit your job?
When do you want to quit your job?
How do you want to quit your job?
Where do you want to work next?
Just like currying functions, currying decisions makes decisions easier to reason about, and easier to ensure each decision is correct.

I find that writing out my decision on paper, and then breaking it down into as many small decisions as I can, quickly makes a choice obvious.

It might not be an easy path… but at least it’s clear.

Have you tried a similar strategy in your decision making?
