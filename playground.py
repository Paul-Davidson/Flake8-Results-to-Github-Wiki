a = """
h2. Coverage Pie Chart

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'pie1': 'green', 'pie2': 'red', 'primaryTextColor': 'white', 'pieOpacity': 1, 'pieStrokeWidth': 0, 'pieOuterStrokeWidth': 0, 'pieStrokeColor': 'white', 'pieOuterStrokeColor': 'white'}}}%%
pie title
    "Covered" : %(covered)s
    "Not Covered" : %(not_covered)s
```
""" % {
    "covered": 2,
    "not_covered": 1
}

print(a)