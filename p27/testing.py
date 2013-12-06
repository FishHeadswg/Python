#Finishing the page ranking algorithm.
    

def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 100 #number of loops
    ranks = {} #dict of rank for each page
    npages = len(graph) #number of pages in graph
    for page in graph: # initializes rank dict by giving an initial rank for each page
        ranks[page] = 1.0 / npages
    for i in range(0, numloops): # Looping through ranking algorithm nloops times
        newranks = {} #dictionary of new ranks computed by number of times each page is linked to in another page
        for page in graph: # for each url in the graph dictionary that lists each url and the urls it links to
            newrank = (1 - d) / npages #new rank for the current url is 1 - damping faction / number of pages
            for i in graph: #for reach url in the graph dictionary
                if page in graph[i]: # if the current page is found in a url's dictionary
                    newrank += (d * ranks[i])/len(graph[i]) #the new rank for the current page is (the damping faction times the rank of the page / the number of unique urls in the graph dictionary) ADDED to the current rank (if the url is found in another url the rank increases)
            newranks[page] = newrank #newrank dictionary is updated with the new rank of the page
        ranks = newranks #after going through all urls in the graph dict, the initial ranks are swapped for the calculated ranks
    return ranks



cache = {
   'http://udacity.com/cs101x/urank/index.html': """<html>
<body>
<h1>Dave's Cooking Algorithms</h1>
<p>
Here are my favorite recipies:
<ul>
<li> <a href="http://udacity.com/cs101x/urank/hummus.html">Hummus Recipe</a>
<li> <a href="http://udacity.com/cs101x/urank/arsenic.html">World's Best Hummus</a>
<li> <a href="http://udacity.com/cs101x/urank/kathleen.html">Kathleen's Hummus Recipe</a>
</ul>

For more expert opinions, check out the 
<a href="http://udacity.com/cs101x/urank/nickel.html">Nickel Chef</a> 
and <a href="http://udacity.com/cs101x/urank/zinc.html">Zinc Chef</a>.
</body>
</html>






""", 
   'http://udacity.com/cs101x/urank/zinc.html': """<html>
<body>
<h1>The Zinc Chef</h1>
<p>
I learned everything I know from 
<a href="http://udacity.com/cs101x/urank/nickel.html">the Nickel Chef</a>.
</p>
<p>
For great hummus, try 
<a href="http://udacity.com/cs101x/urank/arsenic.html">this recipe</a>.

</body>
</html>






""", 
   'http://udacity.com/cs101x/urank/nickel.html': """<html>
<body>
<h1>The Nickel Chef</h1>
<p>
This is the
<a href="http://udacity.com/cs101x/urank/kathleen.html">
best Hummus recipe!
</a>

</body>
</html>






""", 
   'http://udacity.com/cs101x/urank/kathleen.html': """<html>
<body>
<h1>
Kathleen's Hummus Recipe
</h1>
<p>

<ol>
<li> Open a can of garbonzo beans.
<li> Crush them in a blender.
<li> Add 3 tablesppons of tahini sauce.
<li> Squeeze in one lemon.
<li> Add salt, pepper, and buttercream frosting to taste.
</ol>

</body>
</html>

""", 
   'http://udacity.com/cs101x/urank/arsenic.html': """<html>
<body>
<h1>
The Arsenic Chef's World Famous Hummus Recipe
</h1>
<p>

<ol>
<li> Kidnap the <a href="http://udacity.com/cs101x/urank/nickel.html">Nickel Chef</a>.
<li> Force her to make hummus for you.
</ol>

</body>
</html>

""", 
   'http://udacity.com/cs101x/urank/hummus.html': """<html>
<body>
<h1>
Hummus Recipe
</h1>
<p>

<ol>
<li> Go to the store and buy a container of hummus.
<li> Open it.
</ol>

</body>
</html>




""", 
}

def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = [seed]
    crawled = [] #list of urls to crawl
    graph = {}  # <url>, [list of pages it links to]
    index = {} # dict of each keyword and the urls it appears in
    while tocrawl: # while there are urls still left to crawl
        page = tocrawl.pop() #pop off the last url in tocrawl
        if page not in crawled: #if url has not been crawled already
            content = get_page(page) #gets the url content from the cache
            add_page_to_index(index, page, content) #splits the contents into words and adds each word to the index
            outlinks = get_all_links(content) #finds urls in the contents and puts them into the links list
            graph[page] = outlinks # takes the page and inserts it into the graph dict along with all the urls it links to
            union(tocrawl, outlinks) # adds the pages linked to the list of urls to be crawled
            crawled.append(page) # adds url to the list of crawled urls
    return index, graph # after crawling all urls, the keyword dictionary (index) and url dictionary (graph) are returned


def get_page(url):
    if url in cache:
        return cache[url]
    else:
        return None
    
def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links


def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)

def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)
        
def add_to_index(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

def lucky_search(index, ranks, keyword):
    matches = lookup(index, keyword)
    if not matches:
        return None
    best_match = matches[0]
    for url in matches:
        if ranks[url] > ranks[best_match]:
            best_match = url
    return best_match

def quicksort_pages(pages, ranks):
    if not pages or len(pages) <= 1:
        return pages
    else:
        pivot = ranks[pages[0]]
        worse = []
        better = []
        for page in pages[1:]:
            if ranks[page] <= pivot:
                worse.append(page)
            else:
                better.append(page)
        return quicksort_pages(better, ranks) + [pages[0]] + quicksort_pages(worse, ranks)

def ordered_search(index, ranks, keyword):
    pages = lookup(index, keyword)
    return quicksort_pages(pages, ranks)

index, graph = crawl_web('http://udacity.com/cs101x/urank/index.html')
ranks = compute_ranks(graph)
#Here's an example of how your procedure should work on the test site: 
print ordered_search(index, ranks, "Hummus")