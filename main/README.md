# Brand Ripplr Assessment Test

## Q1.
### Create a model in Django...
    
    - Create a model in Django with a minimum of 4 attributes.
    - Register that model in Django Admin. 
    - Make sure this Model instance is accessible by 1 user (on the admin site) at a time.
    
> Example: 
    User_1 logs in to Django Admin and accesses this model instance. Now User_1 can see all the fields and edit them. Meanwhile, User_2 opens the same modelin Django admin. User_2 can't edit this model and all actions are disabled. As soon asUser_1 closes this form (navigating away from form) User_2 can edit it.

__________________________________________________

### Response: 

> Done in the Project  => blog.models.py & blog.admin.py

# Q2. 
### It is very challenging task to implement search algorithms that provide relevant results because of the complexity of any language.

Explain theoretically, (without implementation) how would you use machine learning
concepts and techniques to deliver relevant results considering the above points in a
search engine context to return relevant results considering the following points:
 - Different words, sometimes, refer to a common concept. Eg.: men, man ; tree,
trees;
 - The same word has different meanings given the context. Eg: Free parking (no
cost for the parking); Meat free restaurant (no meat dishes served).

### Q2 Response

This is indeed a very challenging task.
I think this requires to analyze the search queries through a Natural Language Processing perspective. In this matter a very useful platform offering some more in depth documentation and libraries is [SciKit-Learn.org](http://scikit-learn.org/stable/related_projects.html#domain-specific-packages).
A Python related Library doing something like this would be: [Natural language toolkit (nltk)](http://www.nltk.org/) - Natural language processing and some machine learning.

# Q3. 

### Find the attached data.txt file which contains a dump JSON for the Business Data and Keyword Data.

1. Read all the data and index that in Elastic Search.
2. Create a GET type Api in Django which takes a query parameter (‘q’) and search within the index data in Elastic search. e.g. http://localhost:8000/search/?q=cafe
3. Create one simple HTML page with only 1 search text box in it, and hit the above listed api from the search box text.

### Q3 Response

> Done in the Project => blog.views.py


### Q4. Optimize and correct the following Python code snippet.

##### The following method was implemented to shuffle the elements of a list with some restrictions but it’s not working as expected.

Here are the restrictions:
    - Elements on the list can move randomly to the left or to the right
    - Elements must not move more than one position away from the original one
    - The list is non circular.
    
##### How would you change the algorithm to work as expected?


Input Value = [21, 22, 23, 24, 25, 26, 27, 28]
Output Value: [22, 21, 24, 23, 26, 25, 28, 27]

```python
def _shuffle_list_values(self):
    ids_list = [-1122, 2321, -9023, 2711, 8112, -0912, 2711, 9832]
    random_movements = {}
    for n_id in ids_list:
        movement = random.randrange(-1, 2, 1)
        random_movements[n_id] = movement
        
    left = -1
    right = 1
    shuffled_list = [x for x in ids_list]
    
    for n_id in ids_list:
        if not(ids_list.index(n_id) == 0 and random_movements[n_id] == left) or\
        not(ids_list.index(n_id) == len(ids_list) - 1 and random_movements[n_id] == right):
            shuffled_list.insert(ids_list.index(n_id) + random_movements[n_id],
            shuffled_list.pop(ids_list.index(n_id)))
    return shuffled_list
```

### Response:
```python
import random

t_list = [21, 22, 23, 24, 25, 26, 27, 28]
t_list2 = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38]
t_list3 = [-1122, 2321, -9023, 2711, 8112, -912, 2711, 9832] # Edited 6th element -0912 to -912

def new_shuffle_list_values(old):
    top, formated = len(old)-1, [] 
    for i, x in enumerate(old):
        if not i:
            new_index = i +  random.choice([0,1])
        elif i == top:
            new_index = i +  random.choice([-1,0])
        else:
            if p == i-1:
                new_index = i +  random.choice([0,1])
            elif p == i:
                new_index = i +  random.choice([-1,1])
            else:
                new_index = i +  random.choice([-1, 0, 1])
        formated.append((x, new_index))
        p = new_index         
    return [x[0] for x in sorted(formated, key=lambda s: s[1])]

```


### Q5. Share an example of your work (code/repository) that you are proud of and tell us why.


> Creates a listings cloud grid in one hit on the database


```python
# -*- coding: utf-8 -*-
from itertools import product

from django.db.models import When, Value, Q


def build_interval(min_value, max_value, count):
    interval_size = abs(max_value - min_value) / count

    for i in xrange(count):
        yield (
            min_value + i * interval_size,
            min_value + (i + 1) * interval_size
        )


def get_cells(min_lat, min_long, max_lat, max_long, row_count, col_count):
    print list(build_interval(min_lat, max_lat, row_count))
    print list(build_interval(min_long, max_long, col_count))
    return product(
        build_interval(min_lat, max_lat, row_count),
        build_interval(min_long, max_long, col_count)
    )


def get_cell_info(i, boundaries):
    """
    Gets info about cell by boundaries
    Args:
        i: number of item
        boundaries: tuple of tuples with min/max latitude/ longitude
    Returns: dict with center of grid, and case condition for listings
    """
    ((min_lat, max_lat), (min_long, max_long)) = boundaries
    center_lat = (min_lat + max_lat) / 2
    center_long = (min_long + max_long) / 2
    return {
        'center_lat': center_lat,
        'center_long': center_long,
        'condition': When(
            (
                Q(latitude__gt=min_lat) &
                Q(latitude__lte=max_lat) &
                Q(longitude__gt=min_long) &
                Q(longitude__lte=max_long)
            ),
            then=Value(i)
        )
    }


def build_grid(min_lat, min_long, max_lat, max_long, row_count, col_count):
    """
    Builds map grid with numbers of grid and count of cells
    map - is a dict where key is number of grid and value it's a dictionary with
    center of grid, condition for numbering listings
    Args:
        min_lat: Decimal
        min_long: Decimal
        max_lat: Decimal
        max_long: Decimal
        row_count: Integer
        col_count: Integer
    Returns:
    """
    cells = get_cells(
        min_lat,
        min_long,
        max_lat,
        max_long,
        row_count,
        col_count
    )

    return {
        i: get_cell_info(i, boundaries)
        for i, boundaries in enumerate(cells)
    }
```
### Q6. (Bonus question): Write down the necessary test cases for Q1 and Q3.

#### Response:
> Done in the project => blog.tests/ => test_*.py

