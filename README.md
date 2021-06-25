# Socket Multithreading with Python
This is the final project for Computer Architecture course. It shows the usage of multithreading alongside socket programming using Python.

## How to use
Open a terminal in the root directory of this project and type:
```
python server.py public
```
Open your browser and type the following in the address bar
```
localhost:8085
```
You should be able to see the following page: <br>
![sdvdfvd](https://user-images.githubusercontent.com/33752872/123389815-78af6900-d5c4-11eb-9e92-b1483e46125d.png) <br>

You can also browse to `localhost:8085/noanime.jpg` to get this image <br>
![noanime](https://user-images.githubusercontent.com/33752872/123390148-ccba4d80-d5c4-11eb-9fe1-d2fc233e0724.jpg) <br>

If you see in the console now, you will see the following output:
```
[ACTIVE CONNECTIONS OR ACTIVE THREADS] 1
```
This shows that there is only 1 active thread currently running in the local network. Try opening a new tab or use a different browser (or go incognito mode for google chrome) and notice that the number goes up.
```
[ACTIVE CONNECTIONS OR ACTIVE THREADS] 2
```
This shows that there is another thread running/connected to the server.
