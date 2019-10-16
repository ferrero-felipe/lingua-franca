import multiprocessing
import tkinter as Tk
from queue import Empty







if __name__ == '__main__':
   q = multiprocessing.Queue()
   info = multiprocessing.Queue()
   frames_q = multiprocessing.Queue()
   q.cancel_join_thread()  # or else thread that puts data will not term
   gui = GuiApp()  # q)
   # t1 = multiprocessing.Process(target=print_b, args=(q,info))
   t1 = multiprocessing.Process(target=live, args=(q, info, frames_q))
   t1.start()
   gui.root.mainloop()
   t1.join()
   print("closed")