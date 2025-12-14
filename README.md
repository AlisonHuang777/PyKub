### About PyKub
PyKub is a python script implementation of the famous board game Rummikub. For rules, see [Wikipedia](https://en.wikipedia.org/wiki/Rummikub) for reference.
In this implementation, after the game begins, there are 5 commands:
- `info`: displays what kubs are currently on the table and what kubs you have.
- `take`: takes a kubset from the table to your stack.
- `play`: plays a (valid) kubset from your stack to the table.
- `end`: ends the current turn.
- `exit`: exits the game and closes the program.
### About the files
`PyKub.py` is initially made for a high school project. For the university project, the files are `PyKubConnected.py` and `PyKubClient.py`, which is a modification of the original version that is capable of co-op.
To use it, run `PyKubConnected.py` first on a device. The program will display the IPv4 and the port. Then, run `PyKubClient.py` on another device, which you can enter the IPv4 and the port to establish a connection. If the operation is successful, the game will automatically starts.
