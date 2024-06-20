#!/usr/bin/env python
# coding: utf-8

# In[2]:


def preprocess_strong_suffix(shift, bpos, pat, m):
    #initialize the last border position
    i = m
    j = m + 1
    bpos[i] = j

    #process the pattern from right to left
    while i > 0:
        #find the next border position
        while j <= m and pat[i - 1] != pat[j - 1]:
            if shift[j] == 0:
                 #compute the shift value for the current border position
                shift[j] = j - i
            j = bpos[j]
        i -= 1
        j -= 1
        #assign the border position
        bpos[i] = j

def preprocess_case2(shift, bpos, pat, m):
    #use the border positions to set shift values
    j = bpos[0]
    for i in range(m + 1):
        if shift[i] == 0:
            #set the shift value based on the border position
            shift[i] = j
        if i == j:
            j = bpos[j]

def boyer_moore(text, pattern):
    #preprocessing phase
    n = len(text)  #n = lngth of the text
    m = len(pattern)  #m = length of the pattern
    if m == 0:
        #case: empty pattern
        return "Pattern cannot be empty"  
    if n < m:
        #case: pattern longer than text
        return "Text length must be greater than or equal to pattern length"  

    #generate bad character skip list
    bad_char_table = {chr(i): m for i in range(256)}  #initialize all characters to length of pattern
    for i in range(m - 1):
        #bad character rule formula: max(1, m - i - 1)
        bad_char_table[pattern[i]] = max(1, m - i - 1)
    bad_char_table['*'] = m  #default shift for characters not in the pattern

    #create an ordered list of bad character table entries for display
    ordered_bad_char_table = {char: bad_char_table[char] for char in pattern}
    ordered_bad_char_table['*'] = m

    #generate good suffix skip list
    good_suffix_table = [0] * (m + 1) #initialize the good suffix table
    border = [0] * (m + 1) #initialize the border array
    preprocess_strong_suffix(good_suffix_table, border, pattern, m) #preprocess the strong suffixes
    preprocess_case2(good_suffix_table, border, pattern, m) #use the strong suffixes to create the good suffix table

    #print text, pattern, bad character table, and good suffix table
    print("Text:", text)
    print("Pattern:", pattern)
    print("Bad Character Table:", ordered_bad_char_table)
    print("Good Suffix Table:")
    for k, shift in enumerate(reversed(good_suffix_table[:-1]), 1):  #assign shift value to k for display
        if k < m:
            #display the shift values for good suffixes
            print(f"k{k} = {shift}")

    #search phase
    i = 0  #starting index in the text
    comparisons = 0  #count the number of character comparisons
    shifts = []  #track the shifts made during the search
    matches = []  #track the indices where pattern matches

    while i <= n - m:
        j = m - 1  #start comparing from the end of the pattern
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1  #move left if characters match
            comparisons += 1
        if j < 0:
            matches.append(i)  #pattern found at index i
            i += good_suffix_table[0]  #shift pattern to align with the next possible match
            shifts.append(good_suffix_table[0])
        else:
            comparisons += 1
            
            #bad character shift: bad_char_table.get(text[i + j], m)
            bad_char_shift = bad_char_table.get(text[i + j], m)
            
            #good suffix shift: good_suffix_table[j + 1]
            good_suffix_shift = good_suffix_table[j + 1]
            
            # Shift formula: max(good_suffix_shift, bad_char_shift)
            shift = max(good_suffix_shift, bad_char_shift)
            shifts.append(shift)
            i += shift

    if matches:
        return (f"Number of comparisons: {comparisons}\n"
                f"Shifts: {shifts[:-1]}\n"
                f"Pattern occurs at indices: {matches}\n")  
    else:
        return (f"Pattern not found\n"
                f"Number of comparisons: {comparisons}\n"
                f"Shifts: {shifts[:-1]}")  # print until k(m-1)

#example usage with test cases of various scenarios

#basic match
text = "ini_kuyulayu" 
pattern = "kuyulayu"
print(boyer_moore(text, pattern))

#multiple matches
text = "abababab"
pattern = "ab"
print(boyer_moore(text, pattern))

#pattern at the end
text = "abcdef"
pattern = "def"
print(boyer_moore(text, pattern))

#pattern with repeating characters
text = "aaaaaa"
pattern = "aaa"
print(boyer_moore(text, pattern))

#non-alphabet characters
text = "1234567890"
pattern = "567"
print(boyer_moore(text, pattern))

#pattern not found
text = "abcdef"
pattern = "gh"
print(boyer_moore(text, pattern))


# In[ ]:





# In[ ]:




