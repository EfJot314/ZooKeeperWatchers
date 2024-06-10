from kazoo.client import KazooClient
from tkinter import messagebox
import subprocess



class ZooFollower:
    def __init__(self, host: str, app_cmd: str):
        self.app_cmd = app_cmd
        self.app = None

        self.last_number_of_children = 0

        self.zk = KazooClient(hosts=host)

    def start(self):
        self.zk.start()
        #define watchers
        self.zk.DataWatch("/a", self.handle_app)
        if self.zk.exists("/a"):
            self.zk.ChildrenWatch("/a/", self.handle_children_with_path("/a"))

    def stop(self):
        self.zk.stop()

    def handle_app(self, data: object, stat: object):
        # /a has been deleted
        if stat is None:
            if self.app is not None:
                self.app.terminate()
                self.app = None
        # /a has been created
        else:
            self.zk.ChildrenWatch("/a/", self.handle_children_with_path("/a"))
            if self.app is None:
                self.app = subprocess.Popen(self.app_cmd)

    def get_node_tree(self, path):
        to_return = (path, [])
        children = self.zk.get_children(path)
        for child in children:
            to_return[1].append(child)
        return to_return

    def get_tree(self):
        if not self.zk.exists("/a"):
            return []
        tree = []
        tree.append(self.get_node_tree("/a"))
        for node_tree in tree:
            for child in node_tree[1]:
                path = f"{node_tree[0]}/{child}"
                tree.append(self.get_node_tree(path))
        return tree

    def get_number_of_children(self, path: str):
        counter = 0
        children = self.zk.get_children(path)
        for child in children:
            counter += 1
            counter += self.get_number_of_children(f"{path}/{child}")
        return counter

    def handle_children_with_path(self, path):
        def handle_children(children: list[str]):
            for child in children:
                new_path = f"{path}/{child}"
                self.zk.ChildrenWatch(f"{new_path}/", self.handle_children_with_path(new_path))
            actual_children_num = self.get_number_of_children("/a")
            if actual_children_num > self.last_number_of_children:
                if len(children) is not None:
                    messagebox.showinfo("Zoo Follower", f"Number of children: {actual_children_num}")
            self.last_number_of_children = actual_children_num
        return handle_children




#get info
print("Type address and port of zookeeper client:")
host = input()
print("Type application command to run:")
app_cmd = input()

#run follower
follower = ZooFollower(host, app_cmd)
follower.start()


#main loop
try:
    while True:
        #handle commands
        comm = input().strip()
        if comm == "x":
            follower.stop()
            break
        elif comm == "tree":
            tree = follower.get_tree()
            for node_tree in tree:
                print(node_tree[0], "->", node_tree[1])
except KeyboardInterrupt:
    follower.stop()




