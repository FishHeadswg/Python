# Question 4: Remove Tags

# When we add our words to the index, we don't really want to include
# html tags such as <body>, <head>, <table>, <a href="..."> and so on.

# Write a procedure, remove_tags, that takes as input a string and returns
# a list of words, in order, with the tags removed. Tags are defined to be
# strings surrounded by < >. Words are separated by whitespace or tags. 
# You may assume the input does not include any unclosed tags, that is,  
# there will be no '<' without a following '>'.

def make_converter(match, replacement):
    return [match, replacement]

def apply_converter(converter, string):
    previous = None
    while previous != string:
        previous = string
        position = string.find(converter[0])
        if position != -1:
            string = string[:position] + converter[1] + string[position + len(converter[0]):]
        return string

def remove_tags(content):
    start = content.find('<')
    while start != -1:
        end = content.find('>')
        content = content[:start] + ' ' + content[end + 1:]
        start = content.find('<')
    return content.split()
    


print remove_tags('''<h1>Title</h1><p>This is a
                    <a href="http://www.udacity.com">link</a>.<p>''')
#>>> ['Title','This','is','a','link','.']

print remove_tags('''<table cellpadding='3'>
                     <tr><td>Hello</td><td>World!</td></tr>
                     </table>''')
#>>> ['Hello','World!']

print remove_tags("<hello><goodbye>")
#>>> []

print remove_tags("This is plain text.")
#>>> ['This', 'is', 'plain', 'text.']