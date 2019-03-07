# Python 3 program to print frequencies  
# of all array elements in O(1) extra  
# space and O(n) time  

  
# Function to find counts of all elements  
# present in arr[0..n-1]. The array  
# elements must be range from 1 to n  

def printfrequency(arr, n): 

  

    # Subtract 1 from every element so that  

    # the elements become in range from 0 to n-1  

    for j in range(n): 

        arr[j] = arr[j] - 1

  

    # Use every element arr[i] as index  

    # and add 'n' to element present at  

    # arr[i]%n to keep track of count of  

    # occurrences of arr[i]  

    for i in range(n): 

        arr[arr[i] % n] = arr[arr[i] % n] + n 

  

    # To print counts, simply print the  

    # number of times n was added at index  

    # corresponding to every element  

    for i in range(n): 

        print(i + 1, "->", arr[i] // n) 

  
# Driver code 

arr = [2, 3, 3, 2, 5] 

n = len(arr) 
printfrequency(arr, n) 
