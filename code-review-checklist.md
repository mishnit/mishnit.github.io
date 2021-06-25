## The developer and reviewer both need to focus on below checklist:

- Testability
- Functionality
- Comment and Coding Conventions
- Documentation
- Error Handling
- Control Structures
- Performance
- Resource Leaks
- Thread Safety
- Security
 
# Testability
  - [ ] Code has appropriate unit tests
  - [ ] Tests are well-designed

# Functionality
  - [ ] The code works well
  - [ ] The code covers edge cases
  - [ ] The code is modular and addresses separation of concerns
 
- Comment and Coding Conventions
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
  - [ ] Design patterns if used are correctly applied

- Documentation
  - [ ] The code is readable and easy to understand 
  - [ ] All methods are commented in clear language.
  - [ ] Comments exist and describe rationale or reasons for decisions in code
  - [ ] All public methods/interfaces/contracts are commented describing usage
  - [ ] All edge cases are described in comments
  - [ ] All unusual behaviour or edge case handling is commented
  - [ ] Data structures and units of measurement are explained

- Error Handling
  - [ ] Variables are not accidentally used with null values
  - [ ] Arrays are checked for out of bound conditions
  - [ ] Catch clauses are fine grained and catch specific exceptions
  - [ ] Exceptions are not eaten if caught, unless explicitly documented otherwise
  - [ ] APIs and other public contracts check input values and fail fast
  - [ ] Files/Sockets/Cursors and other resources are properly closed even when an exception occurs in using them
  - [ ] Null/None are not returned from any method
  - [ ] Floating point numbers are not compared for equality

- Control Structures
  - [ ] There is an else block for every if clause even if it is empty
  - [ ] No complex/long boolean expressions
  - [ ] No negatively named boolean variables
  - [ ] No empty blocks of code
  - [ ] No empty destructor exists 
  - [ ] Ideal data structures are used
  - [ ] Constructors do not accept null/none values
  - [ ] Collections are initialised with a specific estimated capacity

- Performance
  - [ ] StringBuilder is used to concatenate strings
  - [ ] Loops have a set length and correct termination conditions
  - [ ] Blocks of code inside loops are as small as possible
  - [ ] Order/index of a collection is not modified when it is being looped over
  - [ ] No methods with boolean parameters
  - [ ] No object exists longer than necessary
 
- Resource Leaks
  - [ ] No memory leaks
  - [ ] Law of Demeter (principle of least knowledge) is not violated
  - [ ] Methods return early without compromising code readability

- Thread Safety
  - [ ] Objects accessed by multiple threads are accessed only through a lock, or synchronized methods.
  - [ ] Race conditions have been handled
  - [ ] Locks are acquired and released in the right order to prevent deadlocks, even in error handling code.
  - [ ] StringBuffer is used to concatenate strings in multi-threaded code

- Security
  - [ ] All data inputs are checked (for the correct type, length/size, format and range)
  - [ ] Invalid parameter values handled such that exceptions are not thrown
  - [ ] No sensitive information is logged or visible in a stacktrace

PS: Developers are highly recommended to use static code analysis tools and code profiling tools   
