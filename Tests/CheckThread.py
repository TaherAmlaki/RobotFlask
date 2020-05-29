import threading
from robot import run

options =
t1 = threading.Thread(target=run, args=("./GetStarWarsFilms.robot",))
t2 = threading.Thread(target=run, args=("./GetStarWarsPlanets.robot",))

t1.start()
t2.start()
t1.join()
t2.join()
