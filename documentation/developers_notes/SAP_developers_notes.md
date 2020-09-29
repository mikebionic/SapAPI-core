# Developer notes for every SapHasap/SapSolution [Sap Chozgut] developer
**Authors:** 
+ Muhammetberdi Jepbarov | muhammedjepbarov@gmail.com | [GitHub](github.com/mike-bionic) | [LinkedIn](https://www.linkedin.com/in/muhammed-jepbarov/)
## Follow these simple rules to keep on pragmatic development and avoid misunderstandings, code crashes, arguments
-----------
## Always keep an identation
**Important!**
>Configuring your IDE (Sublime Text, VS-code, vi, vim, Atom ...) make **Tab Size** = 2 as default.
+ For Python - **Tabs**
+ HTML/CSS/JS - **Tabs (2 space size) or 2 spaces** 
-----------
## Keep on modular app development
+ For **Flask** microframework use Blueprints
+ Code the **soft-relation** way (you sould be able to throw away the whole module without crashing the app)
+ Manage **folders** and **code-files** for easy orientation and understanding
-----------
## Specify routes depending on a platform or method of work
```python
# example of api routes of client applications
def api_checkout():
  pass

# example of ssr driven app routes for ajax requests
def ui_checkout():
  pass
```
-----------
## Spaces
+ Add **space** after "," in dictionaries, lists, tuples, arguments
and after ":" in dictionaries 
```python
resources = {
  "ResName": "Product 1",
  "ResPrice": 54.6,
  "Colors": ["Red", "Blue"]
}
```
+ Put **space** arount assignments and comparisons (except arguments)
```python
def check_status(active=True):
  if active:
    if resource.status == active:
      return active
```
+ Put **one** line break between functions and **two** line breaks between classes
```python
def fucntion():
  pass

def second_function():
  pass


class Resource(self,name,price):
  self.name == name
  self.price == price
```
-----------
## Notes / questions / tasks
+ use triple "!" or "?" signs to put notes and question inside the code, because it's searchable for other developers and yourself
```python
# !!! BUG: the response is crashing

# !!! TODO: convert to single function

# ??? Why is it crashing?
```
-----------
## Variables and naming
+ use snake_case in **Python**
+ use camelCase in **JavaScript**
-----------
## Quotes or double-quotes
+ use **double-quotes " "** in dictionaries, lists, tuples and JSON
+ use **single-quotes ' '** in request methods
```python
if request.method == 'GET':
  response = {
    "status": 1,
    "message": "success"
  }
  return response
```
-----------
## Exceptions and error handling
+ Always handle errors (database insertions, functions, etc.)
```python
def division(num=0):
  try:
    division_result = 5/num
  except Exception as ex:
    # print exception message ("Error: division by zero")
    print(ex)
    division_result = 0
  return division_result 
```
+ Put Datetime, Description, [optional: Name] to make logging better and figure the issue faster
```python
from datetime import datetime
try:
  function()
except Exception as ex:
  print(f"{datetime.now()} | Module Exception | (John Doe): {ex}")
``` 
-----------
# API development tips
## Response status codes
+ return correct status codes depending on result (ex: 200, 201, 400)
```python
# Good: correct response codes
def checkout():
  try:
    db_insertion()
    response = "success"
    return make_response(response), 201
  except:
    response = "error"
    return make_response(response), 400

# Bad: same response code for every case
def checkout():
  try:
    db_insertion()
    response = "success"
  except:
    response = "error"
  return make_response(response),200
```