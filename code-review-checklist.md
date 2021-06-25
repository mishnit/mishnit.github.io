# Code Review Checklist

The developer and reviewer both need to focus on below checklist:

  - [Testability](#testability)
  - [Functionality and Code structure](#functionality-and-code-structure)
  - [Coding Conventions and Control Structures](#coding-conventions-and-control-structures)
  - [Documentation](#documentation)
  - [Error Handling](#error-handling)
  - [Resource Leaks](#resource-leaks)
  - [Thread Safety](#thread-safety)
  - [Security](#security)
  - [Positive Review](#positive-review)
  - [Negative Review](#negative-review)
 
# Testability
  - [ ] Code has appropriate unit tests
  - [ ] Tests are well-designed

# Functionality and Code Structure
  - [ ] The code works well
  - [ ] The code covers edge cases
  - [ ] The code is modular and addresses separation of concerns
  - [ ] Law of Demeter (principle of least knowledge) is not violated
  - [ ] Design patterns if used are correctly applied
 
# Coding Conventions and Control Structures
  - [ ] Follows coding conventions
  - [ ] Names are simple and if possible short
  - [ ] Names are spelt correctly
  - [ ] Names contain units where applicable
  - [ ] Enums are used instead of int constants where applicable
  - [ ] There are no usages of 'magic numbers'
  - [ ] All variables are in the smallest scope possible
  - [ ] All class, variable, and method modifiers are correct.
  - [ ] There is no commented out code
  - [ ] There is no dead/unused code (inaccessible at Runtime)
  - [ ] No code can be replaced with library functions
  - [ ] Required logs are present
  - [ ] Frivolous logs are absent
  - [ ] Debugging code is absent
  - [ ] All print statements are commented out
  - [ ] No stack traces are printed
  - [ ] Variables are immutable where possible
  - [ ] Code is not repeated or duplicated
  - [ ] There is an else block for every if clause even if it is empty
  - [ ] No complex/long boolean expressions
  - [ ] No negatively named boolean variables
  - [ ] No empty blocks of code
  - [ ] No empty destructor exists 
  - [ ] Ideal data structures are used
  - [ ] Constructors do not accept null/none values
  - [ ] Collections are initialised with a specific estimated capacity
  - [ ] StringBuilder is used to concatenate strings
  - [ ] Loops have a set length and correct termination conditions
  - [ ] Blocks of code inside loops are as small as possible
  - [ ] Order/index of a collection is not modified when it is being looped over
  - [ ] No methods with boolean parameters

# Documentation
  - [ ] The code is readable and easy to understand 
  - [ ] All methods are commented in clear language.
  - [ ] Comments exist and describe rationale or reasons for decisions in code
  - [ ] All public methods/interfaces/contracts are commented describing usage
  - [ ] All edge cases are described in comments
  - [ ] All unusual behaviour or edge case handling is commented
  - [ ] Data structures and units of measurement are explained

# Error Handling
  - [ ] All data inputs are checked (for the correct type, length/size, format and range)
  - [ ] Invalid parameter values handled such that exceptions are not thrown
  - [ ] Variables are not accidentally used with null values
  - [ ] Arrays are checked for out of bound conditions
  - [ ] Catch clauses are fine grained and catch specific exceptions
  - [ ] Exceptions are not eaten if caught, unless explicitly documented otherwise
  - [ ] APIs and other public contracts check input values and fail fast
  - [ ] Files/Sockets/Cursors and other resources are properly closed even when an exception occurs in using them
  - [ ] Null/None are not returned from any method
  - [ ] Floating point numbers are not compared for equality
  - [ ] Methods return early without compromising code readability
 
# Resource Leaks
  - [ ] No object exists longer than necessary
  - [ ] No memory leaks

# Thread Safety
  - [ ] Objects accessed by multiple threads are accessed only through a lock, or synchronized methods.
  - [ ] Race conditions have been handled
  - [ ] Locks are acquired and released in the right order to prevent deadlocks, even in error handling code.
  - [ ] StringBuffer is used to concatenate strings in multi-threaded code

# Security
  - [ ] No sensitive information is logged or visible in a stacktrace
  - [ ] Encryption if used anywhere is strong enough
  - [ ] Secret keys, passwords and tokens etc are not hard coded
  - [ ] Short-Lived access token and Long-Lived refresh token are being used for session security
  - [ ] Auth tokens are being stored via httponly and secure cookies only
  - [ ] New short-lived access token can be renewed by using Long-Lived refresh token
  - [ ] Database contains only hashed values for passwords, secret keys and token

# Positive Review
  - Use +1 to mark LGTM (Looks good to me)
  - Use +2 to mark LPTM (Looks perfect to me)

# Negative Review
  - Use -1 to mark ABSC (Accepted but small change). Mention what is wrong and how it can be fixed in the comment. 
  - Use -2 to mark LBTM (Looks bad to me). Mention what is critical and probably requires rework. Be polite while asking any question in the comment.
  
# Note
  - Code review should be used to develop an environment of learning, which should help to avoid repeating mistakes rather blaming an individual.   
  - Every Pull request requires atleast two positive reviews (single +2 or two +1) from peers to get merged in master.
  - Managers are highly recommended to make static code analysis tools and code profiling tools available to their teammates.
  - Group code reviews can be a great exercise for knowledge sharing.
  - Ideally a reviewer should not spend more than 60 minutes at a time. 
