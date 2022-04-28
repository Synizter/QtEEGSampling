class a:
    def __init__(self, fn, *args, **kwargs):
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.var_in_a = 666

        print(self.fn)
        print(self.args)
        print(self.kwargs)
    
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception as e:
            print(e)
        else:
            print("This is the result from fn :", result)
        finally:
            pass

class b:
    def __init__(self):
        self.worker = a(self.execute_this_fn)
    
    def execute_this_fn(self):
        print("Hello from b")
        print("I can access attribute in a! :", self.var_in_a)
        return 69

t = b()
t.worker.run()