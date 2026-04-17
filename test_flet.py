import flet
try:
    print("Trying label")
    t1 = flet.Tab(label="test")
    print("label works")
except Exception as e:
    print("label Error", e)

try:
    print("Trying tab_content")
    t2 = flet.Tab(tab_content=flet.Text("test"))
    print("tab_content works")
except Exception as e:
    print("tab_content Error", e)
