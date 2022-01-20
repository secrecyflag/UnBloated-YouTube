#!/usr/bin/python3
"""
AUTHOR: secrecyflag

YouTube base.js contains a line for deciphering the signature.
for example (pretty print):
```js
coa = function(a) {
    a=a.split("");
    lC.ln(a,32);
    lC.fA(a,1);
    lC.c2(a,7);
    lC.fA(a,16);
    lC.c2(a,7);
    lC.c2(a,53);
    lC.ln(a,10);
    lC.fA(a,88);
    lC.ln(a,19);
    return a.join("")
};

var lC = {
    fA:function(a,b) {  // splice
        a.splice(0,b)
    },
    ln:function(a) {  // reversing
        a.reverse()
    },
    c2:function(a,b) {  // swapping
        var c=a[0];
        a[0]=a[b%a.length];
        a[b%a.length]=c
    }
};
```
lC variable is the "dictionary" of functions, which does the following operations:
Splicing, reversing and swapping.
All those operations need to be done in the order said for example above,
and this order changes frequently (don't know how frequently; I mean its changing somehow).
"""
import re
from constants import RePatterns


def get_initial_function_body(js: str) -> str:
    """
    Returns the deciphering line
    
    :param js: base.js lines
    :return: JS deciphering line
    """
    body = re.search(RePatterns.DECIPHER_FUNCTION, js)
    if body is not None:
        return body.group()


def get_initial_function_operations(js: str) -> list:
    """

    :return:
    """
    body = get_initial_function_body(js)
    start_body_index = body.index("{")
    body = body[start_body_index+1:-2]
    return body.split(";") 


def get_initial_function_name(js: str):
    return get_initial_function_body(js).split("=")[0].strip()


def get_dict_name(body: str):
    """
    Returns the dictionary of functions name.

    :return:
    """
    dict_name = re.search(RePatterns.DICT_FUNCTION_NAME, body).group()
    return dict_name


def get_dict_functions(js: str) -> dict:
    """
    The main function contains all the other sub functions, 
    such for `reverse`, `splice` and swapping.
    
    :return: dict: {function name: body ...}
    """
    functions = {}
    dict_name = get_dict_name(get_initial_function_body(js))
    pattern = RePatterns.find_dict_functions(dict_name)
    pattern = pattern.replace("$", "\$")  # if there is $ char in dictionary name
    functions_list = re.search(pattern, js)
    if functions is not None:
        # reformatting to a dictionary
        functions_list = functions_list.group().split("\n")
        for function in functions_list:
            function_name, body = function.split(":")
            functions[function_name] = body
        return functions


def get_parameters(command):
    """
    Returns the parameters when calling a function.
    for example: `lc.ln(a,52)` -> [a, 52]. 

    :return: parameters, list
    """
    start_parameters = command.index("(")
    parameters = command[start_parameters+1:-1]
    return parameters.split(",")


def extract_function_from_command(command):
    """
    Extracts and returns the function used in the current command.
    for example: `lc.ln(a,52)` -> ln

    :return: function name
    """
    function_name = command.split(".")[1]
    end_index = function_name.index("(")
    function_name = function_name[:end_index]
    return function_name


def swap(a: list, b: int):
    """
    Swapping implementation from JS to python.

    :return: swapped a/signature
    """
    c = a[0]
    a[0] = a[b % len(a)]
    a[b % len(a)] = c
    return a



def decrypt(signature: str, js: str):
    """
    Main function for decrypting the signature cipher.
    
    :param signature: original signature, encrypted
    :param js: base.js contents
    :return: the decrypted signature
    """
    functions = get_dict_functions(js)
    signature = [char for char in signature]
    for command in get_initial_function_operations(js):
        parameters = get_parameters(command)
        if parameters[0] == '""':  # if there are no parameters
            continue
        function_name = extract_function_from_command(command)
        body = functions[function_name]
        if "reverse" in body:
            signature.reverse()
        elif "splice" in body:
            for i in range(int(parameters[1])):
                signature.remove(signature[0])
        else:
            signature = swap(signature, int(parameters[1])) 
    return "".join(signature)

